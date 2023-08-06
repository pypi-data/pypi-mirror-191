import urllib
import hashlib
import hmac
import time
import uuid
from copy import copy
from datetime import datetime, timedelta
from threading import Lock
from typing import Any, Dict, List, Tuple
import json
from requests.exceptions import SSLError

# REST API HOST
from strategy_api.event.engine import EventEngine, EVENT_TIMER, Event
from strategy_api.tm_api.Binance.futureInverse import Security
from strategy_api.tm_api.api.rest.rest_client import RestClient, Request, Response
from strategy_api.tm_api.api.websocket.websocket_client import WebsocketClient
from strategy_api.tm_api.base import BaseGateway
from strategy_api.tm_api.object import Exchange, Product, PositionSide, OrderRequest, Direction, Offset, CancelRequest, \
    HistoryRequest, DataType, Interval, OrderData, OrderType, BarData, Status, TickData, TdMode, Dest, Chain, \
    WithDrawData, TransferType, TransferRequest, DepthData, BidData, AskData
from strategy_api.tm_api.tools import symbol_deal, get_order_type

REST_HOST: str = "https://api.binance.com"

# Websocket API HOST
WEBSOCKET_TRADE_HOST: str = "wss://stream.binance.com:9443/ws/"
WEBSOCKET_DATA_HOST: str = "wss://stream.binance.com:9443/stream"

# order direction mapping
DIRECTION_VT2BINANCE: Dict[Direction, str] = {
    Direction.LONG: "BUY",
    Direction.SHORT: "SELL"
}

DIRECTION_BINANCE2VT: Dict[str, Direction] = {v: k for k, v in DIRECTION_VT2BINANCE.items()}

# GTC 成交为止, 一直有效
ORDERTYPE_VT2BINANCES: Dict[OrderType, Tuple[str, str]] = {
    OrderType.LIMIT: ("LIMIT", "GTC"),  # 限价单
    OrderType.MARKET: ("MARKET", "GTC"),  # 市价单
    OrderType.STOP_MARKET: ("STOP_MARKET", "GTC"),  # 止损单
    OrderType.TAKE_PROFIT_MARKET: ("TAKE_PROFIT_MARKET", "GTC")  # 止盈单
}

ORDERTYPE_BINANCES2VT: Dict[Tuple[str, str], OrderType] = {v: k for k, v in ORDERTYPE_VT2BINANCES.items()}

INTERVAL_VT2BINANCE: Dict[Interval, str] = {
    Interval.MINUTE: "1m",
    Interval.MINUTE_3: "3m",
    Interval.MINUTE_5: "5m",
    Interval.MINUTE_15: "15m",
    Interval.MINUTE_30: "30m",
    Interval.HOUR: "1h",
    Interval.HOUR_2: "2h",
    Interval.HOUR_4: "4h",
    Interval.HOUR_6: "6h",
    Interval.HOUR_8: "8h",
    Interval.HOUR_12: "12h",
}

TIMEDELTA_MAP: Dict[Interval, timedelta] = {
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1)
}

STATUS_BINANCE2VT: Dict[str, Status] = {
    "NEW": Status.NOTTRADED,
    "PARTIALLY_FILLED": Status.PARTTRADED,
    "FILLED": Status.ALLTRADED,
    "CANCELED": Status.CANCELLED,
    "REJECTED": Status.REJECTED,
    "EXPIRED": Status.CANCELLED
}

CHAIN_BINANCEVT2VT: Dict[str, Chain] = {
    "TRX": Chain.TRC20,
    "ETH": Chain.ERC20,
    "BSC": Chain.BNB_SMART_CHAIN,
    "BNB": Chain.BNB_BEACON_CHAIN,
}

CHAIN_VT2BINANCE: Dict[Chain, str] = {v: k for k, v in CHAIN_BINANCEVT2VT.items()}


class BinanceSpotGateway(BaseGateway):
    """
    binance spot gateway for howtrader
    """
    default_setting: Dict[str, Any] = {
        "key": "",
        "secret": "",
        "proxy_host": "",
        "proxy_port": 0,
    }

    exchange: Exchange = Exchange.BINANCE
    product: Product = Product.U_FUTURES
    symbolMap: dict = dict()
    SPOT_SET: set = set()
    MARGIN_SET: set = set()

    def __init__(self, event_engine: EventEngine, order_switch: bool = False, bar_switch: bool = False,
                 tick_switch: bool = False) -> None:
        """init"""
        super().__init__(event_engine, order_switch, bar_switch, tick_switch)

        self.trade_ws_api: "BinanceSpotTradeWebsocketApi" = BinanceSpotTradeWebsocketApi(self)
        self.cross_trade_ws_api: "BinanceCrossTradeWebsocketApi" = BinanceCrossTradeWebsocketApi(self)
        self.isolated_trade_ws_api: "BinanceIsolatedTradeWebsocketApi" = BinanceIsolatedTradeWebsocketApi(self)

        self.market_ws_api: "BinanceSpotDataWebsocketApi" = BinanceSpotDataWebsocketApi(self)
        self.rest_api: "BinanceSpotRestAPi" = BinanceSpotRestAPi(self)
        self.get_server_time_interval: int = 0

    def connect(self, setting: dict):
        """connect binance api"""
        key: str = setting["key"]
        secret: str = setting["secret"]

        if isinstance(setting["proxy_host"], str):
            proxy_host: str = setting["proxy_host"]
        else:
            proxy_host: str = ""

        if isinstance(setting["proxy_port"], int):
            proxy_port: int = setting["proxy_port"]
        else:
            proxy_port: int = 0

        self.rest_api.connect(key, secret, proxy_host, proxy_port)
        self.market_ws_api.connect(proxy_host, proxy_port)
        if self.order_call_switch:
            self.event_engine.unregister(EVENT_TIMER, self.process_timer_event)
            self.event_engine.register(EVENT_TIMER, self.process_timer_event)

            self.event_engine.unregister(EVENT_TIMER, self.trade_ws_api.ping_pong)
            self.event_engine.register(EVENT_TIMER, self.trade_ws_api.ping_pong)

            self.event_engine.unregister(EVENT_TIMER, self.cross_trade_ws_api.ping_pong)
            self.event_engine.register(EVENT_TIMER, self.cross_trade_ws_api.ping_pong)

            self.event_engine.unregister(EVENT_TIMER, self.isolated_trade_ws_api.ping_pong)
            self.event_engine.register(EVENT_TIMER, self.isolated_trade_ws_api.ping_pong)

        self.event_engine.unregister(EVENT_TIMER, self.market_ws_api.ping_pong)
        self.event_engine.register(EVENT_TIMER, self.market_ws_api.ping_pong)

    def process_timer_event(self, event: Event) -> None:
        """process timer event, for updating the listen key"""
        self.rest_api.keep_user_stream()
        self.rest_api.keep_cross_user_stream()
        self.rest_api.keep_isolated_user_stream()
        self.get_server_time_interval += 1
        if self.get_server_time_interval >= 300:  # get the server time for every five miute
            self.rest_api.query_time()
            self.get_server_time_interval = 0

    def new_order_id(self) -> str:
        return self.rest_api.get_order_id()

    # 多头买进
    def buy(self,
            orderid: str,
            symbol: str,
            volume: float,  # 数量
            price: float = 0,  # 价格
            maker: bool = False,  # 限价单
            stop_loss: bool = False,  # 止损
            stop_loss_price: float = 0,  # 止损价
            stop_profit: bool = False,  # 止盈
            stop_profit_price: float = 0,  # 止盈价
            position_side: PositionSide = PositionSide.ONEWAY,
            tdMode: TdMode = TdMode.CROSS,
            ccy: str = ""
            ):
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.LONG,
            offset=Offset.OPEN,
            type=get_order_type(maker, stop_loss, stop_profit, self.exchange),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange,
            stop_loss_price=stop_loss_price,
            stop_profit_price=stop_profit_price,
            reference=symbol + "__" + "MARGIN_BUY",
            tdMode=tdMode
        )
        self.send_order(original_req, orderid)

        # 多头卖出

    def sell(self,
             orderid: str,
             symbol: str,
             volume: float,  # 数量
             price: float = 0,  # 价格
             maker: bool = False,  # 限价单
             stop_loss: bool = False,  # 止损
             stop_loss_price: float = 0,  # 止损价
             stop_profit: bool = False,  # 止盈
             stop_profit_price: float = 0,  # 止盈价
             position_side: PositionSide = PositionSide.ONEWAY,
             tdMode: TdMode = TdMode.CROSS,
             ccy: str = ""
             ):
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.SHORT,
            offset=Offset.CLOSE,
            type=get_order_type(maker, stop_loss, stop_profit, self.exchange),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange,
            stop_loss_price=stop_loss_price,
            stop_profit_price=stop_profit_price,
            reference=symbol + "__" + "AUTO_REPAY",
            tdMode=tdMode
        )
        self.send_order(original_req, orderid)

        # 空头买进

    def short(self,
              orderid: str,
              symbol: str,
              volume: float,  # 数量
              price: float = 0,  # 价格
              maker: bool = False,  # 限价单
              stop_loss: bool = False,  # 止损
              stop_loss_price: float = 0,  # 止损价
              stop_profit: bool = False,  # 止盈
              stop_profit_price: float = 0,  # 止盈价
              position_side: PositionSide = PositionSide.ONEWAY,
              tdMode: TdMode = TdMode.CROSS,
              ccy: str = ""
              ):
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.SHORT,
            offset=Offset.OPEN,
            type=get_order_type(maker, stop_loss, stop_profit, self.exchange),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange,
            stop_loss_price=stop_loss_price,
            stop_profit_price=stop_profit_price,
            reference=symbol + "__" + "MARGIN_BUY",
            tdMode=tdMode
        )
        self.send_order(original_req, orderid)

        # 空头卖出

    def cover(self,
              orderid: str,
              symbol: str,
              volume: float,  # 数量
              price: float = 0,  # 价格
              maker: bool = False,  # 限价单
              stop_loss: bool = False,  # 止损
              stop_loss_price: float = 0,  # 止损价
              stop_profit: bool = False,  # 止盈
              stop_profit_price: float = 0,  # 止盈价
              position_side: PositionSide = PositionSide.ONEWAY,
              tdMode: TdMode = TdMode.CROSS,
              ccy: str = ""
              ):
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        original_req: OrderRequest = OrderRequest(
            symbol=new_symbol,
            direction=Direction.LONG,
            offset=Offset.CLOSE,
            type=get_order_type(maker, stop_loss, stop_profit, self.exchange),
            price=price,
            volume=volume,
            positionSide=position_side,
            exchange=self.exchange,
            stop_loss_price=stop_loss_price,
            stop_profit_price=stop_profit_price,
            reference=symbol + "__" + "AUTO_REPAY",
            tdMode=tdMode
        )
        self.send_order(original_req, orderid)

    def withdraw_coin(self, symbol: str,  # 币种
                      amount: float,  # 数量
                      toAddress: str,  # 提币地址（手机）
                      chain: Chain,  # 链
                      dest: Dest = Dest.CHAIN,  # 提币方式
                      fee: float = 0,  # 手续费设置
                      areaCode: str = ""  # 手机区号
                      ) -> bool:

        req: WithDrawData = WithDrawData(
            symbol=symbol,
            amount=str(amount),
            dest=dest,
            toAddress=toAddress,
            fee=str(fee),
            chain=chain,
            areaCode=areaCode
        )
        return self.rest_api.withdraw_coin(req)

    def transfer_coin(self, type: TransferType,
                      symbol: str,
                      amount: float,
                      fromSymbol: str = "",
                      toSymbol: str = "",
                      ) -> bool:
        req: TransferRequest = TransferRequest(
            type=type,
            symbol=symbol,
            amount=amount,
            fromSymbol=fromSymbol,
            toSymbol=toSymbol,
        )

        return self.rest_api.transfer_coin(req)

    # 发送订单
    def send_order(self, req: OrderRequest, orderid: str):
        self.rest_api.send_order(req, orderid)

    def query_symbol(self, quote_symbol: str, s_type: str = "") -> list:
        if s_type == "SPOT":
            return [i.replace(quote_symbol.upper(), "-" + quote_symbol.upper()) for i in self.SPOT_SET if i.endswith(quote_symbol.upper())]
        elif s_type == "MARGIN":
            return [i.replace(quote_symbol.upper(), "-" + quote_symbol.upper()) for i in self.MARGIN_SET if i.endswith(quote_symbol.upper())]
        else:
            return []

    # 撤销订单
    def cancel_order(self, orderid: str, symbol: str) -> None:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        req: CancelRequest = CancelRequest(
            orderid=orderid,
            symbol=new_symbol,
            exchange=self.exchange
        )
        self.rest_api.cancel_order(req)

    # 获取历史K线
    def query_history(self,
                      symbol: str,
                      interval: Interval,
                      hour: int = 0,
                      minutes: int = 0,
                      end_time: datetime = None
                      ) -> List[BarData]:

        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        if end_time:
            end: datetime = end_time
        else:
            end: datetime = datetime.now()

        if hour:
            start: datetime = end - timedelta(hours=hour)
        elif minutes:
            start: datetime = end - timedelta(minutes=minutes)
        else:
            print("分钟，小时参数都为0, 查询k线失败")
            return []

        req: HistoryRequest = HistoryRequest(
            symbol=new_symbol,
            start=start,
            end=end,
            interval=interval,
            exchange=self.exchange
        )
        return self.rest_api.query_history(req)

    def query_depth(self, symbol: str, limit: int) -> DepthData:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        depth_data: DepthData = DepthData(
            symbol=symbol,
            bid_data=[],
            ask_data=[]
        )

        if limit not in [5, 10, 20, 50, 100, 500, 1000, 5000]:
            print(f"无该档位: {limit}")
            return depth_data
        return self.rest_api.query_depth(new_symbol, limit, depth_data)

    # 订阅数据
    def subscribe(self, symbol: str, data_type: DataType, interval: Interval = None) -> None:
        new_symbol = symbol_deal(symbol, self.exchange)
        self.symbolMap[new_symbol] = symbol

        if data_type == DataType.TICK:
            self.market_ws_api.subscribe(new_symbol)
        elif data_type == DataType.BAR:
            if interval:
                self.market_ws_api.subscribe(new_symbol, interval)
            else:
                print(f"订阅失败，k 线数据未定义间隔时间")
        else:
            print(f"订阅失败，未知数据类型: {data_type}")

    # 关闭
    def close(self) -> None:
        self.rest_api.stop()
        self.trade_ws_api.stop()
        self.market_ws_api.stop()


class BinanceSpotRestAPi(RestClient):
    """binance spot rest api"""

    def __init__(self, gateway: BinanceSpotGateway) -> None:
        """init"""
        super().__init__()

        self.gateway: BinanceSpotGateway = gateway

        self.trade_ws_api: BinanceSpotTradeWebsocketApi = self.gateway.trade_ws_api
        self.cross_ws_api: BinanceCrossTradeWebsocketApi = self.gateway.cross_trade_ws_api
        self.isolated_ws_api: BinanceIsolatedTradeWebsocketApi = self.gateway.isolated_trade_ws_api

        self.key: str = ""
        self.secret: str = ""

        self.user_stream_key: str = ""
        self.cross_stream_key: str = ""
        self.isolated_stream_key: str = ""

        self.keep_alive_count: int = 0
        self.keep_cross_alive_count: int = 0
        self.keep_isolated_alive_count: int = 0

        self.keep_alive_failed_count: int = 0
        self.keep_cross_failed_count: int = 0
        self.keep_isolated_failed_count: int = 0

        self.recv_window: int = 10000
        self.time_offset: int = 0

        self.order_count: int = 1_000_000
        self.order_count_lock: Lock = Lock()
        self.connect_time: int = 0

    def sign(self, request: Request) -> Request:
        """signature for private api"""
        security: Security = request.data["security"]
        if security == Security.NONE:
            request.data = None
            return request

        if request.params:
            path: str = request.path + "?" + urllib.parse.urlencode(request.params)
        else:
            request.params = dict()
            path: str = request.path

        if security == Security.SIGNED:
            timestamp: int = int(time.time() * 1000)

            if self.time_offset > 0:
                timestamp -= abs(self.time_offset)
            elif self.time_offset < 0:
                timestamp += abs(self.time_offset)

            request.params["timestamp"] = timestamp

            query: str = urllib.parse.urlencode(sorted(request.params.items()))
            signature: bytes = hmac.new(self.secret, query.encode(
                "utf-8"), hashlib.sha256).hexdigest()

            query += "&signature={}".format(signature)
            path: str = request.path + "?" + query

        request.path = path
        request.params = {}
        request.data = {}

        # request headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "X-MBX-APIKEY": self.key,
            "Connection": "close"
        }

        if security in [Security.SIGNED, Security.API_KEY]:
            request.headers = headers

        return request

    def connect(
            self,
            key: str,
            secret: str,
            proxy_host: str,
            proxy_port: int
    ) -> None:
        """connect rest api"""
        self.key = key
        self.secret = secret.encode()
        self.proxy_port = proxy_port
        self.proxy_host = proxy_host

        self.connect_time = (
                int(datetime.now().strftime("%y%m%d%H%M%S")) * self.order_count
        )
        self.init(REST_HOST, proxy_host, proxy_port)
        self.start()

        # 获取服务器时间
        self.query_time()
        self.query_margin_contract()
        self.query_spot_contract()
        # 保持用户 ws 的链接
        if self.gateway.order_call_switch:
            self.start_user_stream()
            self.start_cross_stream()
            self.start_isolated_stream()

    def query_spot_contract(self) -> None:
        data: dict = {
            "security": Security.NONE
        }
        self.add_request(
            method="GET",
            path="/api/v3/exchangeInfo?permissions=SPOT",
            callback=self.on_query_spot_contract,
            data=data
        )

    def query_margin_contract(self) -> None:
        data: dict = {
            "security": Security.NONE
        }
        self.add_request(
            method="GET",
            path="/api/v3/exchangeInfo?permissions=MARGIN",
            callback=self.on_query_margin_contract,
            data=data
        )

    def query_time(self) -> None:
        """query time"""
        data: dict = {
            "security": Security.NONE
        }
        path: str = "/api/v3/time"

        self.add_request(
            "GET",
            path,
            callback=self.on_query_time,
            on_failed=self.on_query_time_failed,
            on_error=self.on_query_time_error,
            data=data
        )

    def _new_order_id(self) -> int:
        """generate customized order id"""
        with self.order_count_lock:
            self.order_count += 1
            return self.order_count

    def _new_withdraw_id(self) -> str:
        """generate customized order id"""
        return "".join(str(uuid.uuid4()).split("-"))

    def get_order_id(self) -> str:
        orderid: str = "x-A6SIDXVS" + str(self.connect_time + self._new_order_id())
        return orderid

    def withdraw_coin(self, req: WithDrawData) -> bool:
        asset_path = "/sapi/v1/capital/config/getall"
        resp: Response = self.request(
            "GET",
            asset_path,
            data={"security": Security.SIGNED}
        )
        if resp.status_code // 100 != 2:
            msg = f"获取资产信息失败，状态码：{resp.status_code}，信息：{resp.text}"
            print(msg)
        else:
            data: dict = resp.json()
            for coin in data:
                if coin['coin'] == req.symbol:
                    for one in coin['networkList']:
                        if CHAIN_VT2BINANCE[req.chain] == one['network']:
                            if float(one['withdrawMin']) > float(req.amount):
                                print("提币数量少于最小提币数量")
                                return False
                            if float(one['withdrawMax']) < float(req.amount):
                                print("提币数量大于最大提币数量")
                                return False

                            path = "/sapi/v1/capital/withdraw/apply"

                            params: dict = {
                                "coin": req.symbol,  # 币种
                                "withdrawOrderId": self._new_withdraw_id(),  # 自定义提币ID
                                "network": one['network'],  # 提币网络
                                "address": req.toAddress,  # 提币地址
                                "amount": req.amount,  # 提币数量
                                "walletType": 0
                            }

                            self.add_request(
                                method="POST",
                                path=path,
                                callback=self.on_withdraw_coin,
                                data={"security": Security.SIGNED},
                                params=params
                            )
                            return True
        return False

    def transfer_coin(self, req: TransferRequest) -> bool:
        path: str = "/sapi/v1/asset/transfer"
        params: dict = {
            "type": req.type,  # 币种
            "asset": req.symbol,  # 自定义提币ID
            "amount": req.amount,  # 提币网络
        }
        self.add_request(
            method="POST",
            path=path,
            callback=self.on_withdraw_coin,
            data={"security": Security.SIGNED},
            params=params
        )
        return True

    def send_order(self, req: OrderRequest, orderid: str):
        """send/place order"""
        # create order by OrderRequest
        order: OrderData = req.create_order_data(
            orderid
        )

        self.gateway.on_order(copy(order))

        data: dict = {
            "security": Security.SIGNED
        }
        params: dict = {
            "symbol": req.symbol,
            "side": DIRECTION_VT2BINANCE[req.direction],
            "quantity": req.volume,
            "newClientOrderId": orderid,
            "newOrderRespType": "RESULT",
            "recvWindow": self.recv_window
        }
        # 如果订单type = taker，那就是市价单，如果不是，则是限价单
        if req.type == OrderType.MARKET:
            params["type"] = "MARKET"  # 市价单
        elif req.type == OrderType.STOP_MARKET:
            params["type"] = "STOP_LOSS_LIMIT"  # 止损单
            params["price"] = req.price
            params["timeInForce"] = "GTC"
            params["stopPrice"] = req.stop_loss_price
        elif req.type == OrderType.TAKE_PROFIT_MARKET:
            params["type"] = "TAKE_PROFIT_LIMIT"  # 止赢单
            params["price"] = req.price
            params["timeInForce"] = "GTC"
            params["stopPrice"] = req.stop_profit_price
        else:
            order_type, time_condition = ORDERTYPE_VT2BINANCES[req.type]
            params["type"] = order_type
            params["timeInForce"] = time_condition
            params["price"] = req.price
        path = "/api/v3/order"
        if "MARGIN" in req.reference.split("__")[0]:
            if req.tdMode == TdMode.CROSS:
                params['islsolated'] = "FALSE"
            else:
                params['islsolated'] = "TRUE"
            params['sideEffectType'] = req.reference.split("__")[-1]
            path = "/sapi/v1/margin/order"

        self.add_request(
            method="POST",
            path=path,
            callback=self.on_send_order,
            data=data,
            params=params,
            extra=order,
            on_error=self.on_send_order_error,
            on_failed=self.on_send_order_failed
        )

    def cancel_order(self, req: CancelRequest) -> None:
        """cancel order"""
        data: dict = {
            "security": Security.SIGNED
        }

        params: dict = {
            "symbol": req.symbol.upper(),
            "origClientOrderId": req.orderid
        }

        self.add_request(
            method="DELETE",
            path="/api/v3/order",
            callback=self.on_cancel_order,
            params=params,
            data=data,
            on_failed=self.on_cancel_order_failed,
        )

    def query_history(self, req: HistoryRequest) -> List[BarData]:
        """query historical kline data"""
        history: List[BarData] = []
        limit: int = 1500
        start_time: int = int(datetime.timestamp(req.start))

        while True:
            # query parameters
            params: dict = {
                "symbol": req.symbol.upper(),
                "interval": INTERVAL_VT2BINANCE[req.interval],
                "limit": limit,
                "startTime": start_time * 1000,  # convert the start time into milliseconds
            }

            if req.end:
                end_time: int = int(datetime.timestamp(req.end))
                params["endTime"] = end_time * 1000  # convert the start time into milliseconds

            resp: Response = self.request(
                "GET",
                "/api/v3/klines",
                data={"security": Security.NONE},
                params=params
            )

            # continue to query the data until failed
            if resp.status_code // 100 != 2:
                msg: str = f"查询历史kline数据失败, status code：{resp.status_code}，msg：{resp.text}"
                print(msg)
                break
            else:
                data: dict = resp.json()
                if not data:
                    msg: str = f"历史K线数据为空，开始时间：{start_time}"
                    print(msg)
                    break

                buf: List[BarData] = []

                for row in data:
                    bar: BarData = BarData(
                        symbol=self.gateway.symbolMap[req.symbol],
                        datetime=generate_datetime(row[0]),
                        endTime=generate_datetime(row[6]),
                        interval=req.interval,
                        volume=float(row[5]),
                        turnover=float(row[7]),
                        open_price=float(row[1]),
                        high_price=float(row[2]),
                        low_price=float(row[3]),
                        close_price=float(row[4]),
                        exchange=self.gateway.exchange
                    )
                    buf.append(bar)

                history.extend(buf)

                begin: datetime = buf[0].datetime
                end: datetime = buf[-1].datetime
                msg: str = f"查询历史kline数据成功，{req.symbol} - {req.interval.value}，{begin} - {end}"
                print(msg)

                # if the data len is less than limit, break the while loop
                if len(data) < limit:
                    break

                # update start time
                start_dt = bar.datetime + TIMEDELTA_MAP[req.interval]
                start_time = int(datetime.timestamp(start_dt))

        return history

    def query_depth(self, symbol: str, limit: int, depth_data: DepthData) -> DepthData:
        params: dict = {
            "symbol": symbol,
            "limit": limit
        }

        resp: Response = self.request(
            "GET",
            "/api/v3/depth",
            data={"security": Security.NONE},
            params=params
        )
        if resp.status_code // 100 != 2:
            msg: str = f"查询depth数据失败, status code：{resp.status_code}，msg：{resp.text}"
            print(msg)
        else:
            data: dict = resp.json()

            for bid in data["bids"]:
                bid_data: BidData = BidData(
                    bid_price=bid[0],
                    bid_volume=bid[1]
                )
                depth_data.bid_data.append(bid_data)

            for ask in data["asks"]:
                ask_data: AskData = AskData(
                    ask_price=ask[0],
                    ask_volume=ask[1]
                )
                depth_data.ask_data.append(ask_data)

        return depth_data

    def start_user_stream(self) -> None:
        """post listenKey"""
        data: dict = {
            "security": Security.API_KEY
        }

        self.add_request(
            method="POST",
            path="/api/v3/userDataStream",
            callback=self.on_start_user_stream,
            on_failed=self.on_start_user_stream_failed,
            on_error=self.on_start_user_stream_error,
            data=data
        )

    def start_cross_stream(self) -> None:
        """post listenKey"""
        data: dict = {
            "security": Security.API_KEY
        }

        self.add_request(
            method="POST",
            path="/sapi/v1/userDataStream",
            callback=self.on_start_cross_stream,
            on_failed=self.on_start_cross_stream_failed,
            on_error=self.on_start_cross_stream_error,
            data=data
        )

    def start_isolated_stream(self) -> None:
        """post listenKey"""
        data: dict = {
            "security": Security.API_KEY
        }

        self.add_request(
            method="POST",
            path="/sapi/v1/userDataStream/isolated",
            callback=self.on_start_isolated_stream,
            on_failed=self.on_start_isolated_stream_failed,
            on_error=self.on_start_isolated_stream_error,
            data=data
        )

    def on_query_spot_contract(self, data: dict, request: Request) -> None:
        for d in data["symbols"]:
            self.gateway.SPOT_SET.add(d['symbol'])

    def on_query_margin_contract(self, data: dict, request: Request) -> None:
        for d in data["symbols"]:
            self.gateway.MARGIN_SET.add(d['symbol'])

    def on_cancel_order(self, data: dict, request: Request) -> None:
        """cancel order callback"""
        key: Tuple[str, str] = (data.get("type"), data.get("timeInForce"))
        order_type: OrderType = ORDERTYPE_BINANCES2VT.get(key, OrderType.LIMIT)

        traded = float(data.get("executedQty", "0"))
        traded_price = float(data.get('avgPrice', '0'))

        price = float(data["price"])
        if price <= 0 < traded_price:
            price = traded_price

        order: OrderData = OrderData(
            orderid=data.get("clientOrderId"),
            symbol=data.get("symbol"),
            price=price,
            volume=float(data.get("origQty")),
            traded=traded,
            traded_price=traded_price,
            type=order_type,
            direction=DIRECTION_BINANCE2VT.get(data.get("side")),
            status=STATUS_BINANCE2VT.get(data.get("status"), Status.CANCELLED),
            datetime=generate_datetime(float(data.get("updateTime", time.time() * 1000))),
        )
        self.gateway.on_order(order)

        # 撤销订单失败回调

    def on_cancel_order_failed(self, status_code: int, request: Request) -> None:
        self.failed_with_timestamp(request)
        orderid = ""
        if request.extra:
            order: OrderData = copy(request.extra)
            orderid = order.orderid
            order.status = Status.REJECTED
            self.gateway.on_order(copy(order))

        msg = f"撤销订单失败, orderid: {orderid}, status code：{status_code}, msg：{request.response.text}"
        print(msg)

    # 发送订单成功回调
    def on_withdraw_coin(self, data: dict, request: Request) -> None:
        pass

    def keep_user_stream(self) -> None:
        """extend listenKey expire time """
        self.keep_alive_count += 1
        if self.keep_alive_count < 300:
            return None
        self.keep_alive_count = 0

        data: dict = {
            "security": Security.API_KEY
        }

        params: dict = {
            "listenKey": self.user_stream_key
        }

        self.add_request(
            method="PUT",
            path="/api/v3/userDataStream",
            callback=self.on_keep_user_stream,
            params=params,
            data=data,
            on_failed=self.on_keep_user_stream_failed,
            on_error=self.on_keep_user_stream_error
        )

    def keep_cross_user_stream(self) -> None:
        """extend listenKey expire time """
        self.keep_cross_alive_count += 1
        if self.keep_cross_alive_count < 300:
            return None
        self.keep_cross_alive_count = 0

        data: dict = {
            "security": Security.API_KEY
        }

        params: dict = {
            "listenKey": self.cross_stream_key
        }

        self.add_request(
            method="PUT",
            path="/sapi/v1/userDataStream",
            callback=self.on_keep_cross_stream,
            params=params,
            data=data,
            on_failed=self.on_keep_cross_stream_failed,
            on_error=self.on_keep_cross_stream_error
        )

    def keep_isolated_user_stream(self) -> None:
        """extend listenKey expire time """
        self.keep_isolated_alive_count += 1
        if self.keep_isolated_alive_count < 300:
            return None
        self.keep_isolated_alive_count = 0

        data: dict = {
            "security": Security.API_KEY
        }

        params: dict = {
            "listenKey": self.isolated_stream_key
        }

        self.add_request(
            method="PUT",
            path="/sapi/v1/userDataStream/isolated",
            callback=self.on_keep_isolated_stream,
            params=params,
            data=data,
            on_failed=self.on_keep_isolated_stream_failed,
            on_error=self.on_keep_isolated_stream_error
        )

    def on_query_time(self, data: dict, request: Request) -> None:
        """query server time callback"""
        local_time = int(time.time() * 1000)
        server_time = int(data["serverTime"])
        self.time_offset = local_time - server_time

    def on_query_time_failed(self, status_code: int, request: Request):
        self.query_time()

    def on_query_time_error(self, exception_type: type, exception_value: Exception, tb, request: Request) -> None:
        self.query_time()

    def on_send_order(self, data: dict, request: Request) -> None:
        """send order callback"""
        print(data)

    def on_send_order_failed(self, status_code: int, request: Request) -> None:
        """send order failed callback"""
        self.failed_with_timestamp(request)
        if request.extra:
            order: OrderData = copy(request.extra)
            order.status = Status.REJECTED
            order.rejected_reason = request.response.text if request.response.text else ""
            self.gateway.on_order(order)

            msg = f"发送订单失败, orderid: {order.orderid}, status code：{status_code}, msg：{request.response.text}"
            print(msg)

    def on_send_order_error(
            self, exception_type: type, exception_value: Exception, tb, request: Request
    ) -> None:
        """send order error callback"""
        if request.extra:
            order: OrderData = copy(request.extra)
            order.status = Status.REJECTED
            order.rejected_reason = "on_send_order_error"
            self.gateway.on_order(order)

        if not issubclass(exception_type, (ConnectionError, SSLError)):
            self.on_error(exception_type, exception_value, tb, request)

    def on_start_user_stream(self, data: dict, request: Request) -> None:
        """query listen key callback, we connect the account ws"""
        self.user_stream_key = data["listenKey"]
        self.keep_alive_count = 0

        url = WEBSOCKET_TRADE_HOST + self.user_stream_key

        self.trade_ws_api.connect(url, self.proxy_host, self.proxy_port)

    def on_start_cross_stream(self, data: dict, request: Request) -> None:
        """query listen key callback, we connect the account ws"""
        self.cross_stream_key = data["listenKey"]
        self.keep_cross_alive_count = 0

        url = WEBSOCKET_TRADE_HOST + self.cross_stream_key

        self.cross_ws_api.connect(url, self.proxy_host, self.proxy_port)

    def on_start_isolated_stream(self, data: dict, request: Request) -> None:
        """query listen key callback, we connect the account ws"""
        self.isolated_stream_key = data["listenKey"]
        self.keep_isolated_alive_count = 0
        url = WEBSOCKET_TRADE_HOST + self.isolated_stream_key
        self.isolated_ws_api.connect(url, self.proxy_host, self.proxy_port)

    def on_start_user_stream_failed(self, status_code: int, request: Request):
        self.failed_with_timestamp(request)
        self.start_user_stream()

    def on_start_cross_stream_failed(self, status_code: int, request: Request):
        self.failed_with_timestamp(request)
        self.start_cross_stream()

    def on_start_isolated_stream_failed(self, status_code: int, request: Request):
        self.failed_with_timestamp(request)
        self.start_isolated_stream()

    def on_start_user_stream_error(self, exception_type: type, exception_value: Exception, tb, request: Request):
        self.start_user_stream()

    def on_start_isolated_stream_error(self, exception_type: type, exception_value: Exception, tb, request: Request):
        self.start_isolated_stream()

    def on_start_cross_stream_error(self, exception_type: type, exception_value: Exception, tb, request: Request):
        self.start_cross_stream()

    def on_keep_user_stream(self, data: dict, request: Request) -> None:
        """extend the listen key expire time"""
        self.keep_alive_failed_count = 0

    def on_keep_cross_stream(self, data: dict, request: Request) -> None:
        """extend the listen key expire time"""
        self.keep_cross_failed_count = 0

    def on_keep_isolated_stream(self, data: dict, request: Request) -> None:
        """extend the listen key expire time"""
        self.keep_isolated_failed_count = 0

    def on_keep_user_stream_failed(self, status_code: int, request: Request):
        self.failed_with_timestamp(request)
        self.keep_alive_failed_count += 1
        if self.keep_alive_failed_count <= 3:
            self.keep_alive_count = 1200000
            self.keep_user_stream()
        else:
            self.keep_alive_failed_count = 0
            self.start_user_stream()

    def on_keep_cross_stream_failed(self, status_code: int, request: Request):
        self.failed_with_timestamp(request)
        self.keep_cross_failed_count += 1
        if self.keep_cross_failed_count <= 3:
            self.keep_cross_alive_count = 1200000
            self.keep_cross_user_stream()
        else:
            self.keep_cross_failed_count = 0
            self.start_cross_stream()

    def on_keep_isolated_stream_failed(self, status_code: int, request: Request):
        self.failed_with_timestamp(request)
        self.keep_isolated_failed_count += 1
        if self.keep_isolated_failed_count <= 3:
            self.keep_isolated_alive_count = 1200000
            self.keep_isolated_user_stream()
        else:
            self.keep_isolated_failed_count = 0
            self.start_isolated_stream()

    def on_keep_user_stream_error(
            self, exception_type: type, exception_value: Exception, tb, request: Request
    ) -> None:
        """put the listen key failed"""

        self.keep_alive_failed_count += 1
        if self.keep_alive_failed_count <= 3:
            self.keep_alive_count = 1200000
            self.keep_user_stream()
        else:
            self.keep_alive_failed_count = 0
            self.start_user_stream()

        if not issubclass(exception_type, TimeoutError):
            self.on_error(exception_type, exception_value, tb, request)

    def on_keep_cross_stream_error(
            self, exception_type: type, exception_value: Exception, tb, request: Request
    ) -> None:
        """put the listen key failed"""

        self.keep_cross_failed_count += 1
        if self.keep_cross_failed_count <= 3:
            self.keep_cross_alive_count = 1200000
            self.keep_cross_user_stream()
        else:
            self.keep_cross_alive_count = 0
            self.start_cross_stream()

        if not issubclass(exception_type, TimeoutError):
            self.on_error(exception_type, exception_value, tb, request)

    def on_keep_isolated_stream_error(
            self, exception_type: type, exception_value: Exception, tb, request: Request
    ) -> None:
        """put the listen key failed"""

        self.keep_isolated_failed_count += 1
        if self.keep_isolated_failed_count <= 3:
            self.keep_isolated_alive_count = 1200000
            self.keep_isolated_user_stream()
        else:
            self.keep_isolated_alive_count = 0
            self.start_isolated_stream()

        if not issubclass(exception_type, TimeoutError):
            self.on_error(exception_type, exception_value, tb, request)

    def failed_with_timestamp(self, request: Request):
        try:
            if request and request.response and request.response.text:
                resp = json.loads(request.response.text)
                if resp.get('code') == -1021:
                    self.query_time()
        except Exception:
            pass


class BinanceSpotTradeWebsocketApi(WebsocketClient):
    """Binance Spot trade ws api"""

    def __init__(self, gateway: BinanceSpotGateway) -> None:
        """init"""
        super().__init__()

        self.gateway: BinanceSpotGateway = gateway
        self.ping_max_num = 4 * 60
        self.ping_count = 0

    def connect(self, url: str, proxy_host: str, proxy_port: int) -> None:
        """connect binance spot trade ws api"""
        self.init(url, proxy_host, proxy_port)
        self.start()

    def ping_pong(self, event: Event):
        if self.ping_count > self.ping_max_num:
            self.send_packet(send_pong=True)
            self.ping_count = 0
        else:
            self.ping_count += 1

    def on_connected(self) -> None:
        """trade ws connected """
        pass

    def on_packet(self, packet: dict) -> None:
        """receive data from ws"""
        if packet["e"] == "executionReport":
            self.on_order(packet)

    def on_exit_loop(self):
        self.gateway.rest_api.start_user_stream()

    def on_order(self, packet: dict) -> None:
        """order update"""
        key: Tuple[str, str] = (packet["o"], packet["f"])   # 订单类型
        order_type: OrderType = ORDERTYPE_BINANCES2VT.get(key, OrderType.LIMIT)
        price = float(packet["p"])  # 订单原始价格

        order: OrderData = OrderData(
            symbol=packet["s"],  # 交易对
            exchange=Exchange.BINANCE,
            orderid=str(packet["c"]),  # 订单id
            type=order_type,
            direction=DIRECTION_BINANCE2VT[packet["S"]],  # 订单方向
            price=price,
            volume=float(packet["q"]),  # 订单原始数量
            traded=float(packet["z"]),  # 订单累计已成交量
            traded_volume=float(packet.get("l", "0")),  # 订单末次成交量
            traded_price=float(packet.get("L", "0")),  # 订单末次成交价格
            status=STATUS_BINANCE2VT.get(packet["X"], Status.NOTTRADED),
            datetime=generate_datetime(packet["E"]),
        )

        self.gateway.on_order(order)


class BinanceCrossTradeWebsocketApi(WebsocketClient):
    """Binance Spot trade ws api"""

    def __init__(self, gateway: BinanceSpotGateway) -> None:
        """init"""
        super().__init__()

        self.gateway: BinanceSpotGateway = gateway
        self.ping_max_num = 4 * 60
        self.ping_count = 0

    def connect(self, url: str, proxy_host: str, proxy_port: int) -> None:
        """connect binance spot trade ws api"""
        self.init(url, proxy_host, proxy_port)
        self.start()

    def ping_pong(self, event: Event):
        if self.ping_count > self.ping_max_num:
            self.send_packet(send_pong=True)
            self.ping_count = 0
        else:
            self.ping_count += 1

    def on_connected(self) -> None:
        """trade ws connected """
        pass

    def on_packet(self, packet: dict) -> None:
        """receive data from ws"""
        if packet["e"] == "executionReport":
            self.on_order(packet)

    def on_exit_loop(self):
        self.gateway.rest_api.start_user_stream()

    def on_order(self, packet: dict) -> None:
        """order update"""
        key: Tuple[str, str] = (packet["o"], packet["f"])   # 订单类型
        order_type: OrderType = ORDERTYPE_BINANCES2VT.get(key, OrderType.LIMIT)
        price = float(packet["p"])  # 订单原始价格

        order: OrderData = OrderData(
            symbol=packet["s"],  # 交易对
            orderid=str(packet["c"]),  # 订单id
            type=order_type,
            direction=DIRECTION_BINANCE2VT[packet["S"]],  # 订单方向
            price=price,
            volume=float(packet["q"]),  # 订单原始数量
            traded=float(packet["z"]),  # 订单累计已成交量
            traded_volume=float(packet.get("l", "0")),  # 订单末次成交量
            traded_price=float(packet.get("L", "0")),  # 订单末次成交价格
            status=STATUS_BINANCE2VT.get(packet["X"], Status.NOTTRADED),
            datetime=generate_datetime(packet["E"]),
        )

        self.gateway.on_order(order)


class BinanceIsolatedTradeWebsocketApi(WebsocketClient):
    """Binance Spot trade ws api"""

    def __init__(self, gateway: BinanceSpotGateway) -> None:
        """init"""
        super().__init__()

        self.gateway: BinanceSpotGateway = gateway
        self.ping_max_num = 4 * 60
        self.ping_count = 0

    def connect(self, url: str, proxy_host: str, proxy_port: int) -> None:
        """connect binance spot trade ws api"""
        self.init(url, proxy_host, proxy_port)
        self.start()

    def ping_pong(self, event: Event):
        if self.ping_count > self.ping_max_num:
            self.send_packet(send_pong=True)
            self.ping_count = 0
        else:
            self.ping_count += 1

    def on_connected(self) -> None:
        """trade ws connected """
        pass

    def on_packet(self, packet: dict) -> None:
        """receive data from ws"""
        if packet["e"] == "executionReport":
            self.on_order(packet)

    def on_exit_loop(self):
        self.gateway.rest_api.start_user_stream()

    def on_order(self, packet: dict) -> None:
        """order update"""
        key: Tuple[str, str] = (packet["o"], packet["f"])   # 订单类型
        order_type: OrderType = ORDERTYPE_BINANCES2VT.get(key, OrderType.LIMIT)
        price = float(packet["p"])  # 订单原始价格

        order: OrderData = OrderData(
            symbol=packet["s"],  # 交易对
            orderid=str(packet["c"]),  # 订单id
            type=order_type,
            direction=DIRECTION_BINANCE2VT[packet["S"]],  # 订单方向
            price=price,
            volume=float(packet["q"]),  # 订单原始数量
            traded=float(packet["z"]),  # 订单累计已成交量
            traded_volume=float(packet.get("l", "0")),  # 订单末次成交量
            traded_price=float(packet.get("L", "0")),  # 订单末次成交价格
            status=STATUS_BINANCE2VT.get(packet["X"], Status.NOTTRADED),
            datetime=generate_datetime(packet["E"]),
        )

        self.gateway.on_order(order)


class BinanceSpotDataWebsocketApi(WebsocketClient):
    """Binance spot market data ws"""

    def __init__(self, gateway: BinanceSpotGateway) -> None:
        """init"""
        super().__init__()

        self.gateway: BinanceSpotGateway = gateway
        self.ticks: Dict[str, TickData] = {}
        self.bars: Dict[str, BarData] = {}
        self.reqid: int = 0

        self.ping_max_num = 4 * 60
        self.ping_count = 0

    def connect(self, proxy_host: str, proxy_port: int):
        """connect market data ws"""
        self.init(WEBSOCKET_DATA_HOST, proxy_host, proxy_port)

        self.start()

    def ping_pong(self, event: Event):
        if self.ping_count > self.ping_max_num:
            self.send_packet(send_pong=True)
            self.ping_count = 0
        else:
            self.ping_count += 1

    def on_connected(self) -> None:
        """data ws connected"""
        channels = []
        for target in self.bars:
            channels.append(target)

        for target in self.ticks:
            channels.append(target)

        if channels:
            req: dict = {
                "method": "SUBSCRIBE",
                "params": channels,
                "id": self.reqid
            }
            self.send_packet(packet=req)

    def subscribe(self, symbol: str, interval: Interval = None) -> None:
        """subscribe data"""
        if interval:
            target = f"{symbol.lower()}@kline_{interval.value}"
            # 订阅 K线 流程
            if target in self.bars:
                return
            self.reqid += 1
            bar: BarData = BarData(
                symbol=symbol,
                datetime=datetime.now(),
                endTime=datetime.now(),
                interval=interval,
                exchange=self.gateway.exchange,
                product=self.gateway.product
            )
            self.bars[target] = bar

        else:
            target = f"{symbol.lower()}@aggTrade"

            # 订阅tick 数据流程
            if symbol in self.ticks:
                return
            self.reqid += 1
            tick: TickData = TickData(
                symbol=symbol,
                datetime=datetime.now(),
                exchange=self.gateway.exchange,
                product=self.gateway.product
            )
            self.ticks[target] = tick

        req: dict = {
            "method": "SUBSCRIBE",
            "params": [target],
            "id": self.reqid
        }
        self.send_packet(packet=req)

    def on_packet(self, packet: dict) -> None:
        """receiving the subscribed data"""
        stream: str = packet.get("stream", None)

        if not stream:
            return

        data: dict = packet["data"]

        symbol, channel = stream.split("@")
        bar: BarData = self.bars.get(stream)
        tick: TickData = self.ticks.get(stream)

        if channel.startswith("kline_"):
            data = data['k']
            if data['x']:
                bar.volume = float(data['v'])
                bar.turnover = float(data['q'])
                bar.open_price = float(data['o'])
                bar.high_price = float(data['h'])
                bar.low_price = float(data['l'])
                bar.close_price = float(data['c'])
                bar.datetime = generate_datetime(float(data['t']))
                bar.endTime = generate_datetime(float(data['T']))
                self.gateway.on_bar(copy(bar))

        elif channel == "aggTrade":
            # tick.volume = float(data['v'])
            # tick.turnover = float(data['q'])
            # tick.open_price = float(data['o'])
            # tick.high_price = float(data['h'])
            # tick.low_price = float(data['l'])
            tick.last_price = float(data['p'])
            tick.datetime = generate_datetime(float(data['T']))

            if tick.last_price:
                tick.localtime = datetime.now()
                self.gateway.on_tick(copy(tick))


def generate_datetime(timestamp: float) -> datetime:
    """generate time"""
    dt: datetime = datetime.fromtimestamp(timestamp / 1000)
    return dt

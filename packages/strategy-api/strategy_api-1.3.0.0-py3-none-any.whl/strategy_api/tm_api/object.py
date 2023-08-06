# tick 数据: 最后的市场交易、订单快照、盘中市场统计
from dataclasses import dataclass
from datetime import datetime

# tick 数据处理
from enum import Enum
from types import TracebackType
from typing import Union, Callable, Type, Any, List

CALLBACK_TYPE = Callable[[Union[dict, list], "Request"], None]
ON_FAILED_TYPE = Callable[[int, "Request"], None]
ON_ERROR_TYPE = Callable[[Type, Exception, TracebackType, "Request"], None]


# ---------------------------------枚举-----------------------------
class DataType(Enum):
    TICK = "tick"
    BAR = "bar"


class Interval(Enum):
    """
    Interval of bar data.

    """
    MINUTE = "1m"
    MINUTE_3 = "3m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"

    HOUR = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"


# 订单状态类型
class Status(Enum):
    """
    Order status.
    """
    SUBMITTING = "SUBMITTING"  # 提交中 status
    NOTTRADED = "NOTTRADED"  # 没有交易 status
    PARTTRADED = "PARTTRADED"  # 部分交易 status
    ALLTRADED = "ALLTRADED"  # 全部交易 status
    CANCELLED = "CANCELLED"  # 撤单 status
    REJECTED = "REJECTED"  # 拒单 status


ACTIVE_STATUSES = set([Status.SUBMITTING, Status.NOTTRADED, Status.PARTTRADED])


# 订单、交易、仓位等的 方向描述
class Direction(Enum):
    LONG = "Long"  # 多
    SHORT = "Short"  # 空


# 订单类型
class OrderType(Enum):
    """
    Order type.
    """
    LIMIT = "LIMIT"  # 限价单
    MARKET = "MARKET"  # 市价单
    STOP_MARKET = "STOP_MARKET"  # 市价止损
    TAKE_PROFIT_MARKET = "TAKE_PROFIT_MARKET"  # 世价止盈
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"  # 限价止损
    STOP_PROFIT_LIMIT = "STOP_PROFIT_LIMIT"  # 限价止盈
    STOP_LOSS_PROFIT = "STOP_LOSS_PROFIT"  # 止盈止损


class PositionSide(Enum):
    ONEWAY = "ONE_WAY"
    TWOWAY = "TWO_WAY"


# 清算：指订单、成交中的描述
class Offset(Enum):
    NONE = ""
    OPEN = "OPEN"  # 开
    CLOSE = "CLOSE"  # 关


# 产品类型
class Product(Enum):
    SPOT = "SPOT"  # 现货
    U_FUTURES = "U_FUTURES"  # 合约
    B_FUTURES = "B_FUTURES"  # 合约


# 交易所名称
class Exchange(Enum):
    BINANCE = "BINANCE"
    OKEX = "OKEX"


class TdMode(Enum):
    CROSS = "cross"  # 全仓
    ISOLATED = "isolated"  # 逐仓


class Dest(Enum):
    INTERNAL = "INTERNAL"  # 内部转帐
    CHAIN = "CHAIN"  # 链上转账


class TransferType(Enum):
    MAIN_UMFUTURE = "MAIN_UMFUTURE"  # 现货钱包转向U本位合约钱包
    MAIN_CMFUTURE = "MAIN_CMFUTURE"  # 现货钱包转向币本位合约钱包
    MAIN_MARGIN = "MAIN_MARGIN"  # 现货钱包转向杠杆全仓钱包
    UMFUTURE_MAIN = "UMFUTURE_MAIN"  # U本位合约钱包转向现货钱包
    UMFUTURE_MARGIN = "UMFUTURE_MARGIN"  # U本位合约钱包转向杠杆全仓钱包
    CMFUTURE_MAIN = "CMFUTURE_MAIN"  # 币本位合约钱包转向现货钱包
    MARGIN_MAIN = "MARGIN_MAIN"  # 杠杆全仓钱包转向现货钱包
    MARGIN_UMFUTURE = "MARGIN_UMFUTURE"  # 杠杆全仓钱包转向U本位合约钱包
    MARGIN_CMFUTURE = "MARGIN_CMFUTURE"  # 杠杆全仓钱包转向币本位合约钱包
    CMFUTURE_MARGIN = "CMFUTURE_MARGIN"  # 币本位合约钱包转向杠杆全仓钱包

    OKE_CAPITAL_TRADE = "OKE_CAPITAL_TRADE"  # OKE 资金账户 向 OKE 交易账户
    OKE_TRADE_CAPITAL = "OKE_TRADE_CAPITAL"  # OKE 交易账户 向 OKE 资金账户


class Chain(Enum):
    TRC20 = "TRC20"
    ERC20 = "ERC20"
    OKC = "OKC"
    BNB_SMART_CHAIN = 'BNB Smart Chain (BEP20)'
    BNB_BEACON_CHAIN = 'BNB Beacon Chain (BEP2)'


# -----------------------------------------------------------

@dataclass
class BarData:
    symbol: str
    datetime: datetime
    endTime: datetime

    interval: Interval = None
    volume: float = 0
    turnover: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0
    exchange: Exchange = None  # 交易所
    product: Product = None


@dataclass
class TickData:
    symbol: str
    datetime: datetime

    volume: float = 0
    turnover: float = 0
    last_price: float = 0
    last_volume: float = 0
    limit_up: float = 0
    limit_down: float = 0

    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    pre_close: float = 0
    localtime: datetime = None
    exchange: Exchange = None  # 交易所
    product: Product = None


@dataclass
class BidData:
    bid_price: float = 0
    bid_volume: float = 0


@dataclass
class AskData:
    ask_price: float = 0
    ask_volume: float = 0


@dataclass
class DepthData:
    symbol: str
    bid_data: List[BidData]
    ask_data: List[AskData]


# order 数据：当前挂单
@dataclass
class OrderData:
    symbol: str
    orderid: str

    type: OrderType = OrderType.LIMIT
    direction: Direction = None
    offset: Offset = Offset.NONE
    tdMode: TdMode = TdMode.CROSS
    ccy: str = ""
    price: float = 0
    volume: float = 0
    traded: float = 0  # 订单累计成交量
    traded_price: float = 0  # 订单末次成交价
    traded_volume: float = 0  # 订单末次成交量
    status: Status = Status.SUBMITTING
    datetime: datetime = datetime.now()
    update_time: datetime = datetime.now()
    reference: str = ""
    rejected_reason: str = ""  # Order Rejected Reason
    exchange: Exchange = None  # 交易所

    # 检查订单是否有效。
    def is_active(self) -> bool:
        return self.status in ACTIVE_STATUSES

    # 创建 一个测序订单请求数据
    def create_cancel_request(self) -> "CancelRequest":
        return CancelRequest(
            orderid=self.orderid, symbol=self.symbol
        )


# 订单请求数据 发送到特定网关以创建新订单
@dataclass
class OrderRequest:
    """
    Request sending to specific gateway for creating a new order.
    """

    symbol: str
    direction: Direction  # 做多做空方向
    type: OrderType  # 订单类型： 限价、市价、市价止盈、止损
    volume: float  # 交易量
    price: float = 0  # 价格
    offset: Offset = Offset.NONE  # 抵消
    reference: str = ""  # 参考
    tdMode: TdMode = TdMode.CROSS  # 交易模式
    ccy: str = ""
    positionSide: PositionSide = PositionSide.ONEWAY
    exchange: Exchange = None  # 交易所

    stop_loss_price: float = 0  # 止损触发价格
    stop_profit_price: float = 0  # 止盈触发价

    def create_order_data(self, orderid: str) -> OrderData:
        order: OrderData = OrderData(
            symbol=self.symbol,
            orderid=orderid,
            type=self.type,
            direction=self.direction,
            offset=self.offset,
            price=self.price,
            volume=self.volume,
            reference=self.reference,
            exchange=self.exchange,
            tdMode=self.tdMode
        )
        return order


# 提币请求数据
@dataclass
class WithDrawData:
    """
    Request sending to specific gateway for creating a new order.
    """

    symbol: str  # 币种
    amount: str  # 数量
    dest: Dest  #
    toAddress: str  # 价格
    fee: str = ""
    chain: Chain = Chain.TRC20
    areaCode: str = None  # 交易所


# 提币请求数据
@dataclass
class TransferRequest:
    """
    Request sending to specific gateway for creating a new order.
    """
    type: TransferType  # 转移类型
    symbol: str  # 币种
    amount: float  # 数量
    fromSymbol: str = ""
    toSymbol: str = ""


@dataclass
class CancelRequest:
    """
    """

    orderid: str
    symbol: str
    exchange: Exchange = None  # 交易所


@dataclass
class TradeData:
    symbol: str
    orderid: str
    tradeid: str = ""
    direction: Direction = None

    offset: Offset = Offset.NONE
    price: float = 0
    volume: float = 0
    datetime: datetime = None
    exchange: Exchange = None  # 交易所


@dataclass
class HistoryRequest:
    symbol: str
    start: datetime
    end: datetime = None
    interval: Interval = None
    exchange: Exchange = None  # 交易所


@dataclass
class ContractData:
    symbol: str  # 简称
    exchange: Exchange  # 交易所
    name: str  # 全称
    product: Product  # 类型
    size: float  # 合约乘数
    pricetick: float  # 下单价格精度
    min_volume: float = float(1)  # 最小下单数量


@dataclass
class PositionData:
    exchange: Exchange  # 交易所
    symbol: str  # 交易对
    volume: float = 0  # 头寸数量, 符号代表多空方向, 正数为多, 负数为空
    price: float = 0  # 开仓均价
    mark_price: float = 0  # 当前标记价格
    liquidation_price: float = 0  # 参考强平价格
    leverage: int = 1  # 当前杠杆倍数
    # marginType: TdMode = TdMode.CROSS  # 逐仓模式或全仓模式
    pnl: float = 0  # 持仓未实现盈亏

#  =============================================================================
#  GNU Lesser General Public License (LGPL)
#
#  Copyright (c) 2022 Qujamlee from www.aztquant.com
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  =============================================================================
import datetime
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class QuoteRegisterAck:
    market_codes: str = None
    ret_code: int = None


@dataclass
class QuoteStockExtra:
    total_bid_qty: int = None  # 委托买入总量(SH, SZ) - 使用QuoteBaseMsg中数量小数位
    total_ask_qty: int = None  # 委托卖出总量(SH, SZ)
    ma_bid_price: float = None  # 加权平均委买价格(SH, SZ) - 使用QuoteBaseMsg中价格小数位
    ma_ask_price: float = None  # 加权平均委卖价格(SH, SZ) - 使用QuoteBaseMsg中价格小数位
    ma_bond_bid_price: float = None  # 债券加权平均委买价格(SH) - 使用QuoteBaseMsg中价格小数位
    ma_bond_ask_price: float = None  # 债券加权平均委卖价格(SH) - 使用QuoteBaseMsg中价格小数位
    yield_to_maturity: float = None  # 债券到期收益率(SH)
    iopv: float = None  # 基金实时参考净值(SH, SZ)
    etf_buy_count: int = None  # ETF申购笔数(SH)
    etf_sell_count: int = None  # ETF赎回笔数(SH)
    etf_buy_qty: int = None  # ETF申购数量(SH)
    etf_buy_money: float = None  # ETF申购金额(SH)
    etf_sell_qty: int = None  # ETF赎回数量(SH)
    etf_sell_money: float = None  # ETF赎回金额(SH)
    total_warrant_exec_qty: int = None  # 权证执行的总数量(SH)
    warrant_lower_price: float = None  # 权证跌停价格（元）(SH)
    warrant_upper_price: float = None  # 权证涨停价格（元）(SH)
    cancel_buy_count: int = None  # 买入撤单笔数(SH)
    cancel_sell_count: int = None  # 卖出撤单笔数(SH)
    cancel_buy_qty: int = None  # 买入撤单数量(SH) - 使用QuoteBaseMsg中数量小数位
    cancel_sell_qty: int = None  # 卖出撤单数量(SH) - 使用QuoteBaseMsg中数量小数位
    cancel_buy_money: float = None  # 买入撤单金额(SH)
    cancel_sell_money: float = None  # 卖出撤单金额(SH)
    total_buy_count: int = None  # 买入总笔数(SH)
    total_sell_count: int = None  # 卖出总笔数(SH)
    duration_after_buy: int = None  # 买入委托成交最大等待时间(SH)
    duration_after_sell: int = None  # 卖出委托成交最大等待时间(SH)
    num_bid_orders: int = None  # 买方委托价位数(SH)
    num_ask_orders: int = None  # 卖方委托价位数(SH)
    pre_iopv: float = None  # 基金T - 1


@dataclass
class QuoteBaseMsg:
    market: str = None  # 市场
    code: str = None  # 合约代码
    security_type: int = None  # 合约类型

    open: float = None  # 开盘价
    high: float = None  # 最高价
    low: float = None  # 最低价
    last: float = None  # 最新价
    pre_close: float = None  # 昨收盘
    close: float = None  # 今收盘

    upper_limit: float = None  # 涨停价
    lower_limit: float = None  # 跌停价

    total_amount: float = None  # 总成交金额（单位元，与交易所一致）
    total_volume: float = None  # 总成交量  （单位股，与交易所一致）
    avg_price: float = None  # 当日均价

    bid_price: Dict[int, float] = None  # 买价 - XTP(十档) - CTP(五档)
    ask_price: Dict[int, float] = None  # 卖价 - XTP(十档)
    bid_volume: Dict[int, float] = None  # 买量 - XTP(十档)
    ask_volume: Dict[int, float] = None  # 卖量 - XTP(十档)

    data_time: datetime.datetime = None  # 时间: YYYYMMDD - HH:MM: SS.sss


@dataclass
class QuoteMsg:
    data_type: int = None
    quote_base_msg: QuoteBaseMsg = None
    extra_data: Any = None


# 预留,暂未使用
# class SecurityExtraData:
#     product_id: str = None
#     product_name: str = None
#     options_type: str = None
#     delivery_year: str = None
#     delivery_month: str = None
#     is_max_margin_side: bool = None
#     open_date: str = None
#     expire_date: str = None
#     multiple: int = None
#     long_margin_ratio: float = None
#     short_margin_ratio: float = None
#     strike_price: float = None
#     max_market_volume: int = None
#     min_market_volume: int = None
#     max_limit_volume: int = None
#     min_limit_volume: int = None

@dataclass
class SecurityStaticInfo:
    market: str = None
    code: str = None
    security_name: str = None
    security_type: int = None
    price_tick: float = None
    buy_qty_unit: int = None
    sell_qty_unit: int = None
    # extra_data = None


@dataclass
class SecurityInfoRsp:
    security_static_info: List[SecurityStaticInfo] = None

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
from typing import List
from dataclasses import dataclass
from .trade_api import PlaceOrder


# 用户注册回复信息
@dataclass
class TradeRegisterInfo:
    strategy_id: str = None
    account: str = None
    passwd: str = None
    acc_status: int = None


# 注册回复信息
@dataclass
class TradeRegisterAck:
    regist_info: TradeRegisterInfo = None
    regist_code: int = None


# 登录信息
@dataclass
class TradeLoginInfo:
    account: str = None
    trading_day: str = None
    exchange_name: str = None
    exchange_time: datetime.datetime = None


@dataclass
class TradeLoginAck:
    login_info: TradeLoginInfo = None
    ret_code: int = None


# 账户资产信息
@dataclass
class AccMargin:
    account: str = None
    total_amount: float = None
    available_amount: float = None
    deposit: float = None
    open_balance: float = None
    trade_frozen_margin: float = None
    position_market_amount: float = None
    total_buy_amount: float = None
    total_buy_fee: float = None
    total_sell_amount: float = None
    total_sell_fee: float = None
    update_time: datetime.datetime = None


# 入金历史信息
@dataclass
class HisDeposit:
    settlement_date: datetime.datetime = None
    account: str = None
    client_ref: str = None
    deposit: float = None


# 历史资金查询回报
@dataclass
class QryHisAccAck:
    acc_margins: List[AccMargin] = None


# 历史入金查询回报
@dataclass
class QryHisDepositAck:
    his_deposits: List[HisDeposit] = None


# 账户入金信息
@dataclass
class AccDepositAck:
    acc_margin: AccMargin = None
    error_code: int = None


# 委托订单执行状态
@dataclass
class OrdStatusMsg:
    order_status: int = None
    traded_qty: int = None
    traded_amount: float = None
    total_fee: float = None
    frozen_margin: float = None
    frozen_price: float = None
    reject_reason: int = None
    report_time: datetime.datetime = None


# 委托订单信息
@dataclass
class OrdReport:
    place_order: PlaceOrder = None
    status_msg: OrdStatusMsg = None


# 委托查询回复信息
@dataclass
class QueryOrdersAck:
    order_reports: List[OrdReport] = None


# 成交回报信息
@dataclass
class TradeReport:
    order_id: str = None
    client_ref: str = None
    account: str = None
    market: str = None
    code: str = None
    traded_id: str = None
    traded_index: int = None
    exec_type: int = None
    traded_qty: int = None
    traded_price: float = None
    fee: float = None
    transact_time: datetime.datetime = None


# 交易明细查询回复信息
@dataclass
class QueryTradesAck:
    trade_reports: List[TradeReport] = None


# 持仓信息
@dataclass
class StockPosition:
    account: str = None
    market: str = None
    code: str = None
    total_qty: int = None
    today_qty: int = None
    open_avg_price: float = None
    surplus_close_qty: int = None
    frozen_qty: int = None


# 持仓查询回复信息
@dataclass
class QueryPositionsAck:
    positions: List[StockPosition] = None


# 撤单拒绝回报
@dataclass
class CancelOrderReject:
    client_ref: str = None
    org_order_id: str = None
    reject_reason: int = None
    report_time: datetime.datetime = None

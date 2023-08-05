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


@dataclass
class RegisterReq:
    strategy_id: str = None
    strategy_check_code: str = None


@dataclass
class LoginReq:
    account: str = None
    passwd: str = None


# ve账户登出请求
@dataclass
class LogoutReq:
    account: str = None


# 账户信息查询请求
# account and passwd | strategy and check_code
# 若查询条件是 strategy_id + check_code，则返回 所有；
# 若查询条件是 account + passwd; 则只返回 account 和 acc_satus
@dataclass
class UserInfoQryReq:
    account: str = None
    passwd: str = None
    strategy_id: str = None
    strategy_check_code: str = None


# 账户入金请求
@dataclass
class AccDepositReq:
    sender_user: str = None
    account: str = None
    client_ref: str = None
    amount: float = None
    sending_time: datetime.datetime = None


# 账户资金信息查询请求
@dataclass
class TradingAccQryReq:
    account: str = None


# 查询订单信息请求
# 除account外，皆可为空；
# client_ref 与 order_id 只填写一个即可, 则不填写market和code
# 查询未结委托，只填写 account 与 unfinished=true
@dataclass
class QueryOrdersReq:
    account: str = None  # 必填
    market: str = None  # 选填
    code: str = None  # 选填
    client_ref: str = None  # 选填,若填则无需填order_id、market和code
    order_id: str = None  # 选填,若填则无需填client_ref、market和code
    unfinished: bool = None  # 选填,若填则为查询未结委托,只需填写account与unfinished=true


# 查询交易信息请求
# 除account外，皆可为空
# trade_id 或 account market code order_id 填写，则无效（不用填写）
@dataclass
class QueryTradesReq:
    account: str = None
    market: str = None
    code: str = None
    order_id: str = None
    trade_id: str = None


# 查询持仓请求
# 除account外，皆可为空
@dataclass
class QueryPositionsReq:
    account: str = None
    market: str = None
    code: str = None


# 查询历史订单记录请求
# market code 可空
@dataclass
class QueryHistoryOrdersReq:
    account: str = None
    market: str = None
    code: str = None
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None


# 查询历史交易记录请求
# market code 可空
@dataclass
class QueryHistoryTradesReq:
    account: str = None
    market: str = None
    code: str = None
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None


@dataclass
class QryHisAccReq:
    account: str = None
    settlement_date: datetime.datetime = None


@dataclass
class QryHisDepositReq:
    account: str = None
    settlement_date: datetime.datetime = None


# 委托订单请求
@dataclass
class PlaceOrder:
    client_ref: str = None
    sender_user: str = None
    account: str = None
    market: str = None
    code: str = None
    order_type: int = None
    business_type: int = None
    order_side: int = None
    effect: int = None
    order_price: float = None
    order_qty: int = None
    order_id: str = None
    discretion_price: float = None
    send_time: datetime.datetime = None


# 撤单请求
@dataclass
class CancelOrder:
    client_ref: str = None
    sender_user: str = None
    account: str = None
    org_order_id: str = None
    send_time: datetime.datetime = None

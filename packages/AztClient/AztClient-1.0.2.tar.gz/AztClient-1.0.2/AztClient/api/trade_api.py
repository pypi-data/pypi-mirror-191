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

from AztClient.src import TradeApiBase
import AztClient.structs as structs
import AztClient.utils as utils
from AztClient.protocols import EnumProto


class AztTradeApi(TradeApiBase):
    def __init__(self):
        super(AztTradeApi, self).__init__()
        self.SetLogger()

    # 登录
    def Login(self, account: str, passwd: str, timeout: float = None):
        login_req = structs.LoginReq(account=account, passwd=passwd)
        login_ret = self._login(login_req, timeout=timeout)
        if login_ret and login_ret.ret_code == EnumProto.KLoginReCode_LoginSucc:
            if not self._confirm_logined(timeout=timeout):
                return None
        return login_ret

    # 登出
    def Logout(self):
        return self._logout(structs.LogoutReq())

    # 查询账户信息
    def QueryAccountInfo(self, strategy_id: str = None, strategy_check_code: str = None, account: str = None,
                         passwd: str = None, sync: bool = False, timeout: float = None):
        if not strategy_id:
            if not account and not passwd:
                raise utils.errors.ArgsError("参数必须填写strategy_id或者account和passwd")
            account_info_req = structs.UserInfoQryReq(account=account, passwd=passwd)
        else:
            if not strategy_check_code:
                strategy_check_code = "reserved_field_strategy_check_code"
            account_info_req = structs.UserInfoQryReq(
                strategy_id=strategy_id,
                strategy_check_code=strategy_check_code
            )
        return self._query_account_info(account_info_req, sync, timeout)

    # 账户入金
    def DepositAsset(self, amount: float, sync: bool = False, timeout: float = None):
        accdeposit_req = structs.AccDepositReq(amount=amount)
        return self._acc_deposit(accdeposit_req, sync, timeout)

    # 查询账户资产信息
    def QueryAsset(self, sync: bool = False, timeout: float = None):
        trade_req = structs.TradingAccQryReq()
        return self._query_asset(trade_req, sync, timeout)

    def QueryHistoryAsset(self, date: datetime.datetime = None, sync: bool = False, timeout: float = None):
        historyasset_req = structs.QryHisAccReq(settlement_date=date)
        return self._query_history_asset(historyasset_req, sync, timeout)

    def QueryHistoryDeposit(self, date: datetime.datetime = None, sync: bool = False, timeout: float = None):
        historydeposit_req = structs.QryHisDepositReq(settlement_date=date)
        return self._query_history_deposit(historydeposit_req, sync, timeout)

    # 查询订单信息
    def QueryOrders(self, market: str = None, code: str = None, client_ref: str = None, order_id: str = None,
                    unfinished: bool = False, sync: bool = False, timeout: float = None):
        order_req = structs.QueryOrdersReq(market=market, code=code, order_id=order_id,
                                           unfinished=unfinished, client_ref=client_ref)
        return self._query_orders(order_req, sync, timeout)

    # 查询交易信息
    def QueryTrades(self, market: str = None, code: str = None, order_id: str = None, trade_id: str = None,
                    sync: bool = False, timeout: float = None):
        trade_req = structs.QueryTradesReq(market=market, code=code, order_id=order_id,
                                           trade_id=trade_id)
        return self._query_trades(trade_req, sync, timeout)

    # 查询持仓信息
    def QueryPositions(self, market: str = None, code: str = None, sync: bool = False, timeout: float = None):
        position_req = structs.QueryPositionsReq(market=market, code=code)
        return self._query_positions(position_req, sync, timeout)

    # 查询历史委托信息
    def QueryHistoryOrders(self, market: str = None, code: str = None, start_time: datetime.datetime = None,
                           end_time: datetime.datetime = None, sync: bool = False, timeout: float = None):
        historyorders_req = structs.QueryHistoryOrdersReq(market=market, code=code,
                                                          start_time=start_time, end_time=end_time)
        return self._query_history_orders(historyorders_req, sync, timeout)

    # 查询历史交易信息
    def QueryHistoryTrades(self, market: str = None, code: str = None, start_time: datetime.datetime = None,
                           end_time: datetime.datetime = None, sync: bool = False, timeout: float = None):
        historytrades_req = structs.QueryHistoryTradesReq(market=market, code=code,
                                                          start_time=start_time, end_time=end_time)
        return self._query_history_trades(historytrades_req, sync, timeout)

    # 查询证券标的信息
    def QuerySecurityInfo(self, market: str = None, code: str = None, timeout: float = None):
        query_req = structs.QrySecurityStaticReq(market=market, code=code)
        return self._query_security_info(query_req, timeout)

    def _insert_order(self, market: str, code: str, order_type: int, order_side: int, effect: int,
                      order_price: float, order_qty: int, discretion_price: float):
        order_req = structs.PlaceOrder(
            market=market,
            code=code,
            order_type=order_type,
            business_type=EnumProto.KBusinessType_NORMAL,
            order_side=order_side,
            effect=effect,
            order_price=order_price,
            order_qty=order_qty,
            discretion_price=discretion_price
        )
        return self._submit_order(order_req)

    # 买入委托
    def Buy(self, market: str, code: str,
            order_qty: int = 100,  # 默认买入1手(100股)
            order_type: int = EnumProto.KOrderType_Market,  # 默认市价委托
            effect: int = EnumProto.KPositionEffect_Open,  # 默认多仓委托,股票委托不用关注
            order_price: float = None,  # 委托限价,适用于限价单,保留两位小数
            discretion_price: float = None  # 市价转限价后委托限价,适用于市价转限价委托,保留两位小数
            ):
        return self._insert_order(market, code, order_type, EnumProto.KOrderDirection_Buy, effect, order_price,
                                  order_qty, discretion_price)

    # 卖出委托
    def Sell(self, market: str, code: str,
             order_qty: int = 100,  # 默认卖出1手(100股)
             order_type: int = EnumProto.KOrderType_Market,  # 默认市价委托
             effect: int = EnumProto.KPositionEffect_Close,  # 默认空仓委托,股票委托不用关注
             order_price: float = None,  # 委托限价,适用于限价单,保留两位小数
             discretion_price: float = None  # 市价转限价后委托限价,适用于市价转限价委托,保留两位小数
             ):
        return self._insert_order(market, code, order_type, EnumProto.KOrderDirection_Sell, effect, order_price,
                                  order_qty, discretion_price)

    # 撤单委托
    def Cancel(self, order_id: str):
        order_req = structs.CancelOrder(org_order_id=order_id)
        return self._cancel_order(order_req)
        # 初始化

    def Start(self, ip: str, port: int, spi=None, timeout: float = None, reconnect: int = None,
              reconnect_ivl: float = None):
        if timeout and not isinstance(timeout, (int, float)):
            return utils.errors.ArgsError("timeout参数必须为None或int/float类型数值,单位为秒")
        if reconnect and not isinstance(reconnect, int):
            return utils.errors.ArgsError("reconnect参数必须为None或int类型数值")
        if reconnect_ivl and not isinstance(reconnect_ivl, (int, float)):
            return utils.errors.ArgsError("reconnect_ivl参数必须为None或int/float类型数值,单位为秒")
        if spi:
            if isinstance(spi, type):
                spi = spi()
            if not getattr(spi, "api", None):
                setattr(spi, "api", self)
        return self._start(ip, port, spi, timeout, reconnect, reconnect_ivl)

    def Stop(self):
        return self._stop()

    def Join(self, wait: float = None):
        self._join(wait=wait)

    def SetLogger(self, logger=None, title="Trade"):
        self._set_logger(logger=logger, title=title)

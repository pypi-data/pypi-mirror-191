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

from AztClient.utils import set_spi_base as _set_spi_base, set_empty_method as _set_empty_method


@_set_spi_base
class AztTradeSpi:

    # 连接中断回报，一旦被调用，则说明客户端与服务端的连接中断了
    @_set_empty_method
    def onError(self, err):
        pass

    # 断线自动重连成功
    @_set_empty_method
    def onReconnected(self):
        pass

    # 账户入金回报，msg为AccDepositAck实例
    @_set_empty_method
    def onDepositAsset(self, msg):
        pass

    # 查询账户信息回报，msg为UserRegisterInfo实例
    @_set_empty_method
    def onQueryAccountInfo(self, msg):
        pass

    # 查询账户资产信息回报，msg为AccMargin实例
    @_set_empty_method
    def onQueryAsset(self, msg):
        pass

    # 查询委托订单信息回报，msg为QueryOrdersAck实例
    @_set_empty_method
    def onQueryOrders(self, msg):
        pass

    # 查询成交信息回报，msg为QueryTradesAck实例
    @_set_empty_method
    def onQueryTrades(self, msg):
        pass

    # 查询持仓信息回报，msg为QueryPositionsAck实例
    @_set_empty_method
    def onQueryPositions(self, msg):
        pass

    # 查询历史委托信息回报，msg为QueryOrdersAck实例
    @_set_empty_method
    def onQueryHistoryOrders(self, msg):
        pass

    # 查询历史成交信息回报，msg为QueryTradesAck实例
    @_set_empty_method
    def onQueryHistoryTrades(self, msg):
        pass

    # 委托执行回报，msg为OrdReport实例
    @_set_empty_method
    def onOrderReport(self, msg):
        pass

    # 委托成交回报，msg为TradeReport实例
    @_set_empty_method
    def onTradeReport(self, msg):
        pass

    # 撤单失败回报，msg为CancelOrderReject实例
    @_set_empty_method
    def onCancelOrderReject(self, msg):
        pass

    # 查询账户历史资产信息回报，msg为QryHisAccAck实例
    @_set_empty_method
    def onQueryHistoryAsset(self, msg):
        pass

    # 查询历史入金信息回报，msg为QryHisDepositAck实例
    @_set_empty_method
    def onQueryHistoryDeposit(self, msg):
        pass

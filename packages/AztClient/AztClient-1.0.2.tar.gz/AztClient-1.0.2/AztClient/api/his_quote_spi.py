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
class AztHisQuoteSpi:
    # 连接中断回报,err为可raise的Exception错误
    @_set_empty_method
    def onError(self, err):
        pass

    # 断线自动重连成功
    @_set_empty_method
    def onReconnected(self):
        pass

    # 查询Tick行情回报,msg为HisQuoteTicksMsg实例
    @_set_empty_method
    def onQueryHisTicks(self, msg):
        pass

    # 查询Bar行情回报,msg为HisQuoteBarsMsg实例
    @_set_empty_method
    def onQueryHisBars(self, msg):
        pass

    # 查询交易日历回报,msg为TradingCalendar实例
    @_set_empty_method
    def onGetTradingCalendar(self, msg):
        pass

    # 查询下个交易日回报,msg为TradingDate实例
    @_set_empty_method
    def onGetNextTradingDate(self, msg):
        pass

    # 查询基本面数据回报,msg为FundamentalsDatas实例
    @_set_empty_method
    def onGetFundamentals(self, msg):
        pass

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
class AztQuoteSpi:
    # 错误回报，err为可rasie的Exception错误
    @_set_empty_method
    def onError(self, err):
        pass

    # 断线自动重连成功
    @_set_empty_method
    def onReconnected(self):
        pass

    # 订阅行情回报，msg为QuoteRegisterRsp实例
    @_set_empty_method
    def onSubscribe(self, msg):
        pass

    # 取消订阅行情回报，msg为QuoteRegisterRsp实例
    @_set_empty_method
    def onUnsubscribe(self, msg):
        pass

    # 查询行情回报
    @_set_empty_method
    def onQueryQuote(self, msg):
        pass

    # 行情推送，msg为StockQuoteData实例
    @_set_empty_method
    def onQuoteData(self, msg):
        pass

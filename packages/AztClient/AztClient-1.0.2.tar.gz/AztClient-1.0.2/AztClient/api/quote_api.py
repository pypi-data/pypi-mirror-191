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

from AztClient.src import QuoteApiBase
import AztClient.structs as structs


class AztQuoteApi(QuoteApiBase):
    def __init__(self):
        super(AztQuoteApi, self).__init__()
        self.SetLogger()

    def Subscribe(self, codes, sync=False, timeout=None):
        if isinstance(codes, (list, tuple)):
            codes = ",".join(codes)
        if not isinstance(codes, str):
            raise TypeError("'codes' must be a string or list/tuple")
        req = structs.QuoteSubscribe(exchange_securitys=codes)
        return self._quote_register(req, sync, timeout)

    def Unsubscribe(self, codes, sync=False, timeout=None):
        if isinstance(codes, (list, tuple)):
            codes = ",".join(codes)
        if not isinstance(codes, str):
            raise TypeError("'codes' must be a string or list/tuple")
        req = structs.QuoteSubscribe(exchange_securitys=codes)
        return self._quote_unregister(req, sync, timeout)

    def QueryQuote(self, codes, sync=False, timeout=None):
        if isinstance(codes, (list, tuple)):
            codes = ",".join(codes)
        if not isinstance(codes, str):
            raise TypeError("'codes' must be a string or list/tuple")
        req = structs.QuoteSubscribe(exchange_securitys=codes)
        return self._quote_query(req, sync, timeout)

    # 查询证券标的信息
    def QuerySecurityInfo(self, codes, timeout: float = None):
        if isinstance(codes, (list, tuple)):
            codes = ",".join(codes)
        query_req = structs.QuoteSubscribe(exchange_securitys=codes)
        return self._query_security_info(query_req, timeout)

    def Start(self, ip: str, port: int, spi=None, timeout=None, reconnect=None, reconnect_ivl=None):
        if spi:
            if isinstance(spi, type):
                spi = spi()
            if not getattr(spi, "api", None):
                setattr(spi, "api", self)
        return self._start(ip, port, spi, timeout, reconnect, reconnect_ivl)

    def Login(self, account: str, passwd: str, timeout: float = None):
        login_req = structs.LoginReq(account=account, passwd=passwd)
        return self._login(login_req, timeout)

    def Logout(self):
        return self._logout(structs.LogoutReq())

    def Stop(self):
        return self._stop()

    def Join(self, wait: float = None):
        self._join(wait=wait)

    def SetLogger(self, logger=None, title="Quote"):
        self._set_logger(logger=logger, title=title)

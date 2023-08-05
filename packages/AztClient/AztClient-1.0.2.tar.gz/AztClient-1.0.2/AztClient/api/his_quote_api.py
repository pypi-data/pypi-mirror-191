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
from AztClient.src import HisQuoteApiBase
import AztClient.structs as structs
from AztClient.protocols import EnumProto


class AztHisQuoteApi(HisQuoteApiBase):

    def __init__(self):
        super(AztHisQuoteApi, self).__init__()
        self.SetLogger()

    def Login(self, account: str, passwd: str, timeout: float = None):
        return self._login(structs.HisQuoteLogin(account=account, passwd=passwd), timeout)

    def Logout(self):
        return self._logout(structs.HisQuoteLogout())

    def GetTradingCalendar(self, market: str, year: int = None, sync: bool = False, timeout: float = None):
        get_req = structs.GetCalendar(market=market, calendar_year=year)
        return self._get_trading_calendar(get_req, sync, timeout)

    def GetNextTradingDate(self, market: str, trading_date: datetime.datetime, direction: bool = True,
                           sync: bool = False, timeout: float = None):
        if trading_date.weekday() in [5, 6]:
            return structs.TradingDate(market=market)

        get_req = structs.TradingDate(market=market, trading_date=trading_date)
        if direction:
            return self._get_next_trading_date(get_req, sync, timeout)
        return self._get_prev_trading_date(get_req, sync, timeout)

    def QueryHisTicks(self, market: str, code: str, start_time: datetime.datetime, end_time: datetime.datetime,
                      num: int = None, adjust: int = None, adjust_time: datetime.datetime = None, sync: bool = False,
                      timeout: float = None):
        query_req = structs.QueryHisTicks(market=market, code=code, start_time=start_time,
                                          end_time=end_time, limit_number=num, adjust=adjust,
                                          adjust_end_time=adjust_time)
        if num is None:
            return self._query_his_ticks(query_req, sync, timeout)
        elif num <= 0 or num >= 24000:
            raise ValueError("The range of parameter 'num' must be (0,24000).")
        else:
            return self._query_limit_num_his_ticks(query_req, sync, timeout)

    def QueryHisBars(self, market: str, code: str, period: int, start_time: datetime.datetime,
                     end_time: datetime.datetime,
                     num: int = None, adjust: int = None, adjust_time: datetime.datetime = None, sync: bool = False,
                     timeout: float = None):
        if period == EnumProto.KPeriod_DAILY:
            end_time += datetime.timedelta(days=1)
        query_req = structs.QueryHisBars(market=market, code=code, period=period, start_time=start_time,
                                         end_time=end_time, limit_number=num,
                                         adjust=adjust, adjust_end_time=adjust_time)

        if num is None:
            return self._query_his_bars(query_req, sync, timeout)
        elif num <= 0 or num >= 24000:
            raise ValueError("The range of parameter 'num' must be (0,24000).")
        else:
            ret = self._query_limit_num_his_bars(query_req, sync, timeout)
            if ret:
                ret.his_quote_bars.sort(key=lambda x: x.eob)
            return ret

    def GetFundamentals(self, fundamentals_type: int, market: str, code: str, start_date: datetime.datetime = None,
                        end_date: datetime.datetime = None, fileds=None, sync: bool = False, timeout: float = None):
        get_req = structs.GetFundamentalsReq(fundamentals_type=fundamentals_type, market=market, code=code,
                                             start_date=start_date, end_date=end_date)

        return self._get_fundamentals(get_req, fileds, sync, timeout)

    def Start(self, ip: str, port: int, spi=None, timeout=None, reconnect=None, reconnect_ivl=None):
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

    def SetLogger(self, logger=None, title="HisQuote"):
        self._set_logger(logger=logger, title=title)

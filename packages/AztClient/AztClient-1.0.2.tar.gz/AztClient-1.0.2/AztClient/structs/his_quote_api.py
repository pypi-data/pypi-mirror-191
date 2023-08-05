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
class HisQuoteLogin:
    account: str = None
    passwd: str = None


@dataclass
class HisQuoteLogout:
    account: str = None


@dataclass
class QueryHisTicks:
    market: str = None
    code: str = None
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None
    limit_number: int = None
    adjust: int = None
    adjust_end_time: datetime.datetime = None


@dataclass
class QueryHisBars:
    market: str = None
    code: str = None
    period: int = None
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None
    limit_number: int = None
    adjust: int = None
    adjust_end_time: datetime.datetime = None


@dataclass
class GetCalendar:
    market: str = None
    calendar_year: int = None


@dataclass
class TradingDate:
    market: str = None
    trading_date: datetime.datetime = None


@dataclass
class GetFundamentalsReq:
    fundamentals_type: int = None
    market: str = None
    code: str = None
    start_date: datetime.datetime = None
    end_date: datetime.datetime = None

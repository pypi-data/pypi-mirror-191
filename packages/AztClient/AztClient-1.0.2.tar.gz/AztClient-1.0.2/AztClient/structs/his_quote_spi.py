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
import pandas as pd
from typing import List
from dataclasses import dataclass
from .quote_spi import QuoteMsg


@dataclass
class HisQuoteLoginRsp:
    error_code: int = None
    error_msg: str = None


@dataclass
class HisQuoteStockTicksMsg:
    his_quote_ticks: List[QuoteMsg] = None


@dataclass
class HisQuoteBar:
    bob: datetime.datetime = None
    eob: datetime.datetime = None
    market: str = None
    code: str = None
    period: int = None
    open: float = None
    close: float = None
    high: float = None
    low: float = None
    settle: float = None
    total_amount: float = None
    total_volume: int = None
    total_positon: int = None


@dataclass
class HisQuoteBarsMsg:
    his_quote_bars: List[HisQuoteBar] = None


@dataclass
class Calendar:
    market: str = None
    calendar: List[datetime.datetime] = None


@dataclass
class TradingCalendar:
    calendars: List[Calendar] = None


class TradingDerivativeDatas:
    pass


class BalanceSheetDatas:
    pass


class CashFlowDatas:
    pass


class IncomeStatementDatas:
    pass


class PrimFinanceDatas:
    pass


class DerivFinanceDatas:
    pass


@dataclass
class FundamentalsDatas:
    fundamentals_type: int = None
    market: str = None
    code: str = None
    datas: pd.DataFrame = None

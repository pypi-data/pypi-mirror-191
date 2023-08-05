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

from .quote_api import *
from .quote_spi import *
from .trade_api import *
from .trade_spi import *
from .his_quote_api import *
from .his_quote_spi import *

from ..protocols import MsgProto, EnumProto

from . import py2pb as _pyb
from .py2pb import ToProto, ToPyobj

# =======================================================================================
# = QuoteApi
# =======================================================================================
# QuoteSubscribe
_pyb.RegisterConvertor(protobuf=MsgProto.Quote_QuoteSymbolsMsg).Register(QuoteSubscribe)

# QrySecurityStaticReq
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_QrySecurityStaticReq).Register(QrySecurityStaticReq)

# =======================================================================================
# = QuoteSpi
# =======================================================================================
# QuoteRegisterAck
_pyb.RegisterConvertor(protobuf=MsgProto.Quote_QuoteSubscribeUnAck).SetPyHandles(
    _pyb.PyEnumReprHandle(ret_code=EnumProto.EQuoteRetCode)
).Register(QuoteRegisterAck)

# QuoteStockExtra
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("price_decimal_place", normal_attrs=(
        "ma_bid_price", "ma_ask_price", "ma_bond_bid_price", "ma_bond_ask_price", "iopv", "warrant_lower_price",
        "warrant_upper_price"
    )),
    _pyb.DecimalConfigurator("amount_decimal_place", normal_attrs=(
        "yield_to_maturity", "etf_buy_money", "etf_sell_money", "cancel_buy_money", "cancel_sell_money"
    )),
    protobuf=MsgProto.Quote_QuoteStockExtra,
).Register(QuoteStockExtra)

# QuoteBaseMsg
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("price_decimal_place", normal_attrs=(
        "open", "high", "low", "last", "pre_close", "close", "upper_limit", "lower_limit", "avg_price"
    ), map_attrs=("bid_price", "ask_price")),
    _pyb.DecimalConfigurator("amount_decimal_place", normal_attrs=("total_amount",)),
    _pyb.MapConfigurator("bid_volume", "ask_volume"),
    _pyb.CopyConfigurator("total_volume").SetCfgHandle(_pyb.MapConfigHandle(total_volume="last_volume")),
    _pyb.DatetimeConfigurator(data_time="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Quote_QuoteBaseMsg,
).SetPyHandles(
    _pyb.PyEnumReprHandle(security_type=EnumProto.ESecurityType)
).Register(QuoteBaseMsg)

# QuoteMsg
_pyb.RegisterConvertor(
    _pyb.spec_configurator.AztQuoteMsgConfigurator(),
    protobuf=MsgProto.Quote_QuoteMsg,
).SetAutoAttrs(False).SetPyHandles(
    _pyb.PyEnumReprHandle(data_type=EnumProto.EMarketDataType)
).Register(QuoteMsg)

# SecurityStaticInfo
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("price_decimal_place", normal_attrs=("price_tick",)),
    protobuf=MsgProto.Quote_SecurityStaticInfo,
).SetPyHandles(
    _pyb.PyEnumReprHandle(security_type=EnumProto.ESecurityType)
).Register(SecurityStaticInfo)

# SecurityInfoRsp
_pyb.RegisterConvertor(
    _pyb.RepeatConfigurator("security_static_info", recur=True),
    protobuf=MsgProto.Quote_SecurityInfoRsp,
).Register(SecurityInfoRsp)

# =======================================================================================
# = TradeApi
# =======================================================================================
# RegisterReq
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_RegisterReq).Register(RegisterReq)

# LoginReq
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_LoginReq).Register(LoginReq)

# LogoutReq
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_LogoutReq).Register(LogoutReq)

# UserInfoQryReq
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_UserInfoQryReq).Register(UserInfoQryReq)

# AccDepositReq
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("amount_decimal_place", normal_attrs=("amount",)),
    _pyb.DatetimeConfigurator(sending_time="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_AccDepositReq,
).Register(AccDepositReq)

# TradingAccQryReq
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_TradingAccQryReq).Register(TradingAccQryReq)

# QueryOrdersReq
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_QueryOrdersReq).Register(QueryOrdersReq)

# QueryTradesReq
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_QueryTradesReq).Register(QueryTradesReq)

# QueryPositionsReq
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_QueryPositionsReq).Register(QueryPositionsReq)

# QueryHistoryOrdersReq
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(start_time="%Y%m%d-%H:%M:%S.%f", end_time="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_QueryHistoryOrdersReq,
).Register(QueryHistoryOrdersReq)

# QueryHistoryTradesReq
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(start_time="%Y%m%d-%H:%M:%S.%f", end_time="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_QueryHistoryTradesReq,
).Register(QueryHistoryTradesReq)

# QryHisAccReq
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(settlement_date="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_QryHisAccReq,
).Register(QryHisAccReq)

# QryHisDepositReq
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(settlement_date="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_QryHisDepositReq,
).Register(QryHisDepositReq)

# PlaceOrder
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("price_decimal_place", normal_attrs=("order_price", "discretion_price")),
    _pyb.DatetimeConfigurator(send_time="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_PlaceOrder,
).SetAutoAttrs(True, _pyb.spec_handle.Azt_PlaceOrder_effect_handle()).SetPyHandles(
    _pyb.PyEnumReprHandle(
        order_type=EnumProto.EOrderType,
        business_type=EnumProto.EBusinessType,
        order_side=EnumProto.EOrderSide,
        effect=EnumProto.EPositionEffect)
).Register(PlaceOrder)

# CancelOrder
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(send_time="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_CancelOrder,
).Register(CancelOrder)

# =======================================================================================
# = TradeSpi
# =======================================================================================
# TradeRegisterInfo
_pyb.RegisterConvertor(protobuf=MsgProto.Trade_UserRegisterInfo).SetPyHandles(
    _pyb.PyEnumReprHandle(acc_status=EnumProto.EAccStatus)
).Register(TradeRegisterInfo)

# TradeRegisterAck
_pyb.RegisterConvertor(
    _pyb.CopyConfigurator("regist_info", recur=True).SetCfgHandle(
        _pyb.MapConfigHandle(regist_info="registe_info")),
    protobuf=MsgProto.Trade_RegisterAck,
).SetPyHandles(
    _pyb.PyEnumReprHandle(regist_code=EnumProto.ERegisterRet)
).Register(TradeRegisterAck)

# TradeLoginInfo
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(exchange_time="%Y%m%d%H%M%S"),
    protobuf=MsgProto.Trade_LoginInfo,
).Register(TradeLoginInfo)

# TradeLoginAck
_pyb.RegisterConvertor(
    _pyb.CopyConfigurator("login_info", recur=True),
    protobuf=MsgProto.Trade_LoginAck,
).SetPyHandles(
    _pyb.PyEnumReprHandle(ret_code=EnumProto.ELoginRetCode)
).Register(TradeLoginAck)

# AccMargin
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("amount_decimal_place", normal_attrs=(
        "total_amount", "available_amount", "deposit", "open_balance", "trade_frozen_margin",
        "position_market_amount", "total_buy_amount", "total_buy_fee", "total_sell_amount",
        "total_sell_fee")),
    _pyb.DatetimeConfigurator(update_time="%Y%m%d"),
    protobuf=MsgProto.Trade_AccMargin,
).Register(AccMargin)

# HisDeposit
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("amount_decimal_place", normal_attrs=("deposit",)),
    _pyb.DatetimeConfigurator(settlement_date="%Y%m%d", deposit_time="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_HisDeposit,
).Register(HisDeposit)

# QryHisAccAck
_pyb.RegisterConvertor(
    _pyb.RepeatConfigurator("acc_margins", recur=True),
    protobuf=MsgProto.Trade_QryHisAccAck,
).Register(QryHisAccAck)

# QryHisDepositAck
_pyb.RegisterConvertor(
    _pyb.RepeatConfigurator("his_deposits", recur=True),
    protobuf=MsgProto.Trade_QryHisDepositAck,
).Register(QryHisDepositAck)

# AccDepositAck
_pyb.RegisterConvertor(
    _pyb.CopyConfigurator("acc_margin", recur=True),
    protobuf=MsgProto.Trade_AccDepositAck,
).SetPyHandles(
    _pyb.PyEnumReprHandle(error_code=EnumProto.EDepositRetCode)
).Register(AccDepositAck)

# OrdStatusMsg
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("price_decimal_place",
                             normal_attrs=("traded_amount", "total_fee", "frozen_margin", "frozen_price")),
    # _pyb.DatetimeConfigurator(report_time="%Y%m%d-%H:%M:%S.%f"),
    _pyb.MultiDatetimeConfigurator(report_time=("%Y%m%d-%H:%M:%S.%f", "%Y%m%d-%H%M%S.%f")),
    protobuf=MsgProto.Trade_OrdStatusMsg
).SetPyHandles(
    _pyb.PyEnumReprHandle(order_status=EnumProto.EOrderStatus, reject_reason=EnumProto.EOrderRejectReason)
).Register(OrdStatusMsg)

# OrdReport
_pyb.RegisterConvertor(
    _pyb.CopyConfigurator("place_order", "status_msg", recur=True),
    protobuf=MsgProto.Trade_OrdReport,
).Register(OrdReport)

# QueryOrdersAck
_pyb.RegisterConvertor(
    _pyb.RepeatConfigurator("order_reports", recur=True),
    protobuf=MsgProto.Trade_QueryOrdersAck,
).Register(QueryOrdersAck)

# TradeReport
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("price_decimal_place", normal_attrs=("traded_price", "fee")),
    _pyb.DatetimeConfigurator(transact_time="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_TradeReport,
).SetPyHandles(
    _pyb.PyEnumReprHandle(exec_type=EnumProto.EExecType)
).Register(TradeReport)

# QueryTradesAck
_pyb.RegisterConvertor(
    _pyb.RepeatConfigurator("trade_reports", recur=True),
    protobuf=MsgProto.Trade_QueryTradesAck,
).Register(QueryTradesAck)

# StockPosition
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("price_decimal_place", normal_attrs=("open_avg_price",)),
    protobuf=MsgProto.Trade_StokPosition,
).Register(StockPosition)

# QueryPositionsAck
_pyb.RegisterConvertor(
    _pyb.RepeatConfigurator("positions", recur=True),
    protobuf=MsgProto.Trade_QueryPositionsAck,
).Register(QueryPositionsAck)

# CancelOrderReject
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(report_time="%Y%m%d-%H:%M:%S.%f"),
    protobuf=MsgProto.Trade_CancelOrderReject,
).SetPyHandles(
    _pyb.PyEnumReprHandle(reject_reason=EnumProto.ECxRejReasonType)
).Register(CancelOrderReject)

# =======================================================================================
# = HisQuoteApi
# =======================================================================================
# HisQuoteLogin
_pyb.RegisterConvertor(protobuf=MsgProto.His_Quote_ReqLogin).Register(HisQuoteLogin)

# HisQuoteLogout
_pyb.RegisterConvertor(protobuf=MsgProto.His_Quote_ReqLogout).Register(HisQuoteLogout)

# QueryHisTicks
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(start_time="%Y%m%d %H:%M:%S", end_time="%Y%m%d %H:%M:%S",
                              adjust_end_time="%Y%m%d %H:%M:%S"),
    protobuf=MsgProto.His_Quote_QueryHisTicks,
).SetPyHandles(
    _pyb.PyEnumReprHandle(adjust=EnumProto.EAdjust)
).Register(QueryHisTicks)

# QueryHisBars
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(start_time="%Y%m%d %H:%M:%S", end_time="%Y%m%d %H:%M:%S",
                              adjust_end_time="%Y%m%d %H:%M:%S"),
    protobuf=MsgProto.His_Quote_QueryHisBars,
).SetPyHandles(
    _pyb.PyEnumReprHandle(adjust=EnumProto.EAdjust)
).Register(QueryHisBars)

# GetCalendar
_pyb.RegisterConvertor(protobuf=MsgProto.His_Quote_GetCalendar).Register(GetCalendar)

# TradingDate
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(trading_date="%Y%m%d"),
    protobuf=MsgProto.His_Quote_TradingDate,
).Register(TradingDate)

# GetFundamentalsReq
_pyb.RegisterConvertor(
    _pyb.DatetimeConfigurator(start_date="%Y%m%d", end_date="%Y%m%d"),
    protobuf=MsgProto.His_Quote_GetFundamentalsReq,
).SetPyHandles(
    _pyb.PyEnumReprHandle(fundamentals_type=EnumProto.EFundamentalsType)
).Register(GetFundamentalsReq)

# =======================================================================================
# = HisQuoteSpi
# =======================================================================================
# HisQuoteLoginRsp
_pyb.RegisterConvertor(protobuf=MsgProto.His_Quote_RspLogin).SetPyHandles(
    _pyb.PyEnumReprHandle(error_code=EnumProto.EHisQuoteErrCode)
).Register(HisQuoteLoginRsp)

# HisQuoteStockTicksMsg
_pyb.RegisterConvertor(
    _pyb.RepeatConfigurator("his_quote_ticks", recur=True),
    protobuf=MsgProto.His_Quote_HisTicksMsg,
).Register(HisQuoteStockTicksMsg)

# HisQuoteBar
_pyb.RegisterConvertor(
    _pyb.DecimalConfigurator("price_decimal_place", normal_attrs=("open", "close", "high", "low", "settle")),
    _pyb.DecimalConfigurator("amount_decimal_place", normal_attrs=("total_amount",)),
    _pyb.DatetimeConfigurator(bob=None, eob=None),  # timestamp
    _pyb.CopyConfigurator("total_volume").SetCfgHandle(_pyb.MapConfigHandle(total_volume="last_volume")),
    protobuf=MsgProto.His_Quote_HisQuoteBar,
).SetPyHandles(
    _pyb.PyEnumReprHandle(period=EnumProto.EPeriod)
).Register(HisQuoteBar)

# HisQuoteBarsMsg
_pyb.RegisterConvertor(
    _pyb.RepeatConfigurator("his_quote_bars", recur=True),
    protobuf=MsgProto.His_Quote_HisBarsMsg,
).Register(HisQuoteBarsMsg)

# Calendar
_pyb.RegisterConvertor(
    _pyb.spec_configurator.AztCalendarConfigurator(),
    protobuf=MsgProto.His_Quote_Calendar,
).SetAutoAttrs(False).Register(Calendar)

# TradingCalendar
_pyb.RegisterConvertor(
    _pyb.RepeatConfigurator("calendars", recur=True),
    protobuf=MsgProto.His_Quote_TradingCalendar,
).SetAutoAttrs(False).Register(TradingCalendar)

# TradingDerivativeDatas
_pyb.RegisterConvertor(
    _pyb.spec_configurator.AztFundamentalDataConfigurator(
        MsgProto.His_Quote_StockTradingDerivative, "trading_derivative_datas", ("pub_date",)),
    protobuf=MsgProto.His_Quote_TradingDerivativeDatas,
).SetAutoAttrs(False).Register(TradingDerivativeDatas)

# BalanceSheetDatas
_pyb.RegisterConvertor(
    _pyb.spec_configurator.AztFundamentalDataConfigurator(
        MsgProto.His_Quote_BalanceSheet, "balance_sheet_datas", ("pub_date",)),
    protobuf=MsgProto.His_Quote_BalanceSheetDatas,
).SetAutoAttrs(False).Register(BalanceSheetDatas)

# CashFlowDatas
_pyb.RegisterConvertor(
    _pyb.spec_configurator.AztFundamentalDataConfigurator(
        MsgProto.His_Quote_CashFlow, "cash_flow_datas", ("pub_date",)),
    protobuf=MsgProto.His_Quote_CashFlowDatas,
).SetAutoAttrs(False).Register(CashFlowDatas)

# IncomeStatementDatas
_pyb.RegisterConvertor(
    _pyb.spec_configurator.AztFundamentalDataConfigurator(
        MsgProto.His_Quote_IncomeStatement, "income_datas", ("pub_date",)),
    protobuf=MsgProto.His_Quote_IncomeStatementDatas,
).SetAutoAttrs(False).Register(IncomeStatementDatas)

# PrimFinanceDatas
_pyb.RegisterConvertor(
    _pyb.spec_configurator.AztFundamentalDataConfigurator(
        MsgProto.His_Quote_PrimFinance, "prim_finance_datas", ("pub_date",)),
    protobuf=MsgProto.His_Quote_PrimFinanceDatas,
).SetAutoAttrs(False).Register(PrimFinanceDatas)

# DerivFinanceDatas
_pyb.RegisterConvertor(
    _pyb.spec_configurator.AztFundamentalDataConfigurator(
        MsgProto.His_Quote_DerivFinance, "deriv_finance_datas", ("pub_date",)),
    protobuf=MsgProto.His_Quote_DerivFinanceDatas,
).SetAutoAttrs(False).Register(DerivFinanceDatas)

# FundamentalsDatas
_pyb.RegisterConvertor(
    _pyb.spec_configurator.AztFundamentalConfigurator({
        EnumProto.KFundamentalsType_Prim: MsgProto.His_Quote_PrimFinanceDatas,
        EnumProto.KFundamentalsType_Deriv: MsgProto.His_Quote_DerivFinanceDatas,
        EnumProto.KFundamentalsType_TradingDerivative: MsgProto.His_Quote_TradingDerivativeDatas,
        EnumProto.KFundamentalsType_Income: MsgProto.His_Quote_IncomeStatementDatas,
        EnumProto.KFundamentalsType_Cashflow: MsgProto.His_Quote_CashFlowDatas,
        EnumProto.KFundamentalsType_BalanceSheet: MsgProto.His_Quote_BalanceSheetDatas,
    }),
    protobuf=MsgProto.His_Quote_FundamentalsDatas,
).SetAutoAttrs(False).SetPyHandles(
    _pyb.PyEnumReprHandle(fundamentals_type=EnumProto.EFundamentalsType)
).Register(FundamentalsDatas)

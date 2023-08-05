class EAdjust:
    KAdjust_NONE = 0
    KAdjust_PREV = 1
    KAdjust_POST = 2


class EFundamentalsType:
    KFundamentalsType_Unknown = 0
    KFundamentalsType_TradingDerivative = 1
    KFundamentalsType_BalanceSheet = 2
    KFundamentalsType_Cashflow = 3
    KFundamentalsType_Income = 4
    KFundamentalsType_Prim = 5
    KFundamentalsType_Deriv = 6


class EHisQuoteErrCode:
    KHisQuoteErrCode_Unknown = 0
    KHisQuoteErrCode_LoginSucc = 1
    KHisQuoteErrCode_SystemError = 201100
    KHisQuoteErrCode_ReqTypeUnknown = 201101
    KHisQuoteErrCode_DoNotLogin = 201102
    KHisQuoteErrCode_NotTradeDay = 201103
    KHisQuoteErrCode_NotTradeTime = 201104
    KHisQuoteErrCode_StaffNotExist = 201111
    KHisQuoteErrCode_ErrStaffLoginPasswd = 201112
    KHisQuoteErrCode_ErrStaffLoginSkey = 201113
    KHisQuoteErrCode_StaffLogOutFailed = 201114
    KHisQuoteErrCode_NoPrivilegeAdmin = 201115
    KHisQuoteErrCode_StaffAccountForbidden = 201116


class EHisQuoteFrontMsgID:
    KHisFrontMsgID_Unknown = 0
    KHisFrontMsgID_LoginReq = 1
    KHisFrontMsgID_LoginRsp = 2
    KHisFrontMsgID_QueryHisTicksReq = 3
    KHisFrontMsgID_QueryHisTicksRsp = 4
    KHisFrontMsgID_QueryHisTicksNumReq = 5
    KHisFrontMsgID_QueryHisTicksNumRsp = 6
    KHisFrontMsgID_QueryHisBarsReq = 7
    KHisFrontMsgID_QueryHisBarsRsp = 8
    KHisFrontMsgID_QueryHisBarsNumReq = 9
    KHisFrontMsgID_QueryHisBarsNumRsp = 10
    KHisFrontMsgID_GetFundamentalsReq = 11
    KHisFrontMsgID_GetFundamentalsRsp = 12
    KHisFrontMsgID_GetFundamentalsNumReq = 13
    KHisFrontMsgID_GetFundamentalsNumRsp = 14
    KHisFrontMsgID_GetCalendarReq = 15
    KHisFrontMsgID_GetCalendarRsp = 16
    KHisFrontMsgID_GetPreviousTradingDateReq = 17
    KHisFrontMsgID_GetPreviousTradingDateRsp = 18
    KHisFrontMsgID_GetNextTradingDateReq = 19
    KHisFrontMsgID_GetNextTradingDateRsp = 20
    KHisFrontMsgID_LogoutReq = 23


class EPeriod:
    KPeriod_Unknown = 0
    KPeriod_ONE_MIN = 1
    KPeriod_FIVE_MIN = 2
    KPeriod_FIFTEEN_NMIN = 3
    KPeriod_HALF_HOUR = 4
    KPeriod_ONE_HOUR = 5
    KPeriod_DAILY = 6


KAdjust_NONE = 0
KAdjust_POST = 2
KAdjust_PREV = 1
KFundamentalsType_BalanceSheet = 2
KFundamentalsType_Cashflow = 3
KFundamentalsType_Deriv = 6
KFundamentalsType_Income = 4
KFundamentalsType_Prim = 5
KFundamentalsType_TradingDerivative = 1
KFundamentalsType_Unknown = 0
KHisFrontMsgID_GetCalendarReq = 15
KHisFrontMsgID_GetCalendarRsp = 16
KHisFrontMsgID_GetFundamentalsNumReq = 13
KHisFrontMsgID_GetFundamentalsNumRsp = 14
KHisFrontMsgID_GetFundamentalsReq = 11
KHisFrontMsgID_GetFundamentalsRsp = 12
KHisFrontMsgID_GetNextTradingDateReq = 19
KHisFrontMsgID_GetNextTradingDateRsp = 20
KHisFrontMsgID_GetPreviousTradingDateReq = 17
KHisFrontMsgID_GetPreviousTradingDateRsp = 18
KHisFrontMsgID_LoginReq = 1
KHisFrontMsgID_LoginRsp = 2
KHisFrontMsgID_LogoutReq = 23
KHisFrontMsgID_QueryHisBarsNumReq = 9
KHisFrontMsgID_QueryHisBarsNumRsp = 10
KHisFrontMsgID_QueryHisBarsReq = 7
KHisFrontMsgID_QueryHisBarsRsp = 8
KHisFrontMsgID_QueryHisTicksNumReq = 5
KHisFrontMsgID_QueryHisTicksNumRsp = 6
KHisFrontMsgID_QueryHisTicksReq = 3
KHisFrontMsgID_QueryHisTicksRsp = 4
KHisFrontMsgID_Unknown = 0
KHisQuoteErrCode_DoNotLogin = 201102
KHisQuoteErrCode_ErrStaffLoginPasswd = 201112
KHisQuoteErrCode_ErrStaffLoginSkey = 201113
KHisQuoteErrCode_LoginSucc = 1
KHisQuoteErrCode_NoPrivilegeAdmin = 201115
KHisQuoteErrCode_NotTradeDay = 201103
KHisQuoteErrCode_NotTradeTime = 201104
KHisQuoteErrCode_ReqTypeUnknown = 201101
KHisQuoteErrCode_StaffAccountForbidden = 201116
KHisQuoteErrCode_StaffLogOutFailed = 201114
KHisQuoteErrCode_StaffNotExist = 201111
KHisQuoteErrCode_SystemError = 201100
KHisQuoteErrCode_Unknown = 0
KPeriod_DAILY = 6
KPeriod_FIFTEEN_NMIN = 3
KPeriod_FIVE_MIN = 2
KPeriod_HALF_HOUR = 4
KPeriod_ONE_HOUR = 5
KPeriod_ONE_MIN = 1
KPeriod_Unknown = 0

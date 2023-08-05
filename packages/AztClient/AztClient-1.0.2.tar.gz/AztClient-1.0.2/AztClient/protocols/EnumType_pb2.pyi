class EAccStatus:
    KAccStatus_Unknown = 0
    KAccStatus_Normal = 1
    KAccStatus_WrittenOff = 2
    KAccStatus_Disable = 3


class EBusinessType:
    KBusinessType_Unknown = 0
    KBusinessType_NORMAL = 1


class ECxRejReasonType:
    KCxRejReasonType_TooLateCancel = 0
    KCxRejReasonType_UnknowOrder = 1
    KCxRejReasonType_Broker = 2
    KCxRejReasonType_PendingCancel = 3
    KCxRejReasonType_Duplicate = 6
    KCxRejReasonType_Other = 99


class EDepositRetCode:
    KDepositReCode_Unknown = 0
    KDepositReCode_NoError = 1
    KDepositReCode_NoEnoughCash = 2
    KDepositReCode_CapitalOverrun = 3
    KDepositReCode_IllegalAccount = 4
    KDepositReCode_IllegalPara = 5


class EExecType:
    KExecType_Unknown = 0
    KExecType_New = 1
    KExecType_DoneForDay = 3
    KExecType_Canceled = 4
    KExecType_Replaced = 5
    KExecType_PendingCancel = 6
    KExecType_Stopped = 7
    KExecType_Rejected = 8
    KExecType_Suspended = 9
    KExecType_PendingNew = 65
    KExecType_Calculated = 66
    KExecType_Expired = 67
    KExecType_Restated = 68
    KExecType_PendingReplace = 69
    KExecType_Trade = 70
    KExecType_TradeCorrect = 71
    KExecType_TradeCancel = 72
    KExecType_OrderStatus = 73


class ELoginRetCode:
    KLoginReCode_Unknown = 0
    KLoginReCode_LoginSucc = 1
    KLoginReCode_UnknownAcc = 2
    KLoginReCode_AccUnNormal = 3


class EOrderRejectReason:
    KOrderRejectReason_NoError = 0
    KOrdRejReason_UnknownSymbol = 1
    KOrdRejReason_ExchangeClosed = 2
    KOrdRejReason_OrdExceedsLimit = 3
    KOrdRejReason_TooLateEnter = 4
    KOrdRejReason_UnknowOrd = 5
    KOrdRejReason_DuplicateOrd = 6
    KOrdRejReason_StaleOrd = 8
    KOrdRejReason_InvalidAcc = 10
    KOrdRejReason_UnsupportedOrdChara = 11
    KOrdRejReason_IncorrectQty = 13
    KOrdRejReason_UnknownAcc = 15
    KOrdRejReason_NotEnoughPosition = 16
    KOrdRejReason_QtyNonMultipleBuyUnit = 103
    KOrdRejReason_SecuritiesTrading = 102
    KOrdRejReason_PriceNonMultipleTick = 106
    KOrdRejReason_IllegalEntrustedBusiness = 108
    KOrdRejReason_LackDeposit = 117
    KOrdRejReason_PriceError = 125
    KOrdRejReason_InvalidBusinessCategory = 148
    KOrdRejReason_NonTradingTime = 204
    KOrdRejReason_PriceZero = 219


class EOrderSide:
    KOrderDirection_Unknown = 0
    KOrderDirection_Buy = 49
    KOrderDirection_Sell = 50
    KOrderDirection_Call = 68
    KOrderDirection_Callable = 69
    KOrderDirection_FinancingToBuy = 70
    KOrderDirection_FinancingToSell = 71


class EOrderStatus:
    KOrderStatus_Unknown = 0
    KOrderStatus_New = 1
    KOrderStatus_PartiallyFilled = 2
    KOrderStatus_Filled = 3
    KOrderStatus_DoneForDay = 4
    KOrderStatus_Canceled = 5
    KOrderStatus_PendingCancel = 6
    KOrderStatus_Stopped = 7
    KOrderStatus_Rejected = 8
    KOrderStatus_Suspended = 9
    KOrderStatus_PendingNew = 65
    KOrderStatus_Calculated = 66
    KOrderStatus_Expired = 67
    KOrderStatus_AcceptedForBidding = 68
    KOrderStatus_PendingReplace = 69


class EOrderType:
    KOrderType_Unknown = 0
    KOrderType_Market = 1
    KOrderType_Limit = 2
    KOrderType_Stop = 4
    KOrderType_Best_5_Then_Cancel = 7
    KOrderType_Best_5_Then_Limit = 8
    KOrderType_Immediately_Or_Cancel = 9
    KOrderType_All_Or_Cancel = 10
    KOrderType_Market_Then_Limit = 75
    KOrderType_Best_Of_Party = 85
    KOrderType_Best_Of_Conterparty = 86


class EPositionEffect:
    KPositionEffect_Unknown = 0
    KPositionEffect_Open = 48
    KPositionEffect_Close = 49
    KPositionEffect_ForceClose = 50
    KPositionEffect_CloseToday = 51
    KPositionEffect_CloseYesterday = 52


class ERegisterRet:
    KRegisterRet_Unknown = 0
    KRegisterRet_Success = 1
    KRegisterRet_ReRegister = 2
    KRegisterRet_InvalidStrategy = 3


class ESessionStatus:
    KSessionStatus_UnKnown = 0
    KSessionStatus_Connected = 1
    KSessionStatus_Closed = 2
    KSessionStatus_Disconnected = 3


class ETradeMsgID:
    KTradeReqType_Unknown = 0
    KTradeReqType_PlaceOrder = 1
    KTradeReqType_CancelOrder = 2
    KTradeRspType_OrdStatusReport = 3
    KTradeReqType_ExecReport = 4
    KTradeReqType_RejectCancelReport = 5
    KTradeReqType_AccDepositReq = 21
    KTradeReqType_AccDepositAck = 22
    KTradeReqType_TradingAccQryReq = 23
    KTradeReqType_TradingAccQryAck = 24
    KQueryOrdersReq = 25
    KQueryOrdersAck = 26
    KQueryTradesReq = 29
    KQueryTradesAck = 30
    KQueryPositionsReq = 31
    KQueryPositionsAck = 32
    KQueryHistoryOrdersReq = 33
    KQueryHistoryOrdersAck = 34
    KQueryHistoryTradesReq = 35
    KQueryHistoryTradesAck = 36
    KTradeReqType_QryHisAccReq = 37
    KTradeReqType_QryHisAccAck = 38
    KTradeReqType_QryHisDepositReq = 39
    KTradeReqType_QryHisDepositAck = 40
    KTradeReqType_QrySecurityStaticReq = 41
    KTradeReqType_QrySecurityStaticAck = 42
    KVexchangeMsgID_RegisterReq = 80
    KVexchangeMsgID_RegisterAck = 81
    KVexchangeMsgID_UnRegisterReq = 82
    KVexchangeMsgID_UnRegisterAck = 83
    KVexchangeMsgID_LoginReq = 84
    KVexchangeMsgID_LoginAck = 85
    KVexchangeMsgID_LogoutReq = 86
    KVexchangeMsgID_UserInfoQryReq = 87
    KVexchangeMsgID_UserInfoQryAck = 88
    KVexchangeMsgID_HeartBeatReq = 100
    KVexchangeMsgID_HeartBeatAck = 101
    KVexchangeMsgID_SessionControl = 102


KAccStatus_Disable = 3
KAccStatus_Normal = 1
KAccStatus_Unknown = 0
KAccStatus_WrittenOff = 2
KBusinessType_NORMAL = 1
KBusinessType_Unknown = 0
KCxRejReasonType_Broker = 2
KCxRejReasonType_Duplicate = 6
KCxRejReasonType_Other = 99
KCxRejReasonType_PendingCancel = 3
KCxRejReasonType_TooLateCancel = 0
KCxRejReasonType_UnknowOrder = 1
KDepositReCode_CapitalOverrun = 3
KDepositReCode_IllegalAccount = 4
KDepositReCode_IllegalPara = 5
KDepositReCode_NoEnoughCash = 2
KDepositReCode_NoError = 1
KDepositReCode_Unknown = 0
KExecType_Calculated = 66
KExecType_Canceled = 4
KExecType_DoneForDay = 3
KExecType_Expired = 67
KExecType_New = 1
KExecType_OrderStatus = 73
KExecType_PendingCancel = 6
KExecType_PendingNew = 65
KExecType_PendingReplace = 69
KExecType_Rejected = 8
KExecType_Replaced = 5
KExecType_Restated = 68
KExecType_Stopped = 7
KExecType_Suspended = 9
KExecType_Trade = 70
KExecType_TradeCancel = 72
KExecType_TradeCorrect = 71
KExecType_Unknown = 0
KLoginReCode_AccUnNormal = 3
KLoginReCode_LoginSucc = 1
KLoginReCode_Unknown = 0
KLoginReCode_UnknownAcc = 2
KOrdRejReason_DuplicateOrd = 6
KOrdRejReason_ExchangeClosed = 2
KOrdRejReason_IllegalEntrustedBusiness = 108
KOrdRejReason_IncorrectQty = 13
KOrdRejReason_InvalidAcc = 10
KOrdRejReason_InvalidBusinessCategory = 148
KOrdRejReason_LackDeposit = 117
KOrdRejReason_NonTradingTime = 204
KOrdRejReason_NotEnoughPosition = 16
KOrdRejReason_OrdExceedsLimit = 3
KOrdRejReason_PriceError = 125
KOrdRejReason_PriceNonMultipleTick = 106
KOrdRejReason_PriceZero = 219
KOrdRejReason_QtyNonMultipleBuyUnit = 103
KOrdRejReason_SecuritiesTrading = 102
KOrdRejReason_StaleOrd = 8
KOrdRejReason_TooLateEnter = 4
KOrdRejReason_UnknowOrd = 5
KOrdRejReason_UnknownAcc = 15
KOrdRejReason_UnknownSymbol = 1
KOrdRejReason_UnsupportedOrdChara = 11
KOrderDirection_Buy = 49
KOrderDirection_Call = 68
KOrderDirection_Callable = 69
KOrderDirection_FinancingToBuy = 70
KOrderDirection_FinancingToSell = 71
KOrderDirection_Sell = 50
KOrderDirection_Unknown = 0
KOrderRejectReason_NoError = 0
KOrderStatus_AcceptedForBidding = 68
KOrderStatus_Calculated = 66
KOrderStatus_Canceled = 5
KOrderStatus_DoneForDay = 4
KOrderStatus_Expired = 67
KOrderStatus_Filled = 3
KOrderStatus_New = 1
KOrderStatus_PartiallyFilled = 2
KOrderStatus_PendingCancel = 6
KOrderStatus_PendingNew = 65
KOrderStatus_PendingReplace = 69
KOrderStatus_Rejected = 8
KOrderStatus_Stopped = 7
KOrderStatus_Suspended = 9
KOrderStatus_Unknown = 0
KOrderType_All_Or_Cancel = 10
KOrderType_Best_5_Then_Cancel = 7
KOrderType_Best_5_Then_Limit = 8
KOrderType_Best_Of_Conterparty = 86
KOrderType_Best_Of_Party = 85
KOrderType_Immediately_Or_Cancel = 9
KOrderType_Limit = 2
KOrderType_Market = 1
KOrderType_Market_Then_Limit = 75
KOrderType_Stop = 4
KOrderType_Unknown = 0
KPositionEffect_Close = 49
KPositionEffect_CloseToday = 51
KPositionEffect_CloseYesterday = 52
KPositionEffect_ForceClose = 50
KPositionEffect_Open = 48
KPositionEffect_Unknown = 0
KQueryHistoryOrdersAck = 34
KQueryHistoryOrdersReq = 33
KQueryHistoryTradesAck = 36
KQueryHistoryTradesReq = 35
KQueryOrdersAck = 26
KQueryOrdersReq = 25
KQueryPositionsAck = 32
KQueryPositionsReq = 31
KQueryTradesAck = 30
KQueryTradesReq = 29
KRegisterRet_InvalidStrategy = 3
KRegisterRet_ReRegister = 2
KRegisterRet_Success = 1
KRegisterRet_Unknown = 0
KSessionStatus_Closed = 2
KSessionStatus_Connected = 1
KSessionStatus_Disconnected = 3
KSessionStatus_UnKnown = 0
KTradeReqType_AccDepositAck = 22
KTradeReqType_AccDepositReq = 21
KTradeReqType_CancelOrder = 2
KTradeReqType_ExecReport = 4
KTradeReqType_PlaceOrder = 1
KTradeReqType_QryHisAccAck = 38
KTradeReqType_QryHisAccReq = 37
KTradeReqType_QryHisDepositAck = 40
KTradeReqType_QryHisDepositReq = 39
KTradeReqType_QrySecurityStaticAck = 42
KTradeReqType_QrySecurityStaticReq = 41
KTradeReqType_RejectCancelReport = 5
KTradeReqType_TradingAccQryAck = 24
KTradeReqType_TradingAccQryReq = 23
KTradeReqType_Unknown = 0
KTradeRspType_OrdStatusReport = 3
KVexchangeMsgID_HeartBeatAck = 101
KVexchangeMsgID_HeartBeatReq = 100
KVexchangeMsgID_LoginAck = 85
KVexchangeMsgID_LoginReq = 84
KVexchangeMsgID_LogoutReq = 86
KVexchangeMsgID_RegisterAck = 81
KVexchangeMsgID_RegisterReq = 80
KVexchangeMsgID_SessionControl = 102
KVexchangeMsgID_UnRegisterAck = 83
KVexchangeMsgID_UnRegisterReq = 82
KVexchangeMsgID_UserInfoQryAck = 88
KVexchangeMsgID_UserInfoQryReq = 87

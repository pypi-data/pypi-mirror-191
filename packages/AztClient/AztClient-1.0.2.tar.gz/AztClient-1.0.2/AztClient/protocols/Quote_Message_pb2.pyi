class _MsgProtoBase_Quote_Message_pb2:
    def AskPriceEntry(*args, **kwargs):
        pass

    def AskVolumeEntry(*args, **kwargs):
        pass

    def BidPriceEntry(*args, **kwargs):
        pass

    def BidVolumeEntry(*args, **kwargs):
        pass

    def ByteSize(*args, **kwargs):
        pass

    def Clear(*args, **kwargs):
        pass

    def ClearExtension(*args, **kwargs):
        pass

    def ClearField(*args, **kwargs):
        pass

    def CopyFrom(*args, **kwargs):
        pass

    def DiscardUnknownFields(*args, **kwargs):
        pass

    def FindInitializationErrors(*args, **kwargs):
        pass

    def FromString(*args, **kwargs):
        pass

    def HasExtension(*args, **kwargs):
        pass

    def HasField(*args, **kwargs):
        pass

    def IsInitialized(*args, **kwargs):
        pass

    def ListFields(*args, **kwargs):
        pass

    def MergeFrom(*args, **kwargs):
        pass

    def MergeFromString(*args, **kwargs):
        pass

    def ParseFromString(*args, **kwargs):
        pass

    def RegisterExtension(*args, **kwargs):
        pass

    def SerializePartialToString(*args, **kwargs):
        pass

    def SerializeToString(*args, **kwargs):
        pass

    def SetInParent(*args, **kwargs):
        pass

    def UnknownFields(*args, **kwargs):
        pass

    def WhichOneof(*args, **kwargs):
        pass


class QuoteBaseMsg(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, amount_decimal_place=None, ask_price=None, ask_volume=None, avg_price=None, bid_price=None, bid_volume=None, close=None, code=None, data_time=None, high=None, last=None, last_volume=None, low=None, lower_limit=None, market=None, open=None, pre_close=None, price_decimal_place=None, security_type=None, total_amount=None, upper_limit=None):
        self.amount_decimal_place = amount_decimal_place
        self.ask_price = ask_price
        self.ask_volume = ask_volume
        self.avg_price = avg_price
        self.bid_price = bid_price
        self.bid_volume = bid_volume
        self.close = close
        self.code = code
        self.data_time = data_time
        self.high = high
        self.last = last
        self.last_volume = last_volume
        self.low = low
        self.lower_limit = lower_limit
        self.market = market
        self.open = open
        self.pre_close = pre_close
        self.price_decimal_place = price_decimal_place
        self.security_type = security_type
        self.total_amount = total_amount
        self.upper_limit = upper_limit


class QuoteFutureOptionExtra(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, auction_price=None, auction_qty=None, curr_delta=None, last_enquiry_time=None, pre_delta=None, pre_settle=None, pre_total_positon=None, settle=None, total_positon=None):
        self.auction_price = auction_price
        self.auction_qty = auction_qty
        self.curr_delta = curr_delta
        self.last_enquiry_time = last_enquiry_time
        self.pre_delta = pre_delta
        self.pre_settle = pre_settle
        self.pre_total_positon = pre_total_positon
        self.settle = settle
        self.total_positon = total_positon


class QuoteMsg(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, data_type=None, extra_data=None, quote_base_msg=None):
        self.data_type = data_type
        self.extra_data = extra_data
        self.quote_base_msg = quote_base_msg


class QuoteStockExtra(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, cancel_buy_count=None, cancel_buy_money=None, cancel_buy_qty=None, cancel_sell_count=None, cancel_sell_money=None, cancel_sell_qty=None, duration_after_buy=None, duration_after_sell=None, etf_buy_count=None, etf_buy_money=None, etf_buy_qty=None, etf_sell_count=None, etf_sell_money=None, etf_sell_qty=None, iopv=None, ma_ask_price=None, ma_bid_price=None, ma_bond_ask_price=None, ma_bond_bid_price=None, num_ask_orders=None, num_bid_orders=None, pre_iopv=None, total_ask_qty=None, total_bid_qty=None, total_buy_count=None, total_sell_count=None, total_warrant_exec_qty=None, warrant_lower_price=None, warrant_upper_price=None, yield_to_maturity=None):
        self.cancel_buy_count = cancel_buy_count
        self.cancel_buy_money = cancel_buy_money
        self.cancel_buy_qty = cancel_buy_qty
        self.cancel_sell_count = cancel_sell_count
        self.cancel_sell_money = cancel_sell_money
        self.cancel_sell_qty = cancel_sell_qty
        self.duration_after_buy = duration_after_buy
        self.duration_after_sell = duration_after_sell
        self.etf_buy_count = etf_buy_count
        self.etf_buy_money = etf_buy_money
        self.etf_buy_qty = etf_buy_qty
        self.etf_sell_count = etf_sell_count
        self.etf_sell_money = etf_sell_money
        self.etf_sell_qty = etf_sell_qty
        self.iopv = iopv
        self.ma_ask_price = ma_ask_price
        self.ma_bid_price = ma_bid_price
        self.ma_bond_ask_price = ma_bond_ask_price
        self.ma_bond_bid_price = ma_bond_bid_price
        self.num_ask_orders = num_ask_orders
        self.num_bid_orders = num_bid_orders
        self.pre_iopv = pre_iopv
        self.total_ask_qty = total_ask_qty
        self.total_bid_qty = total_bid_qty
        self.total_buy_count = total_buy_count
        self.total_sell_count = total_sell_count
        self.total_warrant_exec_qty = total_warrant_exec_qty
        self.warrant_lower_price = warrant_lower_price
        self.warrant_upper_price = warrant_upper_price
        self.yield_to_maturity = yield_to_maturity


class QuoteSubscribeUnAck(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, market_codes=None, ret_code=None):
        self.market_codes = market_codes
        self.ret_code = ret_code


class QuoteSymbolsMsg(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, exchange_securitys=None):
        self.exchange_securitys = exchange_securitys


class SecurityExtraData(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, delivery_month=None, delivery_year=None, expire_date=None, is_max_margin_side=None, long_margin_ratio=None, max_limit_volume=None, max_market_volume=None, min_limit_volume=None, min_market_volume=None, multiple=None, open_date=None, options_type=None, product_id=None, product_name=None, ratio_decimal_place=None, short_margin_ratio=None, strike_price=None):
        self.delivery_month = delivery_month
        self.delivery_year = delivery_year
        self.expire_date = expire_date
        self.is_max_margin_side = is_max_margin_side
        self.long_margin_ratio = long_margin_ratio
        self.max_limit_volume = max_limit_volume
        self.max_market_volume = max_market_volume
        self.min_limit_volume = min_limit_volume
        self.min_market_volume = min_market_volume
        self.multiple = multiple
        self.open_date = open_date
        self.options_type = options_type
        self.product_id = product_id
        self.product_name = product_name
        self.ratio_decimal_place = ratio_decimal_place
        self.short_margin_ratio = short_margin_ratio
        self.strike_price = strike_price


class SecurityInfoRsp(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, security_static_info=None):
        self.security_static_info = security_static_info


class SecurityStaticInfo(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, buy_qty_unit=None, code=None, extra_data=None, market=None, price_decimal_place=None, price_tick=None, security_name=None, security_type=None, sell_qty_unit=None):
        self.buy_qty_unit = buy_qty_unit
        self.code = code
        self.extra_data = extra_data
        self.market = market
        self.price_decimal_place = price_decimal_place
        self.price_tick = price_tick
        self.security_name = security_name
        self.security_type = security_type
        self.sell_qty_unit = sell_qty_unit


class TimeStamp(_MsgProtoBase_Quote_Message_pb2):
    def __init__(self, ptime=None):
        self.ptime = ptime


class EMarketDataType:
    KMarketDataType_Unknown = 0
    KMarketDataType_Actual = 1
    KMarketDataType_SOption = 2
    KMarketDataType_Future = 3


class EQuoteMsgID:
    KQuoteMsgID_Unknown = 0
    KQuoteMsgID_Subscribe = 1
    KQuoteMsgID_UnSubscribe = 2
    KQuoteMsgID_QuoteQuery = 3
    KQuoteMsgID_TimeStamp = 4
    KQuoteMsgID_QuoteSnapshot = 5
    KQuoteMsgID_QuerySecurityInfoReq = 6
    KQuoteMsgID_QuerySecurityInfoRsp = 7
    KQuoteMsgID_SubscribeAck = 11
    KQuoteMsgID_UnSubscribeAck = 12
    KQuoteMsgID_QuoteQueryAck = 13


class EQuoteRetCode:
    KQuoteRetCode_Unknown = 0
    KQuoteRetCode_Sucess = 1
    KQuoteRetCode_HasError = 2


class ESecurityType:
    KSecurityType_Unknown = 0
    KSecurityType_Stock = 1
    KSecurityType_Option = 2
    KSecurityType_Fund = 3
    KSecurityType_Index = 4
    KSecurityType_Bond = 5
    KSecurityType_Future = 6
    KSecurityType_FutureOption = 7
    KSecurityType_IndexFuture = 8


KMarketDataType_Actual = 1
KMarketDataType_Future = 3
KMarketDataType_SOption = 2
KMarketDataType_Unknown = 0
KQuoteMsgID_QuerySecurityInfoReq = 6
KQuoteMsgID_QuerySecurityInfoRsp = 7
KQuoteMsgID_QuoteQuery = 3
KQuoteMsgID_QuoteQueryAck = 13
KQuoteMsgID_QuoteSnapshot = 5
KQuoteMsgID_Subscribe = 1
KQuoteMsgID_SubscribeAck = 11
KQuoteMsgID_TimeStamp = 4
KQuoteMsgID_UnSubscribe = 2
KQuoteMsgID_UnSubscribeAck = 12
KQuoteMsgID_Unknown = 0
KQuoteRetCode_HasError = 2
KQuoteRetCode_Sucess = 1
KQuoteRetCode_Unknown = 0
KSecurityType_Bond = 5
KSecurityType_Fund = 3
KSecurityType_Future = 6
KSecurityType_FutureOption = 7
KSecurityType_Index = 4
KSecurityType_IndexFuture = 8
KSecurityType_Option = 2
KSecurityType_Stock = 1
KSecurityType_Unknown = 0

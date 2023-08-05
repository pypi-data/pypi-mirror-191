class _MsgProtoBase_Trade_Message_pb2:
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


class AccDepositAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, acc_margin=None, error_code=None):
        self.acc_margin = acc_margin
        self.error_code = error_code


class AccDepositReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, amount=None, amount_decimal_place=None, client_ref=None, sender_user=None, sending_time=None):
        self.account = account
        self.amount = amount
        self.amount_decimal_place = amount_decimal_place
        self.client_ref = client_ref
        self.sender_user = sender_user
        self.sending_time = sending_time


class AccMargin(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, amount_decimal_place=None, available_amount=None, deposit=None, open_balance=None, position_market_amount=None, total_amount=None, total_buy_amount=None, total_buy_fee=None, total_sell_amount=None, total_sell_fee=None, trade_frozen_margin=None, update_time=None):
        self.account = account
        self.amount_decimal_place = amount_decimal_place
        self.available_amount = available_amount
        self.deposit = deposit
        self.open_balance = open_balance
        self.position_market_amount = position_market_amount
        self.total_amount = total_amount
        self.total_buy_amount = total_buy_amount
        self.total_buy_fee = total_buy_fee
        self.total_sell_amount = total_sell_amount
        self.total_sell_fee = total_sell_fee
        self.trade_frozen_margin = trade_frozen_margin
        self.update_time = update_time


class CancelOrder(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, client_ref=None, org_order_id=None, send_time=None, sender_user=None):
        self.account = account
        self.client_ref = client_ref
        self.org_order_id = org_order_id
        self.send_time = send_time
        self.sender_user = sender_user


class CancelOrderReject(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, client_ref=None, org_order_id=None, reject_reason=None, reject_reason_detail=None, report_time=None):
        self.client_ref = client_ref
        self.org_order_id = org_order_id
        self.reject_reason = reject_reason
        self.reject_reason_detail = reject_reason_detail
        self.report_time = report_time


class HeartBeatAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self):
        pass


class HeartBeatReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, real_time=None):
        self.real_time = real_time


class HisDeposit(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, amount_decimal_place=None, client_ref=None, deposit=None, deposit_time=None, settlement_date=None):
        self.account = account
        self.amount_decimal_place = amount_decimal_place
        self.client_ref = client_ref
        self.deposit = deposit
        self.deposit_time = deposit_time
        self.settlement_date = settlement_date


class LoginAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, login_info=None, ret_code=None):
        self.login_info = login_info
        self.ret_code = ret_code


class LoginInfo(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, exchange_name=None, exchange_time=None, session=None, trading_day=None):
        self.account = account
        self.exchange_name = exchange_name
        self.exchange_time = exchange_time
        self.session = session
        self.trading_day = trading_day


class LoginReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, passwd=None):
        self.account = account
        self.passwd = passwd


class LogoutReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None):
        self.account = account


class OrdReport(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, place_order=None, status_msg=None):
        self.place_order = place_order
        self.status_msg = status_msg


class OrdStatusMsg(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, frozen_margin=None, frozen_price=None, order_status=None, price_decimal_place=None, reject_reason=None, reject_reason_detail=None, report_time=None, total_fee=None, traded_amount=None, traded_qty=None):
        self.frozen_margin = frozen_margin
        self.frozen_price = frozen_price
        self.order_status = order_status
        self.price_decimal_place = price_decimal_place
        self.reject_reason = reject_reason
        self.reject_reason_detail = reject_reason_detail
        self.report_time = report_time
        self.total_fee = total_fee
        self.traded_amount = traded_amount
        self.traded_qty = traded_qty


class PlaceOrder(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, business_type=None, client_ref=None, code=None, discretion_price=None, effect=None, market=None, order_id=None, order_price=None, order_qty=None, order_side=None, order_type=None, price_decimal_place=None, send_time=None, sender_user=None):
        self.account = account
        self.business_type = business_type
        self.client_ref = client_ref
        self.code = code
        self.discretion_price = discretion_price
        self.effect = effect
        self.market = market
        self.order_id = order_id
        self.order_price = order_price
        self.order_qty = order_qty
        self.order_side = order_side
        self.order_type = order_type
        self.price_decimal_place = price_decimal_place
        self.send_time = send_time
        self.sender_user = sender_user


class QryHisAccAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, acc_margins=None):
        self.acc_margins = acc_margins


class QryHisAccReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, settlement_date=None):
        self.account = account
        self.settlement_date = settlement_date


class QryHisDepositAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, his_deposits=None):
        self.his_deposits = his_deposits


class QryHisDepositReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, settlement_date=None):
        self.account = account
        self.settlement_date = settlement_date


class QrySecurityStaticReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, code=None, market=None):
        self.account = account
        self.code = code
        self.market = market


class QueryHistoryOrdersReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, code=None, end_time=None, market=None, start_time=None):
        self.account = account
        self.code = code
        self.end_time = end_time
        self.market = market
        self.start_time = start_time


class QueryHistoryTradesReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, code=None, end_time=None, market=None, start_time=None):
        self.account = account
        self.code = code
        self.end_time = end_time
        self.market = market
        self.start_time = start_time


class QueryOrdersAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, order_reports=None):
        self.order_reports = order_reports


class QueryOrdersReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, client_ref=None, code=None, market=None, order_id=None, unfinished=None):
        self.account = account
        self.client_ref = client_ref
        self.code = code
        self.market = market
        self.order_id = order_id
        self.unfinished = unfinished


class QueryPositionsAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, positions=None):
        self.positions = positions


class QueryPositionsReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, code=None, market=None):
        self.account = account
        self.code = code
        self.market = market


class QueryTradesAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, trade_reports=None):
        self.trade_reports = trade_reports


class QueryTradesReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, code=None, market=None, order_id=None, trade_id=None):
        self.account = account
        self.code = code
        self.market = market
        self.order_id = order_id
        self.trade_id = trade_id


class RegisterAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, regist_code=None, registe_info=None):
        self.regist_code = regist_code
        self.registe_info = registe_info


class RegisterReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, strategy_check_code=None, strategy_id=None):
        self.strategy_check_code = strategy_check_code
        self.strategy_id = strategy_id


class SessionControl(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, session=None, session_status=None):
        self.session = session
        self.session_status = session_status


class StokPosition(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, code=None, frozen_qty=None, market=None, open_avg_price=None, price_decimal_place=None, surplus_close_qty=None, today_qty=None, total_qty=None, update_time=None):
        self.account = account
        self.code = code
        self.frozen_qty = frozen_qty
        self.market = market
        self.open_avg_price = open_avg_price
        self.price_decimal_place = price_decimal_place
        self.surplus_close_qty = surplus_close_qty
        self.today_qty = today_qty
        self.total_qty = total_qty
        self.update_time = update_time


class TradeReport(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, client_ref=None, code=None, exec_type=None, fee=None, market=None, order_id=None, price_decimal_place=None, traded_id=None, traded_index=None, traded_price=None, traded_qty=None, transact_time=None):
        self.account = account
        self.client_ref = client_ref
        self.code = code
        self.exec_type = exec_type
        self.fee = fee
        self.market = market
        self.order_id = order_id
        self.price_decimal_place = price_decimal_place
        self.traded_id = traded_id
        self.traded_index = traded_index
        self.traded_price = traded_price
        self.traded_qty = traded_qty
        self.transact_time = transact_time


class TradingAccQryReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None):
        self.account = account


class UnregisterAck(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, ret_code=None, ret_msg=None):
        self.ret_code = ret_code
        self.ret_msg = ret_msg


class UnregisterReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, strategy_check_code=None, strategy_id=None):
        self.strategy_check_code = strategy_check_code
        self.strategy_id = strategy_id


class UserInfoQryReq(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, account=None, passwd=None, strategy_check_code=None, strategy_id=None):
        self.account = account
        self.passwd = passwd
        self.strategy_check_code = strategy_check_code
        self.strategy_id = strategy_id


class UserRegisterInfo(_MsgProtoBase_Trade_Message_pb2):
    def __init__(self, acc_status=None, account=None, passwd=None, strategy_id=None):
        self.acc_status = acc_status
        self.account = account
        self.passwd = passwd
        self.strategy_id = strategy_id



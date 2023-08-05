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
import threading
import time
import uuid
from typing import Optional
import AztClient.utils as utils
import AztClient.structs as structs
from AztClient.structs import MsgProto, EnumProto

_func_switch = utils.QujamFuncSwitch.set_func_switch

_AllowOrderTimeSHSE_SZSE = (
    datetime.time(9, 30, 0), datetime.time(11, 30, 0),
    datetime.time(13, 0, 0), datetime.time(14, 58, 59),
)


class TradeApiBase(utils.QujamApiObject):
    def __init__(self):
        super(TradeApiBase, self).__init__()
        # 设置zmq
        self.__socket: Optional[utils.QujamSocketZmq, None] = None
        self.__user_info = utils.AztUserInfo()
        # 设置信号
        self._event_logined = threading.Event()
        self._event_connected = threading.Event()
        self._reconnect_timeout = None
        self._first_logined = True
        self.__reconnected_timestamp = False
        # 设置账户标识
        self._sender_user = None
        # 设置switch
        self._switch = utils.QujamFuncSwitch("trade_spi")
        self._switch.set_cls(self)

    def _start(self, ip, port, spi=None, timeout=None, reconnect=None, reconnect_ivl=None):
        # 设置spi
        if spi:
            self._spi = utils.QujamSpiObject(spi)
        # 设置zmq套接字
        self.__socket = utils.QujamSocketZmq()
        self.__socket.set_recv_cb(self.__recv_handle)
        self.__socket.set_err_handle(self.__err_handle)
        self.__socket.set_reconnect_cb(self.__reconnect_handle)
        if reconnect == -1:
            self._reconnect_timeout = None
        elif not reconnect:
            self._reconnect_timeout = None if not reconnect_ivl else reconnect
        else:
            self._reconnect_timeout = reconnect * reconnect_ivl

        err = self.__socket.connect_router(ip, port, timeout, reconnect, reconnect_ivl)
        if err:
            return err
        self.debug(f"已成功连接模拟柜台 - {ip}:{port}")

    def _join(self, wait=None):
        if self.__socket:
            self.__socket.join(wait)

    def _stop(self):
        if self._event_logined.is_set():
            return self._logout(structs.LogoutReq())
        super(TradeApiBase, self)._stop()
        if self.__socket:
            self.__socket.close()
        self._event_connected.clear()

    def isStopped(self):
        return self.__socket is None or self.__socket.is_closed()

    def isFirstLogined(self):
        return self._first_logined

    def isLogined(self):
        return self._event_logined.is_set()

    def _verify_connected(self):
        if not self._event_connected.is_set():
            self.debug("与服务端连接已断开，正在等待重连...")
            self._event_connected.wait(self._reconnect_timeout)

    def _verify_logined(self):
        if not self._event_logined.is_set() and (
                self._first_logined or not self._event_logined.wait(self._reconnect_timeout)):
            self._stop()
            raise utils.errors.NotLoginedError("尚未登录！")

    def _verify_just_reconnected(self):
        if not self.__reconnected_timestamp:
            return False
        if time.time() - self.__reconnected_timestamp < 30:
            return True
        return False

    def _send_unitmsg(self, msg, msg_id, msg_type=EnumProto.KMsgType_Exchange_Req):
        # self.warning(f"发送消息：{msg_type} - {msg_id}\n{msg}")
        unit_msg = MsgProto.UnitedMessage_UnitedMessage(msg_type=msg_type, msg_id=msg_id)
        unit_msg.msg_body.Pack(msg)
        self.__socket.send(unit_msg.SerializeToString())

    def __reconnect_handle(self, reconnect):
        if reconnect is None:
            return  # 不用处理
        elif reconnect == utils.QujamSocketZmq.CONNBROKEN:  # 连接断开
            if self._event_connected.is_set():
                self._event_connected.clear()
            if self._event_logined.is_set():
                self._event_logined.clear()
        elif reconnect == utils.QujamSocketZmq.FIRSTCONN:  # 初次连接
            self._event_connected.set()
        elif reconnect == utils.QujamSocketZmq.RECONNECTED:  # 重连成功
            self.__reconnected_timestamp = time.time()
            if self._first_logined:
                self._event_connected.set()
                return
            login_req = structs.LoginReq(account=self.__user_info.getaccount(),
                                         passwd=self.__user_info.getpasswd())
            self._login(login_req, sync=False)

    # recv handle ----------------------------------------------------------------------------------------------------
    def __recv_handle(self, msg: bytes):
        # self.warning("zmq接收消息:", msg)
        unit_msg = MsgProto.UnitedMessage_UnitedMessage()
        unit_msg.ParseFromString(msg)
        try:
            unit_msg.ParseFromString(msg)
        except MsgProto.DecodeError:
            self.warning("Deserialization failed and data packet loss occurred")
            return
        # logger.debug(f"收到消息：{unit_msg.msg_type} - {unit_msg.msg_id}")
        if unit_msg.msg_type != EnumProto.KMsgType_Exchange_Rsp:
            self.warning(f"Unknow recv msg msg_type: {unit_msg.msg_type}(should be {EnumProto.KMsgType_Exchange_Rsp})")
            return
        try:
            self._switch.get(unit_msg.msg_id)(unit_msg)
        except KeyError:
            self.warning(f"Unknow recv msg msg_id: {unit_msg.msg_id}")
        except Exception as e:
            self.error("error happened in trade recv_handle: ", repr(e))
            raise

    def __err_handle(self, err: Exception):
        return self._spi.handle_reply(err, "onError")

    @_func_switch("trade_spi", EnumProto.KVexchangeMsgID_RegisterAck)
    def _case_register(self, unit_msg):
        msg = MsgProto.Trade_RegisterAck()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, None, EnumProto.KVexchangeMsgID_RegisterAck)

    def _confirm_logined(self, timeout=None):
        account = self.__user_info.getaccount()
        passwd = self.__user_info.getpasswd()
        if not account or not passwd:
            return False
        if self._event_logined.is_set():
            return True
        stgyid = self.__user_info.getstgyid()
        if not stgyid:
            query_user_info = structs.UserInfoQryReq(account=account, passwd=passwd)
            account_info = self._query_account_info(query_user_info, True, timeout)
            if not account_info:
                return False
            stgyid = account_info.strategy_id
            self.__user_info.set(stgyid=stgyid)

        self._sender_user = stgyid
        self._event_logined.set()
        self._first_logined = False
        return True

    @_func_switch("trade_spi", EnumProto.KVexchangeMsgID_LoginAck)
    def _case_login(self, unit_msg):
        msg = MsgProto.Trade_LoginAck()
        if unit_msg.msg_body.Unpack(msg):
            login_msg = structs.ToPyobj(msg)
            self._spi.handle_reply(login_msg, None, EnumProto.KVexchangeMsgID_LoginAck)
            if not self._first_logined:
                if not self._event_logined.is_set():
                    self._event_logined.set()
                if not self._event_connected.is_set():
                    self._event_connected.set()

    @_func_switch("trade_spi", EnumProto.KVexchangeMsgID_UserInfoQryAck)
    def _case_user_info(self, unit_msg):
        msg = MsgProto.Trade_UserRegisterInfo()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryAccountInfo", EnumProto.KVexchangeMsgID_UserInfoQryAck)

    @_func_switch("trade_spi", EnumProto.KTradeReqType_AccDepositAck)
    def _case_acc_deposit(self, unit_msg):
        msg = MsgProto.Trade_AccDepositAck()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onDepositAsset", EnumProto.KTradeReqType_AccDepositAck)

    @_func_switch("trade_spi", EnumProto.KTradeReqType_TradingAccQryAck)
    def _case_qurey_asset(self, unit_msg):
        msg = MsgProto.Trade_AccMargin()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryAsset", EnumProto.KTradeReqType_TradingAccQryAck)

    @_func_switch("trade_spi", EnumProto.KQueryOrdersAck)
    def _case_query_orders(self, unit_msg):
        msg = MsgProto.Trade_QueryOrdersAck()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryOrders", EnumProto.KQueryOrdersAck)

    @_func_switch("trade_spi", EnumProto.KQueryTradesAck)
    def _case_query_trades(self, unit_msg):
        msg = MsgProto.Trade_QueryTradesAck()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryTrades", EnumProto.KQueryTradesAck)

    @_func_switch("trade_spi", EnumProto.KQueryPositionsAck)
    def _case_query_position(self, unit_msg):
        msg = MsgProto.Trade_QueryPositionsAck()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryPositions", EnumProto.KQueryPositionsAck)

    @_func_switch("trade_spi", EnumProto.KQueryHistoryOrdersAck)
    def _case_query_history_orders(self, unit_msg):
        msg = MsgProto.Trade_QueryOrdersAck()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryHistoryOrders", EnumProto.KQueryHistoryOrdersAck)

    @_func_switch("trade_spi", EnumProto.KQueryHistoryTradesAck)
    def _case_query_history_trades(self, unit_msg):
        msg = MsgProto.Trade_QueryTradesAck()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryHistoryTrades", EnumProto.KQueryHistoryTradesAck)

    @_func_switch("trade_spi", EnumProto.KTradeReqType_QryHisAccAck)
    def _case_query_history_asset(self, unit_msg):
        msg = MsgProto.Trade_QryHisAccAck()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryHistoryAsset", EnumProto.KTradeReqType_QryHisAccAck)

    @_func_switch("trade_spi", EnumProto.KTradeReqType_QryHisDepositAck)
    def _case_query_history_deposit(self, unit_msg):
        msg = MsgProto.Trade_QryHisDepositAck()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryHistoryDeposit", EnumProto.KTradeReqType_QryHisDepositAck)

    @_func_switch("trade_spi", EnumProto.KTradeRspType_OrdStatusReport)
    def _case_order_report(self, unit_msg):
        msg = MsgProto.Trade_OrdReport()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onOrderReport")

    @_func_switch("trade_spi", EnumProto.KTradeReqType_ExecReport)
    def _case_trade_report(self, unit_msg):
        msg = MsgProto.Trade_TradeReport()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onTradeReport")

    @_func_switch("trade_spi", EnumProto.KTradeReqType_RejectCancelReport)
    def _case_cancel_order_reject(self, unit_msg):
        msg = MsgProto.Trade_CancelOrderReject()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onCancelOrderReject")

    @_func_switch("trade_spi", EnumProto.KTradeReqType_QrySecurityStaticAck)
    def _case_query_security_info(self, unit_msg):
        msg = MsgProto.Quote_SecurityInfoRsp()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, None, EnumProto.KTradeReqType_QrySecurityStaticAck)

    @_func_switch("trade_spi", EnumProto.KVexchangeMsgID_HeartBeatAck)
    def _case_heart_beat(self, _):
        if not self.__socket:
            return
        self.__socket.keep_heart_beat()

    def _sync_return(self, req, sync=False, timeout=None, sid=None, rid=None, once=False, async_handles=(),
                     sync_handles=(), cover_async=False, cover_sync=False):
        return self._spi.handle_request(rid, self._send_unitmsg, (req, sid), None, once, sync, timeout, async_handles,
                                        sync_handles, cover_async, cover_sync)

    def _register_account(self, req, timeout=None):
        self._verify_connected()
        if self._first_logined and self._verify_just_reconnected() and timeout is not None:
            timeout += 30.0
        return self._sync_return(structs.ToProto(req), True, timeout,
                                 EnumProto.KVexchangeMsgID_RegisterReq, EnumProto.KVexchangeMsgID_RegisterAck)

    # ERegisterRet - 注册完成情况返回码
    # KRegisterRet_Unknown         = 0  # 未知错误
    # KRegisterRet_Success         = 1  # 注册成功
    # KRegisterRet_ReRegister      = 2  # 重复注册
    # KRegisterRet_InvalidStrategy = 3  # 无效或非法 strategy_id

    # ### 2.2.8 RegisterAck - 注册响应
    # | 属性 | 类型 | 说明 |
    # | --- | --- | --- |
    # | regist_info | UserRegisterInfo | 账户注册回复信息 |
    # | regist_code | int | 注册完成情况返回码，具体含义与取值参见枚举常量`ERegisterRet` |

    def _login(self, req: structs.LoginReq, sync=True, timeout=None):
        self.__user_info.set(req.account, req.passwd)
        return self._sync_return(structs.ToProto(req), sync, timeout,
                                 EnumProto.KVexchangeMsgID_LoginReq, EnumProto.KVexchangeMsgID_LoginAck, once=True)

    def _logout(self, req):
        if self._event_logined.is_set():
            req.account = self.__user_info.getaccount()
            self._send_unitmsg(structs.ToProto(req), EnumProto.KVexchangeMsgID_LogoutReq)
            self._event_logined.clear()
        return self._stop()

    def _query_account_info(self, req, sync=False, timeout=None):
        self._verify_connected()
        if self._first_logined and sync and self._verify_just_reconnected() and timeout is not None:
            timeout += 30.0
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KVexchangeMsgID_UserInfoQryReq,
                                 EnumProto.KVexchangeMsgID_UserInfoQryAck)

    def _acc_deposit(self, req, sync=False, timeout=None):
        self._verify_connected()
        if self._first_logined and sync and self._verify_just_reconnected() and timeout is not None:
            timeout += 30.0
        req.account = self.__user_info.getaccount()
        req.client_ref = str(uuid.uuid4())
        req.sender_user = self._sender_user
        # req.sending_time = datetime.datetime.now()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KTradeReqType_AccDepositReq,
                                 EnumProto.KTradeReqType_AccDepositAck)

    def _query_asset(self, req, sync=False, timeout=None):
        self._verify_connected()
        self._verify_logined()
        req.account = self.__user_info.getaccount()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KTradeReqType_TradingAccQryReq,
                                 EnumProto.KTradeReqType_TradingAccQryAck)

    def _query_orders(self, req, sync=False, timeout=None):
        self._verify_connected()
        self._verify_logined()
        req.account = self.__user_info.getaccount()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KQueryOrdersReq,
                                 EnumProto.KQueryOrdersAck)

    def _query_trades(self, req, sync=False, timeout=None):
        self._verify_connected()
        self._verify_logined()
        req.account = self.__user_info.getaccount()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KQueryTradesReq,
                                 EnumProto.KQueryTradesAck)

    def _query_positions(self, req, sync=False, timeout=None):
        self._verify_connected()
        self._verify_logined()
        req.account = self.__user_info.getaccount()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KQueryPositionsReq,
                                 EnumProto.KQueryPositionsAck)

    def _query_history_orders(self, req, sync=False, timeout=None):
        self._verify_connected()
        self._verify_logined()
        req.account = self.__user_info.getaccount()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KQueryHistoryOrdersReq,
                                 EnumProto.KQueryHistoryOrdersAck)

    def _query_history_trades(self, req, sync=False, timeout=None):
        self._verify_connected()
        self._verify_logined()
        req.account = self.__user_info.getaccount()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KQueryHistoryTradesReq,
                                 EnumProto.KQueryHistoryTradesAck)

    def _query_history_asset(self, req, sync=False, timeout=None):
        self._verify_connected()
        self._verify_logined()
        req.account = self.__user_info.getaccount()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KTradeReqType_QryHisAccReq,
                                 EnumProto.KTradeReqType_QryHisAccAck)

    def _query_history_deposit(self, req, sync=False, timeout=None):
        self._verify_connected()
        self._verify_logined()
        req.account = self.__user_info.getaccount()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KTradeReqType_QryHisDepositReq,
                                 EnumProto.KTradeReqType_QryHisDepositAck)

    def _query_security_info(self, req, timeout=None):
        self._verify_connected()
        req.account = "azt@sz"
        return self._sync_return(structs.ToProto(req), True, timeout, EnumProto.KTradeReqType_QrySecurityStaticReq,
                                 EnumProto.KTradeReqType_QrySecurityStaticAck)

    def _submit_order(self, req):
        self._verify_connected()
        self._verify_logined()
        now = datetime.datetime.now()
        now_time = now.time()
        if _AllowOrderTimeSHSE_SZSE[0] <= now_time <= _AllowOrderTimeSHSE_SZSE[1] or \
                _AllowOrderTimeSHSE_SZSE[2] <= now_time <= _AllowOrderTimeSHSE_SZSE[3]:
            req.account = self.__user_info.getaccount()
            req.client_ref = str(uuid.uuid4())
            req.sender_user = self._sender_user
            req.send_time = now
            self._send_unitmsg(structs.ToProto(req), EnumProto.KTradeReqType_PlaceOrder)
            return req
        else:
            raise utils.errors.NonTradingTimeError

    def _cancel_order(self, req):
        self._verify_connected()
        self._verify_logined()
        req.account = self.__user_info.getaccount()
        req.client_ref = str(uuid.uuid4())
        req.sender_user = self._sender_user
        req.send_time = datetime.datetime.now()
        self._send_unitmsg(structs.ToProto(req), EnumProto.KTradeReqType_CancelOrder)
        return req

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
import threading
import AztClient.utils as utils
import AztClient.structs as structs
from AztClient.structs import MsgProto, EnumProto

_func_switch = utils.QujamFuncSwitch.set_func_switch


class QuoteApiBase(utils.QujamApiObject):
    def __init__(self):
        super(QuoteApiBase, self).__init__()
        self.__socket = None
        self.__user_info = utils.AztUserInfo()
        self._event_logined = threading.Event()
        self._first_logined = True
        self._reconnect_timeout = None
        self._switch = utils.QujamFuncSwitch("quote_spi")
        self._switch.set_cls(self)
        self._heart_beat_flag = utils.msg_codec.AztCheckSumCodec.HEARTBEAT
        self._heart_beat_response = utils.msg_codec.AztCheckSumCodec.heartbeat()

    def isLogined(self):
        return self._event_logined.is_set()

    def isFirstLogined(self):
        return self._first_logined

    def isStopped(self):
        return self.__socket is None or self.__socket.is_closed()

    def _start(self, ip, port, spi=None, timeout=None, reconnect=None, reconnect_ivl=None):
        self.__socket = utils.QujamSocket()
        self.__socket.set_tcp_recv_cb(self.__recv_handle)
        self.__socket.set_tcp_err_handle(self.__socket_err_handle)
        self.__socket.set_tcp_msg_codec(utils.msg_codec.AztCheckSumCodec)
        self.__socket.set_tcp_reconnect_handle(self.__reconnect_handle)

        if reconnect == -1:
            self._reconnect_timeout = None
        elif not reconnect:
            self._reconnect_timeout = 0
        else:
            self._reconnect_timeout = reconnect * reconnect_ivl
        error = self.__socket.connect_tcp(ip, port, timeout, reconnect, reconnect_ivl)
        if error:
            return error
        if spi:
            self._spi = utils.QujamSpiObject(spi)
        self.debug(f"已连接行情服务 - {ip}:{port}")

    def _stop(self):
        if self._event_logined.is_set():
            return self._logout(structs.LogoutReq())
        super(QuoteApiBase, self)._stop()
        if self.__socket:
            close_err = self.__socket.close()
            self.__socket = None
            return close_err

    def _join(self, wait=None):
        if self.__socket:
            self.__socket.join(wait)

    def _login(self, req, timeout=None):
        self.__user_info.set(req.account, req.passwd)
        return self._spi.handle_request(EnumProto.KVexchangeMsgID_LoginAck, self._send_unitmsg,
                                        (structs.ToProto(req), EnumProto.KVexchangeMsgID_LoginReq,
                                         EnumProto.KMsgType_Exchange_Req),
                                        None, False, True, timeout)

    def _logout(self, req):
        if self._event_logined.is_set():
            req.account = self.__user_info.getaccount()
            self._send_unitmsg(structs.ToProto(req), EnumProto.KVexchangeMsgID_LogoutReq,
                               EnumProto.KMsgType_Exchange_Req)
            self._event_logined.clear()
        return self._stop()

    def _quote_register(self, req, sync=False, timeout=None):
        self._verify_logined()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KQuoteMsgID_Subscribe,
                                 EnumProto.KQuoteMsgID_SubscribeAck)

    def _quote_unregister(self, req, sync=False, timeout=None):
        self._verify_logined()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KQuoteMsgID_UnSubscribe,
                                 EnumProto.KQuoteMsgID_UnSubscribeAck)

    def _quote_query(self, req, sync=False, timeout=None):
        self._verify_logined()
        securities = req.exchange_securitys.split(",")
        sync_handle = query_quote_sync_handle(securities)
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KQuoteMsgID_QuoteQuery,
                                 EnumProto.KQuoteMsgID_QuoteQueryAck, sync_handles=(sync_handle,), cover_sync=True)

    def _query_security_info(self, req, timeout=None):
        req.account = "azt@sz"
        return self._sync_return(structs.ToProto(req), True, timeout, EnumProto.KQuoteMsgID_QuerySecurityInfoReq,
                                 EnumProto.KQuoteMsgID_QuerySecurityInfoRsp)

    def _send_unitmsg(self, msg, msg_id, msg_type=EnumProto.KMsgType_Quote):
        # self.debug(f"发送消息：{msg_type} - {msg_id}\n{msg}")
        unit_msg = MsgProto.UnitedMessage_UnitedMessage(msg_type=msg_type, msg_id=msg_id)
        unit_msg.msg_body.Pack(msg)
        self.__socket.send_tcp(unit_msg.SerializeToString())

    def _sync_return(self, req, sync=False, timeout=None, sid=None, rid=None, once=False, async_handles=(),
                     sync_handles=(), cover_async=False, cover_sync=False):
        return self._spi.handle_request(rid, self._send_unitmsg, (req, sid), None, once, sync, timeout, async_handles,
                                        sync_handles, cover_async, cover_sync)

    def _verify_logined(self):
        if not self._event_logined.is_set() and (
                self._first_logined or not self._event_logined.wait(self._reconnect_timeout)):
            self._stop()
            raise utils.errors.NotLoginedError("尚未登录！")

    @_func_switch("quote_spi", EnumProto.KVexchangeMsgID_LoginAck)
    def _case_login(self, unitedmsg):
        msg = MsgProto.Trade_LoginAck()
        if unitedmsg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, None, EnumProto.KVexchangeMsgID_LoginAck)
            if not self._event_logined.is_set():
                self._event_logined.set()
            if self._first_logined:
                self._first_logined = False

    @_func_switch("quote_spi", EnumProto.KQuoteMsgID_SubscribeAck)
    def _case_subscribe(self, unitedmsg):
        msg = MsgProto.Quote_QuoteSubscribeUnAck()
        if unitedmsg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onSubscribe", EnumProto.KQuoteMsgID_SubscribeAck)

    @_func_switch("quote_spi", EnumProto.KQuoteMsgID_UnSubscribeAck)
    def _case_unsubscribe(self, unitedmsg):
        msg = MsgProto.Quote_QuoteSubscribeUnAck()
        if unitedmsg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onUnsubscribe", EnumProto.KQuoteMsgID_UnSubscribeAck)

    @_func_switch("quote_spi", EnumProto.KQuoteMsgID_QuoteQueryAck)
    def _case_query_quote(self, unitedmsg):
        msg = MsgProto.Quote_QuoteMsg()
        if unitedmsg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryQuote", EnumProto.KQuoteMsgID_QuoteQueryAck)

    @_func_switch("quote_spi", EnumProto.KQuoteMsgID_QuoteSnapshot)
    def _case_snapshot(self, unitedmsg):
        msg = MsgProto.Quote_QuoteMsg()
        if unitedmsg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQuoteData")

    @_func_switch("quote_spi", EnumProto.KQuoteMsgID_QuerySecurityInfoRsp)
    def _case_query_security_info(self, unitedmsg):
        msg = MsgProto.Quote_SecurityInfoRsp()
        if unitedmsg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, None, EnumProto.KQuoteMsgID_QuerySecurityInfoRsp)

    def __recv_handle(self, msg):
        # self.debug(f"收到msg: {msg}")
        if msg == self._heart_beat_flag:
            self.__socket.send_tcp(self._heart_beat_response)
            return
        unitedmsg = MsgProto.UnitedMessage_UnitedMessage()
        try:
            unitedmsg.ParseFromString(msg)
        except MsgProto.DecodeError:
            self.warning("Deserialization failed and data packet loss occurred")
            return
        msg_type = unitedmsg.msg_type
        if msg_type not in [EnumProto.KMsgType_Quote, EnumProto.KMsgType_Exchange_Rsp]:
            self.warning(f"Unknow recv msg msg_type: {msg_type}"
                         f"(should be {EnumProto.KMsgType_Quote} or {EnumProto.KMsgType_Exchange_Rsp})")
            return
        msg_id = unitedmsg.msg_id
        try:
            self._switch.get(msg_id)(unitedmsg)
        except KeyError:
            self.warning(f"Unknow recv msg msg_id: {msg_id}")
        except Exception as e:
            self.error("error happened in quote recv_handle: ", repr(e))
            raise

    def __socket_err_handle(self, err):
        return self._spi.handle_reply(err, "onError")

    def __reconnect_handle(self):
        if not self._event_logined.is_set():
            return True
        trytimes = 5
        login_req = structs.ToProto(
            structs.LoginReq(account=self.__user_info.getaccount(), passwd=self.__user_info.getpasswd()))
        while trytimes:
            trytimes -= 1
            login_rep = self._spi.handle_request(EnumProto.KVexchangeMsgID_LoginAck, self._send_unitmsg,
                                                 (login_req, EnumProto.KVexchangeMsgID_LoginReq,
                                                  EnumProto.KMsgType_Exchange_Req),
                                                 None, False, True, 6.0)
            if login_rep:
                if login_rep.ret_code != EnumProto.KLoginReCode_LoginSucc:
                    self.error(
                        f"error login ret_code:{login_rep.ret_code}(should be {EnumProto.KLoginReCode_LoginSucc})")
                    break
                self._spi.call("onReconnected")
                return True
        self._event_logined.clear()
        return False


class query_quote_sync_handle:
    def __init__(self, securities):
        self.securities = set(securities)
        self._datas = {}

    def __call__(self, data):
        data_code = f"{data.quote_base_msg.market}.{data.quote_base_msg.code}"
        if data_code in self.securities:
            self.securities.remove(data_code)
            self._datas[data_code] = data
        if not self.securities:
            return self._datas, False
        return None, True

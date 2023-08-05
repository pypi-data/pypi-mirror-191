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


class HisQuoteApiBase(utils.QujamApiObject):
    def __init__(self):
        super(HisQuoteApiBase, self).__init__()
        self.__socket = None
        self.__user_info = utils.AztUserInfo()
        self._event_logined = threading.Event()
        self._first_logined = True
        self._reconnect_timeout = None
        self._switch = utils.QujamFuncSwitch("his_quote_spi")
        self._switch.set_cls(self)
        self._heart_beat_flag = utils.msg_codec.AztCheckSumCodec.HEARTBEAT
        self._heart_beat_response = utils.msg_codec.AztCheckSumCodec.heartbeat()

    def isLogined(self):
        return self._event_logined.is_set()

    def isFirstLogined(self):
        return self._first_logined

    def isStopped(self):
        if self.__socket:
            return self.__socket.is_closed()
        return True

    def _start(self, ip, port, spi=None, timeout=None, reconnect=None, reconnect_ivl=None):
        self.__socket = utils.QujamSocket()

        self.__socket.set_tcp_recv_cb(self.__recv_handle)
        self.__socket.set_tcp_err_handle(self.__socket_err_handle)
        self.__socket.set_tcp_msg_codec(utils.msg_codec.AztCheckSumCodec)
        self.__socket.set_tcp_reconnect_handle(self.__reconnect_handle)

        if reconnect == -1:
            self._reconnect_timeout = None
        elif not reconnect:
            self._reconnect_timeout = None if not reconnect_ivl else reconnect
        else:
            self._reconnect_timeout = reconnect * reconnect_ivl

        err = self.__socket.connect_tcp(ip, port, timeout, reconnect, reconnect_ivl)
        if err:
            return err
        if spi:
            self._spi = utils.QujamSpiObject(spi)
        self.debug(f"已连接历史行情服务 - {ip}:{port}")

    def _stop(self):
        if self._event_logined.is_set():
            return self._logout(structs.HisQuoteLogout())
        super(HisQuoteApiBase, self)._stop()
        if self.__socket:
            close_err = self.__socket.close()
            self.__socket = None
            return close_err

    def _join(self, wait=None):
        if self.__socket:
            self.__socket.join(wait)

    def _login(self, req, timeout=None):
        self.__user_info.set(req.account, req.passwd)
        return self._sync_return(structs.ToProto(req), True, timeout, EnumProto.KHisFrontMsgID_LoginReq,
                                 EnumProto.KHisFrontMsgID_LoginRsp)

    def _logout(self, req):
        if self._event_logined.is_set():
            req.account = self.__user_info.getaccount()
            self._send_unitmsg(structs.ToProto(req), EnumProto.KHisFrontMsgID_LogoutReq)
            self._event_logined.clear()
        return self._stop()

    def _query_his_ticks(self, req, sync=False, timeout=None):
        self._verify_logined()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KHisFrontMsgID_QueryHisTicksReq,
                                 EnumProto.KHisFrontMsgID_QueryHisTicksRsp)

    def _query_limit_num_his_ticks(self, req, sync=False, timeout=None):
        self._verify_logined()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KHisFrontMsgID_QueryHisTicksNumReq,
                                 EnumProto.KHisFrontMsgID_QueryHisTicksNumRsp)

    def _query_his_bars(self, req, sync=False, timeout=None):
        self._verify_logined()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KHisFrontMsgID_QueryHisBarsReq,
                                 EnumProto.KHisFrontMsgID_QueryHisBarsRsp)

    def _query_limit_num_his_bars(self, req, sync=False, timeout=None):
        self._verify_logined()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KHisFrontMsgID_QueryHisBarsNumReq,
                                 EnumProto.KHisFrontMsgID_QueryHisBarsNumRsp)

    def _get_trading_calendar(self, req, sync=False, timeout=None):
        self._verify_logined()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KHisFrontMsgID_GetCalendarReq,
                                 EnumProto.KHisFrontMsgID_GetCalendarRsp)

    def _get_prev_trading_date(self, req, sync=False, timeout=None):
        self._verify_logined()
        return self._sync_return(structs.ToProto(req), sync, timeout,
                                 EnumProto.KHisFrontMsgID_GetPreviousTradingDateReq,
                                 EnumProto.KHisFrontMsgID_GetPreviousTradingDateRsp)

    def _get_next_trading_date(self, req, sync=False, timeout=None):
        self._verify_logined()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KHisFrontMsgID_GetNextTradingDateReq,
                                 EnumProto.KHisFrontMsgID_GetNextTradingDateRsp)

    def _get_fundamentals(self, req, fileds=None, sync=False, timeout=None):
        self._verify_logined()
        async_handles = (lambda x: _handle_fundamentals_data(x, fileds),) if fileds else ()
        return self._sync_return(structs.ToProto(req), sync, timeout, EnumProto.KHisFrontMsgID_GetFundamentalsReq,
                                 EnumProto.KHisFrontMsgID_GetFundamentalsRsp, async_handles=async_handles)

    def _send_unitmsg(self, msg, msg_id, msg_type=EnumProto.KMsgType_FrontQuote):
        # logger.debug(f"发送消息：{msg_type} - {msg_id}\n{msg}")
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

    @_func_switch("his_quote_spi", EnumProto.KHisFrontMsgID_LoginRsp)
    def _case_login(self, unit_msg):
        msg = MsgProto.His_Quote_RspLogin()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, None, EnumProto.KHisFrontMsgID_LoginRsp)
            if not self._event_logined.is_set():
                self._event_logined.set()
            if self._first_logined:
                self._first_logined = False

    @_func_switch("his_quote_spi", EnumProto.KHisFrontMsgID_QueryHisTicksRsp)
    def _case_query_his_ticks(self, unit_msg):
        msg = MsgProto.His_Quote_HisTicksMsg()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryHisTicks", EnumProto.KHisFrontMsgID_QueryHisTicksRsp)

    @_func_switch("his_quote_spi", EnumProto.KHisFrontMsgID_QueryHisTicksNumRsp)
    def _case_query_limit_num_his_ticks(self, unit_msg):
        msg = MsgProto.His_Quote_HisTicksMsg()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryHisTicks", EnumProto.KHisFrontMsgID_QueryHisTicksNumRsp)

    @_func_switch("his_quote_spi", EnumProto.KHisFrontMsgID_QueryHisBarsRsp)
    def _case_query_his_bars(self, unit_msg):
        msg = MsgProto.His_Quote_HisBarsMsg()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryHisBars", EnumProto.KHisFrontMsgID_QueryHisBarsRsp)

    @_func_switch("his_quote_spi", EnumProto.KHisFrontMsgID_QueryHisBarsNumRsp)
    def _case_query_limit_his_bars(self, unit_msg):
        msg = MsgProto.His_Quote_HisBarsMsg()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onQueryHisBars", EnumProto.KHisFrontMsgID_QueryHisBarsNumRsp)

    @_func_switch("his_quote_spi", EnumProto.KHisFrontMsgID_GetCalendarRsp)
    def _case_get_trading_calendar(self, unit_msg):
        msg = MsgProto.His_Quote_TradingCalendar()
        unit_msg.msg_body.Unpack(msg)
        cbmsg = structs.ToPyobj(msg)
        self._spi.handle_reply(cbmsg, "onGetTradingCalendar", EnumProto.KHisFrontMsgID_GetCalendarRsp)

    @_func_switch("his_quote_spi", EnumProto.KHisFrontMsgID_GetPreviousTradingDateRsp)
    def _case_get_prev_trading_calendar(self, unit_msg):
        msg = MsgProto.His_Quote_TradingDate()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onGetNextTradingDate",
                                   EnumProto.KHisFrontMsgID_GetPreviousTradingDateRsp)

    @_func_switch("his_quote_spi", EnumProto.KHisFrontMsgID_GetNextTradingDateRsp)
    def _case_get_next_trading_calendar(self, unit_msg):
        msg = MsgProto.His_Quote_TradingDate()
        if unit_msg.msg_body.Unpack(msg):
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onGetNextTradingDate", EnumProto.KHisFrontMsgID_GetNextTradingDateRsp)

    @_func_switch("his_quote_spi", EnumProto.KHisFrontMsgID_GetFundamentalsRsp)
    def _case_get_fundamentals(self, unit_msg):
        msg = MsgProto.His_Quote_FundamentalsDatas()
        if unit_msg.msg_body.Unpack(msg):
            if msg.fundamentals_type == EnumProto.KFundamentalsType_Unknown:
                return
            cbmsg = structs.ToPyobj(msg)
            self._spi.handle_reply(cbmsg, "onGetFundamentals", EnumProto.KHisFrontMsgID_GetFundamentalsRsp)

    def __recv_handle(self, msg):
        # self.warning(f"收到消息: {msg}")
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
        if msg_type != EnumProto.KMsgType_FrontQuote:
            self.warning(f"Unknow recv msg msg_type: {msg_type}(should be {EnumProto.KMsgType_FrontQuote})")
            return
        msg_id = unitedmsg.msg_id
        try:
            self._switch.get(msg_id)(unitedmsg)
        except KeyError:
            self.warning(f"Unknow recv msg msg_id: {msg_id}")
        except Exception as e:
            self.error("error happened in his_quote recv_handle: ", repr(e))
            raise

    def __socket_err_handle(self, err):
        return self._spi.handle_reply(err, "onError")

    def __reconnect_handle(self):
        if not self._event_logined.is_set():
            return True

        trytimes = 5
        login_req = structs.ToProto(
            structs.HisQuoteLogin(account=self.__user_info.getaccount(), passwd=self.__user_info.getpasswd())
        )
        while trytimes:
            trytimes -= 1
            login_rep = self._spi.handle_request(EnumProto.KHisFrontMsgID_LoginRsp, self._send_unitmsg,
                                                 (login_req, EnumProto.KHisFrontMsgID_LoginReq),
                                                 None, False, True, 6.0)
            if login_rep:
                if login_rep.error_code != EnumProto.KHisQuoteErrCode_LoginSucc:
                    self.error(
                        f"error login ret_code:{login_rep.error_code}(should be {EnumProto.KHisQuoteErrCode_LoginSucc})")
                    break
                self._spi.call("onReconnected")
                return True
        self._event_logined.clear()
        return False


def _handle_fundamentals_data(data, fileds):
    if isinstance(fileds, str):
        fileds = fileds.split(",")
    data_columns = data.data.columns
    fileds = [filed for filed in fileds if filed in data_columns]
    data.datas = data.datas[fileds]
    return data, False

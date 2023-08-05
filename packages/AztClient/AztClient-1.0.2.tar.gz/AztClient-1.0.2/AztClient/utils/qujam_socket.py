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
import queue
import socket
import threading

from . import qujam_errors as errors
from .qujam_buffer import BufferQueue
from .qujam_heart_beat import QujamHeartBeat
from .qujam_msg_codec import DefaultMsgCodec
from .qujam_loop_thread import QujamLoopThread, result_call_back_func, error_handle_func


def reconnect_handle_func():
    return True


class QujamSocket:
    def __init__(self, **kwargs):
        self.p_tcp_recv_buflen = kwargs.get("tcp_recv_buflen", 65536)
        self.p_udp_recv_buflen = kwargs.get("udp_recv_buflen", 2048)
        self.p_trace_exception = kwargs.get("trace_exception", False)
        self.m_tcp_socket = None
        self.m_udp_socket = None

        self.m_tcp_addr = None
        self.m_udp_addr = None
        self.m_event_close = threading.Event()

        self.m_tcp_recv_buffer = BufferQueue()
        self.m_tcp_data_transmit = None
        self.m_udp_data_transmit = None
        self.m_tcp_msg_codec = DefaultMsgCodec()

        self.m_tcp_recv_cb = result_call_back_func
        self.m_udp_recv_cb = result_call_back_func

        self.m_tcp_err_handle = error_handle_func
        self.m_udp_err_handle = error_handle_func

        self.m_loop_thread = QujamLoopThread(self.p_trace_exception)

        self.m_heart_beat = None
        self.m_tcp_reconnect = None  # 重连次数, 0 or None : 默认不重连; -1 : 无限重连; >0 : 重连次数用尽后不再重连
        self.m_tcp_reconn_ivl = 1.0  # 重连间隔,默认1s/次
        self.m_tcp_reconnect_handle = reconnect_handle_func

        self._first_connect = True

    def connect_tcp(self, ip: str, port: int, timeout=None, reconnect: int = None, reconnect_ivl: float = None):
        self.m_tcp_addr = (ip, port)
        self.m_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m_tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if isinstance(reconnect, int):
            self.m_tcp_reconnect = reconnect
        if isinstance(reconnect_ivl, (int, float)):
            self.m_tcp_reconn_ivl = float(reconnect_ivl)

        try:
            self._do_connect_tcp(timeout)
        except TimeoutError:
            return errors.ConnectedFailed("服务连接超时")
        except ConnectionRefusedError:
            return errors.ConnectedFailed("服务连接被拒")
        if self._first_connect:
            self._first_connect = False

        self.m_tcp_data_transmit = queue.Queue()
        self.m_loop_thread.make_loop_thread(
            fn=self.m_tcp_socket.recv,
            fargs=(self.p_tcp_recv_buflen,),
            ret_cb=self.tcp_recv,
            err_cb=self.tcp_recv_err,
            loop_condition=lambda: not self.is_closed(),
            finish_exc=OSError,
        )
        self.m_loop_thread.make_loop_thread(
            fn=self.tcp_data_transmit,
            err_cb=self.tcp_user_err,
            loop_condition=lambda: not self.is_closed(),
            finish_exc=errors.CloseSocket,
        )

    def _do_connect_tcp(self, timeout=None):
        try:
            self.m_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.m_tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if timeout is not None:
                self.m_tcp_socket.settimeout(timeout)
            self.m_tcp_socket.connect(self.m_tcp_addr)
            if self.m_event_close.is_set():
                self.m_event_close.clear()
        finally:
            self.m_tcp_socket.settimeout(None)

    def connect_udp(self, ip: str, port: int):
        self.m_udp_addr = (ip, port)
        self.m_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.m_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.m_udp_socket.connect(self.m_udp_addr)
        if self.m_event_close.is_set():
            self.m_event_close.clear()

        self.m_udp_data_transmit = queue.Queue()
        self.m_loop_thread.make_loop_thread(
            fn=self.m_udp_socket.recvfrom,
            fargs=(self.p_udp_recv_buflen,),
            ret_cb=self.udp_recv,
            err_cb=self.udp_recv_err,
            loop_condition=lambda: not self.is_closed(),
            finish_exc=OSError,
        )
        self.m_loop_thread.make_loop_thread(
            fn=self.udp_data_transmit,
            err_cb=self.udp_user_err,
            loop_condition=lambda: not self.is_closed(),
            finish_exc=errors.CloseSocket,
        )

    # 发送函数 =============================================================================
    def send_tcp(self, data: bytes):
        if not self.m_event_close.is_set():
            data = self.m_tcp_msg_codec.encode(data)
            self.m_tcp_socket.send(data)

    def send_udp(self, data: bytes):
        if not self.m_event_close.is_set():
            self.m_udp_socket.sendto(data, self.m_udp_addr)

    # socket是否关闭 =======================================================================
    def is_closed(self):
        return self.m_event_close.is_set()

    def _close_tcp_socket(self):
        if self.m_tcp_socket:
            try:
                self.m_tcp_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.m_tcp_socket.close()
            self.m_tcp_socket = None

    def _close_udp_socket(self):
        if self.m_udp_socket:
            try:
                self.m_udp_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.m_udp_socket.close()
            self.m_udp_socket = None

    def close(self):
        if not self.m_event_close.is_set():
            self.m_event_close.set()
        self.m_loop_thread.stop()
        self._close_tcp_socket()
        self._close_udp_socket()
        if self.m_tcp_data_transmit:
            self.m_tcp_data_transmit.put((None, False))
        self.m_loop_thread.join()
        self.m_tcp_data_transmit = None

    # 设置函数
    def set_tcp_recv_cb(self, fn):
        self.m_tcp_recv_cb = fn

    def set_udp_recv_cb(self, fn):
        self.m_udp_recv_cb = fn

    def set_tcp_err_handle(self, fn):
        self.m_tcp_err_handle = fn

    def set_udp_recv_err(self, fn):
        self.m_udp_err_handle = fn

    def set_tcp_msg_codec(self, codecls, *args, **kwargs):
        self.m_tcp_msg_codec = codecls(*args, **kwargs)

    def set_tcp_reconnect_handle(self, fn):
        self.m_tcp_reconnect_handle = fn

    def set_tcp_heart_beat(self, hb_data: bytes = None, hb_t: int = 3, hb_tv: int = 5):
        self.m_heart_beat = QujamHeartBeat(hb_data, hb_t)
        self.m_loop_thread.make_loop_thread(
            fn=self._tcp_heart_beat,
            err_cb=self.tcp_recv_err,
            loop_condition=lambda: not self.is_closed(),
            btime=hb_tv,
        )

    def keep_heart_beat(self):
        if self.m_heart_beat:
            self.m_heart_beat.keep()

    def _tcp_heart_beat(self):
        if self.m_event_close.is_set():
            raise errors.CloseSocket()
        if self.m_heart_beat.alive():
            data = self.m_heart_beat.data()
            if data:
                self.send_tcp(data)
            self.m_heart_beat.cost()
            return
        raise errors.ConnectedBroken("与服务端连接中断")

    # tcp消息接收
    def tcp_recv(self, data: bytes):
        if not data:
            raise errors.ConnectedBroken("服务器已停止运行")
        self.m_tcp_data_transmit.put((data, True))

    def tcp_data_transmit(self):
        data, ok = self.m_tcp_data_transmit.get()
        if not ok:
            raise errors.CloseSocket()
        self.m_tcp_recv_buffer.enqueue(data)
        while self.m_tcp_recv_buffer.size():
            msg = self.m_tcp_msg_codec.decode(self.m_tcp_recv_buffer)
            if msg is None:
                break
            self.m_tcp_recv_cb(msg)

    # tcp消息接收错误回调
    def tcp_recv_err(self, err: Exception):
        if err.__class__ in (errors.ConnectedBroken, ConnectionResetError):
            if self.m_tcp_reconnect:
                self._close_tcp_socket()
                _reconnect = self.m_tcp_reconnect
                while _reconnect:
                    try:
                        self._do_connect_tcp(self.m_tcp_reconn_ivl)
                        self.m_loop_thread.make_loop_thread(
                            fn=self.m_tcp_socket.recv,
                            fargs=(self.p_tcp_recv_buflen,),
                            ret_cb=self.tcp_recv,
                            err_cb=self.tcp_recv_err,
                            loop_condition=lambda: not self.is_closed(),
                            finish_exc=OSError,
                        )
                        if self.m_tcp_reconnect_handle():
                            return True
                    except (ValueError, ConnectionRefusedError, ConnectionResetError):
                        if _reconnect == -1:
                            continue
                        _reconnect -= 1
                        continue
        self.close()
        return self.m_tcp_err_handle(err)

    def tcp_user_err(self, err):
        return self.m_tcp_err_handle(err)

    # udp消息接收
    def udp_recv(self, data):
        self.m_udp_data_transmit.put((data[0], True))

    def udp_data_transmit(self):
        msg, ok = self.m_udp_data_transmit.get()
        if not ok:
            raise errors.CloseSocket()
        self.m_udp_recv_cb(msg)

    # udp消息接收错误回调
    def udp_recv_err(self, err: Exception):
        return self.m_udp_err_handle(err)

    def udp_user_err(self, err):
        return self.m_udp_err_handle(err)

    def join(self, timeout=None):
        self.m_loop_thread.join(timeout=timeout)

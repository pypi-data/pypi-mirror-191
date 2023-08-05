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

import zmq
from zmq.utils.monitor import recv_monitor_message
import threading
from . import qujam_errors as errors
from .qujam_heart_beat import QujamHeartBeat
from .qujam_loop_thread import QujamLoopThread, result_call_back_func, error_handle_func


class QujamSocketZmq:
    FIRSTCONN, RECONNECTED, CONNBROKEN = range(3)

    def __init__(self):
        self.m_ctx = None
        self.m_dealer_socket = None
        self.m_socket_poll = None
        self.m_socket_moniter = None
        self.m_zmq_addr = None
        self.m_closed = True
        self.m_event_connect = threading.Event()
        self.m_event_close = threading.Event()

        self.m_zmq_recv_cb = result_call_back_func
        self.m_zmq_err_handle = error_handle_func
        self.m_data_transmit = None
        self.m_zmq_reconnect_cb = result_call_back_func

        self.m_loop_thread = QujamLoopThread()

        self.m_heart_beat = None

        self.m_reconnect = None
        self._reconnect = 1

        self._first_connect = True

    def connect_router(self,
                       ip: str,
                       port: int,
                       timeout: float = None,  # 连接超时(0 or None:默认3秒超时,  >0:超时时间)
                       reconnect: int = None,  # 重连次数 (0 or None : 默认不重连; -1 : 无限重连; >0 : 重连次数用尽后不再重连)
                       reconnect_ivl: float = None,  # 重连间隔事件
                       ):
        self.m_reconnect = reconnect
        if reconnect and isinstance(reconnect, int):
            self._reconnect = reconnect

        if not timeout or not isinstance(timeout, (int, float)):
            timeout = 2.0
        if not reconnect_ivl or not isinstance(reconnect_ivl, (int, float)):
            reconnect_ivl = 2.0

        self.m_zmq_addr = (ip, port)
        self.m_ctx = zmq.Context()
        self.m_dealer_socket = self.m_ctx.socket(zmq.DEALER)

        self.m_dealer_socket.setsockopt(zmq.CONNECT_TIMEOUT, int(timeout * 1000))
        self.m_dealer_socket.setsockopt(zmq.RECONNECT_IVL, int(reconnect_ivl * 1000))

        self.m_socket_moniter = self.m_dealer_socket.get_monitor_socket(
            zmq.Event.HANDSHAKE_SUCCEEDED | zmq.Event.DISCONNECTED | zmq.Event.MONITOR_STOPPED
        )
        self.m_socket_poll = zmq.Poller()
        self.m_socket_poll.register(self.m_dealer_socket, zmq.POLLIN)

        if self.m_event_close.is_set():
            self.m_event_close.clear()
        if self.m_event_connect.is_set():
            self.m_event_connect.clear()

        self.m_loop_thread.make_loop_thread(
            fn=self._socket_moniter,
            ret_cb=self.m_zmq_reconnect_cb,
            err_cb=self._socket_err_handle,
            loop_condition=lambda: not self.is_closed(),
            finish_exc=errors.CloseSocketZmq,
        )

        self.m_dealer_socket.connect(f"tcp://{ip}:{port}")
        if not self.m_event_connect.wait(timeout):
            self.m_event_close.set()
            return errors.ConnectedFailed("连接失败")
        self.m_data_transmit = queue.Queue()
        self.m_loop_thread.make_loop_thread(
            fn=self._zmq_recv,
            ret_cb=self._socket_recv,
            err_cb=self._socket_err_handle,
            loop_condition=lambda: not self.is_closed(),
            finish_exc=errors.CloseSocketZmq,
        )
        self.m_loop_thread.make_loop_thread(
            fn=self._data_transmit,
            err_cb=self._socket_err_handle,
            loop_condition=lambda: not self.is_closed(),
            finish_exc=errors.CloseSocketZmq,
        )

    def _socket_moniter(self):
        special_err = None
        try:
            poll_ret = self.m_socket_moniter.poll()
            if not poll_ret:
                return None

            if not self.m_socket_moniter:
                special_err = errors.CloseSocketZmq()
                return None
            event = recv_monitor_message(self.m_socket_moniter)['event']

        except Exception:
            if self.m_event_close.is_set():
                special_err = errors.CloseSocketZmq()
                return None
            raise
        else:
            if event == zmq.Event.HANDSHAKE_SUCCEEDED:
                if not self.m_event_connect.is_set():
                    self.m_event_connect.set()
                self._reconnect = 1 if not self.m_reconnect else (self.m_reconnect + 1)

                if self._first_connect:
                    self._first_connect = False
                    return self.FIRSTCONN
                return self.RECONNECTED

            elif event == zmq.Event.DISCONNECTED:
                if self.m_event_connect.is_set():
                    self.m_event_connect.clear()

                if self._reconnect == -1:
                    return self.CONNBROKEN
                self._reconnect -= 1
                if not self._reconnect:
                    self.close()
                    special_err = errors.ConnectedBroken("与服务端连接中断")
                    return None
                return self.CONNBROKEN

            elif event == zmq.Event.MONITOR_STOPPED:
                special_err = errors.CloseSocketZmq()
                return None
        finally:
            if special_err:
                raise special_err

    def close(self):
        if not self.m_event_close.is_set():
            self.m_event_close.set()
            self.m_loop_thread.stop()
            if self.m_dealer_socket:
                self.m_dealer_socket.disable_monitor()
                self.m_socket_moniter.close()
                self.m_socket_moniter = None
                self.m_socket_poll.unregister(self.m_dealer_socket)
                self.m_dealer_socket.disconnect(f"tcp://{self.m_zmq_addr[0]}:{self.m_zmq_addr[1]}")
                self.m_dealer_socket.close()
                self.m_dealer_socket = None
                self.m_socket_poll = None
            if self.m_ctx:
                self.m_ctx.term()
                self.m_ctx = None
            if self.m_data_transmit:
                self.m_data_transmit.put((None, False))
            self.m_loop_thread.join()
            self.m_data_transmit = None

    def send(self, data: bytes):
        if not self.m_event_close.is_set():
            self.m_dealer_socket.send(data)

    def _zmq_recv(self):
        special_err = None
        try:
            if self.m_socket_poll.poll():
                return self.m_dealer_socket.recv(flags=zmq.NOBLOCK)
        except (zmq.error.ZMQError, AttributeError):
            if self.m_event_close.is_set():
                special_err = errors.CloseSocketZmq()
                return
            special_err = errors.ConnectedBroken("连接中断")
        except Exception:
            raise
        finally:
            if special_err:
                raise special_err

    def _socket_recv(self, data):
        self.m_data_transmit.put((data, True))

    def _socket_err_handle(self, err):
        return self.m_zmq_err_handle(err)

    def _data_transmit(self):
        data, ok = self.m_data_transmit.get()
        if not ok:
            raise errors.CloseSocketZmq()
        self.m_zmq_recv_cb(data)

    def set_recv_cb(self, fn):
        self.m_zmq_recv_cb = fn

    def set_reconnect_cb(self, fn):
        self.m_zmq_reconnect_cb = fn

    def set_err_handle(self, fn):
        self.m_zmq_err_handle = fn

    def set_heart_beat(self, hb_data: bytes = None, hb_t: int = 3, hb_tv: int = 5):
        self.m_heart_beat = QujamHeartBeat(hb_data, hb_t)
        self.m_loop_thread.make_loop_thread(
            fn=self._heart_beat,
            err_cb=self.m_zmq_err_handle,
            loop_condition=lambda: not self.is_closed(),
            btime=hb_tv,
            finish_exc=errors.CloseSocketZmq,
        )

    def keep_heart_beat(self):
        if self.m_heart_beat:
            self.m_heart_beat.keep()

    def _heart_beat(self):
        if self.m_event_close.is_set():
            raise errors.CloseSocketZmq()
        if self.m_heart_beat.alive():
            data = self.m_heart_beat.data()
            if data:
                self.send(data)
            self.m_heart_beat.cost()
            return
        raise errors.ConnectedBroken("与服务端连接中断")

    def join(self, wait=None):
        self.m_loop_thread.join(wait)

    def is_closed(self):
        return self.m_event_close.is_set()

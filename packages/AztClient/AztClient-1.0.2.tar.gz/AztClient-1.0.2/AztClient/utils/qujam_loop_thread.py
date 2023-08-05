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
import time
import typing
from threading import Event
from traceback import format_exc

from .qujam_thread import QujamThread


def result_call_back_func(result):
    pass


def error_handle_func(error):
    return False  # Whether the error was handled. If not,an error is raised


def thread_start_func(this_thread):
    pass


def thread_end_func(this_thread, error):
    return False  # Whether the error was handled. If not,an error is raised


class QujamLoopThread:
    def __init__(self, enbale_warning=False):
        self.m_thread_pool: typing.List[QujamThread] = []
        self.m_thread_signals = []
        self.m_stoped = Event()
        self.m_stoped.clear()
        self.m_enable_warning = enbale_warning

    def join(self, timeout: float = None):
        if timeout is None:
            for thd in self.m_thread_pool:
                if thd.joinable():
                    thd.join()
            return
        _tio = timeout
        for thd in self.m_thread_pool:
            if not thd.joinable():
                continue
            _jstart = time.time()
            thd.join(_tio)
            _tio -= time.time() - _jstart
            if _tio <= 0:
                return

    def get_thread_execptions(self):
        exec_list = []
        for thd in self.m_thread_pool:
            if thd.has_exception():
                exec_list.append((thd.get_exception(), thd.exception_traceback()))
        return exec_list

    def running(self):
        return not self.m_stoped.is_set()

    def make_loop_thread(self, fn, fargs=(), fkwargs=None,
                         ret_cb=None, err_cb=None,
                         loop_condition=None,
                         btime=None,
                         ptime=None,
                         finish_exc=None,
                         start_cb=None,
                         finish_cb=None
                         ):
        if not finish_exc:
            finish_exc = []
        elif finish_exc.__class__ is not list:
            finish_exc = [finish_exc]
        if fkwargs is None:
            fkwargs = {}
        if ret_cb is None:
            ret_cb = result_call_back_func

        if err_cb is None:
            err_cb = error_handle_func

        if loop_condition is None:
            def loop_condition():
                return True

        def _keep_loop():
            return self.running() and loop_condition()

        def _wait_time(st):
            if st is None:
                def _wtime():
                    pass

                return _wtime
            thread_signal = Event()
            self.m_thread_signals.append(thread_signal)

            def _wtime():
                thread_signal.wait(st)

            return _wtime

        fn_btime = _wait_time(btime)
        fn_ptime = _wait_time(ptime)

        if not start_cb:
            start_cb = thread_start_func
        if not finish_cb:
            finish_cb = thread_end_func

        def loop_func():
            now_thread = threading.currentThread()
            start_cb(now_thread)
            func_error = None
            while _keep_loop():
                fn_btime()
                if not _keep_loop():
                    break
                try:
                    ret = fn(*fargs, **fkwargs)
                    if not _keep_loop():
                        break
                    ret_cb(ret)
                except Exception as err:
                    # exc_traceback = format_exc()
                    # print(exc_traceback)
                    if err.__class__ in finish_exc:
                        break
                    if not err_cb(err):
                        func_error = err

                    break
                fn_ptime()
            if not finish_cb(now_thread, func_error) and func_error:
                raise func_error

        _t = QujamThread(target=loop_func, daemon=True, _warning=self.m_enable_warning)
        _t.start()
        self.m_thread_pool.append(_t)
        return _t

    def stop(self):
        self.m_stoped.set()
        for ev in self.m_thread_signals:
            if not ev.is_set():
                ev.set()

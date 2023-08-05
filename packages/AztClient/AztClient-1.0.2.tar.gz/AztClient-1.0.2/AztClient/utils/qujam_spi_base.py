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


class QujamSpiObject:
    def __init__(self, spi):
        self.__spi = spi
        self.__rep_queue_manage = dict()
        self.__rep_async_handle_manage = dict()
        self.__rep_sync_handle_manage = dict()

    def call(self, attr, *args, **kwargs):
        method = getattr(self.__spi, attr, None)
        if method and callable(method):
            method(*args, **kwargs)

    def __rep_queue_subscribe(self, sub_id):
        if sub_id not in self.__rep_queue_manage:
            self.__rep_queue_manage[sub_id] = queue.Queue()
        return self.__rep_queue_manage[sub_id]

    def __rep_queue_unsubscribe(self, sub_id):
        self.__rep_queue_manage.pop(sub_id, None)

    def __rep_async_handle_register(self, reg_id, *handles, cover=False):
        if not handles:
            return
        if reg_id in self.__rep_async_handle_manage:
            if cover:
                self.__rep_async_handle_manage[reg_id] = handles
                return
            self.__rep_async_handle_manage[reg_id] += handles
            return
        self.__rep_async_handle_manage[reg_id] = handles

    def __rep_async_handle_unregister(self, reg_id):
        self.__rep_async_handle_manage.pop(reg_id, None)

    def __rep_sync_handle_register(self, reg_id, *handles, cover=False):
        if not handles:
            return
        if reg_id in self.__rep_sync_handle_manage:
            if cover:
                self.__rep_sync_handle_manage[reg_id] = handles
                return
            self.__rep_sync_handle_manage[reg_id] += handles
            return
        self.__rep_sync_handle_manage[reg_id] = handles

    def __rep_sync_handle_unregister(self, reg_id):
        self.__rep_sync_handle_manage.pop(reg_id, None)

    def handle_request(self, rep_id, exec_func=None, fargs=(), fkwargs=None, req_once=False, sync=False, timeout=None,
                       async_handles=(), sync_handles=(), cover_async=False, cover_sync=False):
        self.__rep_async_handle_register(rep_id, *async_handles, cover=cover_async)
        self.__rep_sync_handle_register(rep_id, *sync_handles, cover=cover_sync)
        if not sync:
            if exec_func:
                exec_func(*fargs, **(fkwargs or {}))
            return None
        q_ = self.__rep_queue_subscribe(rep_id)
        if exec_func is not None:
            exec_func(*fargs, **(fkwargs or {}))
        try:
            return q_.get(timeout=timeout)
        except queue.Empty:
            pass
        finally:
            if req_once:
                self.__rep_queue_unsubscribe(rep_id)

    def handle_reply(self, rep_msg, reply_func=None, rep_id=None):
        rep_func = getattr(self.__spi, reply_func, None) if reply_func else None

        b_not_rep_func = not rep_func
        b_not_rep_ret = True if rep_id is None else (rep_id not in self.__rep_queue_manage)

        if b_not_rep_func and b_not_rep_ret:
            return False

        async_handles = None if rep_id is None else self.__rep_async_handle_manage.get(rep_id, None)
        if async_handles:
            bfilter = False
            for handle in async_handles:
                rep_msg, bfilter = handle(rep_msg)
                if bfilter:
                    break
            if bfilter:
                return False
            self.__rep_async_handle_unregister(rep_id)

        # 异步转发
        if not b_not_rep_func:
            rep_func(rep_msg)

        sync_handles = None if rep_id is None else self.__rep_sync_handle_manage.get(rep_id, None)
        if sync_handles:
            bfilter = False
            for handle in sync_handles:
                rep_msg, bfilter = handle(rep_msg)
                if bfilter:
                    break
            if bfilter:
                return False
            self.__rep_sync_handle_unregister(rep_id)
        # 同步转发
        if not b_not_rep_ret:
            self.__rep_queue_manage[rep_id].put(rep_msg, block=False)
        return True

    def clear(self):
        self.__rep_queue_manage.clear()
        self.__rep_async_handle_manage.clear()


__method_spi_empty_tag = "__empty_spi_method__"


def set_spi_base(spi_base):
    _spi_attrs = dir(spi_base)
    _empty_methods = [_method for _method in _spi_attrs if hasattr(getattr(spi_base, _method), __method_spi_empty_tag)]
    for _empty_method in _empty_methods:
        delattr(spi_base, _empty_method)
    return spi_base


def set_empty_method(method):
    setattr(method, __method_spi_empty_tag, True)
    return method

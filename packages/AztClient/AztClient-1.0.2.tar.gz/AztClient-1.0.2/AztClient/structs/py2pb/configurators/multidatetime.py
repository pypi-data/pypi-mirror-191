#  =============================================================================
#  GNU Lesser General Public License (LGPL)
#
#  Copyright (c) 2022 Qujamlee
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

from .base import ConfiguratorBase, ProtoWrapper

"""
因为某些原因，(比如后端的疏忽),同一个protobuf时间字段的格式并不统一，
比如可能是"20220901-09:30:03.188"格式，也可能是"20221109-184637.120000"格式，
这里使用multi就可以很好地解决该问题
"""


class MultiDatetimeConfigurator(ConfiguratorBase):
    def __init__(self, **dtformat):
        self._format = dtformat
        self._attrs = tuple(self._format.keys())

    def to_proto(self, pyobj, pbobj: ProtoWrapper):
        for _attr, formators in self._format.items():
            if pbobj.hasattr(_attr):
                val = getattr(pyobj, _attr)
                if not val:
                    continue
                special_err = None
                for formator in formators:
                    try:
                        if isinstance(formator, str):
                            dtval = val.strftime(formator)
                            pbobj.setattr(_attr, dtval)
                        elif formator is None or isinstance(formator, datetime.tzinfo):
                            dtval = val.timestamp()
                            pbobj.setattr(_attr, dtval)
                        special_err = None  # 成功了,清除记录
                        break
                    except Exception as e:
                        special_err = e  # 记录错误
                        continue
                if special_err:
                    raise ValueError(
                        f"MultiDatetimeConfigurator execute 'to_proto' failed"
                        f"({pyobj.__class__}.{_attr})") from special_err
        return pbobj

    def to_pyobj(self, pbobj: ProtoWrapper, pyobj):
        for _attr, formators in self._format.items():
            val = pbobj.getattr(_attr, None)
            if val is not None:
                special_err = None
                for formator in formators:
                    try:
                        if isinstance(val, (int, float)):
                            dt = datetime.datetime.fromtimestamp(val)
                            setattr(pyobj, _attr, dt)
                        elif isinstance(val, str) and val:
                            dt = datetime.datetime.strptime(val, formator)
                            setattr(pyobj, _attr, dt)
                        special_err = None
                        break
                    except Exception as e:
                        special_err = e
                        continue
                if special_err:
                    raise ValueError(
                        f"MultiDatetimeConfigurator execute 'to_pyobj' failed"
                        f"({pyobj.__class__}.{_attr})") from special_err
        return pyobj

    def get_attrs(self):
        return self._attrs

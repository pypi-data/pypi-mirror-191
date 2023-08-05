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

from .base import ConfiguratorBase, ProtoWrapper


class DatetimeConfigurator(ConfiguratorBase):
    def __init__(self, **dtformat):
        self._format = dtformat
        self._attrs = tuple(self._format.keys())

    def to_proto(self, pyobj, pbobj: ProtoWrapper):
        for _attr, formator in self._format.items():
            if pbobj.hasattr(_attr):
                val = getattr(pyobj, _attr)
                if not val:
                    continue
                if isinstance(formator, str):
                    dtval = val.strftime(formator)
                    pbobj.setattr(_attr, dtval)
                elif formator is None or isinstance(formator, datetime.tzinfo):
                    dtval = val.timestamp()
                    pbobj.setattr(_attr, dtval)
        return pbobj

    def to_pyobj(self, pbobj: ProtoWrapper, pyobj):
        for _attr, formator in self._format.items():
            val = pbobj.getattr(_attr, None)
            if val is not None:
                if isinstance(val, (int, float)):
                    dt = datetime.datetime.fromtimestamp(val)
                    setattr(pyobj, _attr, dt)
                elif isinstance(val, str) and val:
                    dt = datetime.datetime.strptime(val, formator)
                    setattr(pyobj, _attr, dt)
        return pyobj

    def get_attrs(self):
        return self._attrs

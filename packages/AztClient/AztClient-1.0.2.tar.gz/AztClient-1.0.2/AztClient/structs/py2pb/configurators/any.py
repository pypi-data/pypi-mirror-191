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

from .base import ConfiguratorBase
from ..convertor import GetPbCls, ToPyobj, ToProto


class AnyConfigurator(ConfiguratorBase):
    def __init__(self, **any_map):
        self._any_map = any_map
        self._attrs = tuple(self._any_map.keys())

    def to_proto(self, pyobj, pbobj):
        for _attr in self._attrs:
            pbany = pbobj.getattr(_attr)
            if pbany:
                val = getattr(pyobj, _attr)
                if val is None:
                    continue
                _subpbobj = ToProto(val)
                pbany.Pack(_subpbobj)
        return pbobj

    def to_pyobj(self, pbobj, pyobj):
        for _attr, _pycls in self._any_map.items():
            any_pb = pbobj.getattr(_attr)
            if any_pb is not None:
                _subpbobj = GetPbCls(_pycls)()
                any_pb.Unpack(_subpbobj)
                setattr(pyobj, _attr, ToPyobj(_subpbobj))
        return pyobj

    def get_attrs(self):
        return self._attrs

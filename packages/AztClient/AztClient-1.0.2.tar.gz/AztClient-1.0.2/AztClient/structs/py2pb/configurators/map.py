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

from ..convertor import ToPyobj, ToProto
from .base import ConfiguratorBase


class MapConfigurator(ConfiguratorBase):
    def get_attrs(self):
        return self._attrs

    def __init__(self, *attrs, recur=False):
        self._attrs = attrs
        self._recur = recur

    def to_proto(self, pyobj, pbobj):
        for _attr in self._attrs:
            _map = pbobj.getattr(_attr, None)
            if _map is not None:
                pyval = getattr(pyobj, _attr)
                if pyval is None:
                    continue
                if self._recur:
                    for _key, _val in pyval.items():
                        _map[_key] = ToProto(_val)
                    continue
                for _key, _val in pyval.items():
                    _map[_key] = _val
        return pbobj

    def to_pyobj(self, pbobj, pyobj):
        for _attr in self._attrs:
            _map = pbobj.getattr(_attr, None)
            if _map is not None:
                if self._recur:
                    setattr(pyobj, _attr, {_key: ToPyobj(_val) for _key, _val in _map.items()})
                    continue
                setattr(pyobj, _attr, _map)
        return pyobj

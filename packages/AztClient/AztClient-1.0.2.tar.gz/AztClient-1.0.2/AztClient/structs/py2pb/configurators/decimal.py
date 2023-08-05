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
from ..protobuf_wrapper import ProtoWrapper


class DecimalConfigurator(ConfiguratorBase):
    def get_attrs(self):
        return self._attrs

    def __init__(self, cfg_attr, normal_attrs=(), repeat_attrs=(), map_attrs=(), default_decimal=2):
        self._cfg_attr = cfg_attr
        self._normal_attrs = normal_attrs
        self._repeat_attrs = repeat_attrs
        self._map_attrs = map_attrs
        self._default_decimal = default_decimal
        self._default_decimal_pow = 10 ** self._default_decimal

        self._attrs = self._normal_attrs + self._repeat_attrs + self._map_attrs

    def to_proto(self, pyobj, pbobj: ProtoWrapper):
        if pbobj.hasattr(self._cfg_attr):
            pbobj.setattr(self._cfg_attr, self._default_decimal)
        for normal_attr in self._normal_attrs:
            if pbobj.hasattr(normal_attr):
                pyval = getattr(pyobj, normal_attr)
                if pyval is None:
                    continue
                pbobj.setattr(normal_attr, int(pyval * self._default_decimal_pow))
        for repeat_attr in self._repeat_attrs:
            if pbobj.hasattr(repeat_attr):
                pyrepeatval = getattr(pyobj, repeat_attr)
                if pyrepeatval is None:
                    continue
                pbobj.getattr(repeat_attr, _raise=True).extend(
                    [repeat_val * self._default_decimal_pow for repeat_val in pyrepeatval]
                )
        for map_attr in self._map_attrs:
            _map = pbobj.getattr(map_attr, None)
            if _map is not None:
                pymapval = getattr(pyobj, map_attr)
                if pymapval is None:
                    continue
                for _key, _val in pymapval.items():
                    _map[_key] = _val
        return pbobj

    def to_pyobj(self, pbobj: ProtoWrapper, pyobj):
        decimal_pow = self._default_decimal_pow
        decimal = pbobj.getattr(self._cfg_attr)
        if decimal is not None:
            decimal_pow = 10 ** decimal

        for normal_attr in self._normal_attrs:
            pbval = pbobj.getattr(normal_attr)
            if pbval is not None:
                setattr(pyobj, normal_attr, pbval / decimal_pow)
        for repeat_attr in self._repeat_attrs:
            pbrepeatval = pbobj.getattr(repeat_attr)
            if pbrepeatval is not None:
                setattr(pyobj, repeat_attr, [repeatval / decimal_pow for repeatval in pbrepeatval])
        for map_attr in self._map_attrs:
            pbmapval = pbobj.getattr(map_attr)
            if pbmapval is not None:
                setattr(pyobj, map_attr, {mkey: mval / decimal_pow for mkey, mval in pbmapval.items()})
        return pyobj

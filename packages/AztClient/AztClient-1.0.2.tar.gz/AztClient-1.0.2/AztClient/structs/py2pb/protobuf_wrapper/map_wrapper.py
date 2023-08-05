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

from ..tools import get_protoclass_attrs
from .wrapper_base import ProtoWrapperBase


# 映射封装
class ProtoMapWrapper(ProtoWrapperBase):
    def __init__(self, proto, attrs_map):
        super(ProtoMapWrapper, self).__init__(proto)
        protoattrs = get_protoclass_attrs(proto, wrap=True)
        self._attrs_map = dict(zip(protoattrs, protoattrs))
        self._attrs_map.update(attrs_map)

    def _get_attr_name(self, item):
        return self._attrs_map.get(item)

    def getattr(self, item, default=None, _raise=False):
        if _raise:
            return getattr(self._proto, self._get_attr_name(item))
        return getattr(self._proto, self._get_attr_name(item), default)

    def setattr(self, key, value):
        setattr(self._proto, self._get_attr_name(key), value)

    def hasattr(self, item):
        return hasattr(self._proto, self._get_attr_name(item))

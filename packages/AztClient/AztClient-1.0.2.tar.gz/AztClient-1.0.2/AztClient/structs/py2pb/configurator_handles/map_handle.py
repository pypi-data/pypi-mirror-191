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

from .base_handle import ConfigHandleBase
from ..protobuf_wrapper import ProtoMapWrapper


class MapConfigHandle(ConfigHandleBase):
    def __init__(self, **attrs_map):
        self._attrs_map = attrs_map

    def PreToProto(self, pyobj, pbobj):
        return pyobj, ProtoMapWrapper(pbobj, self._attrs_map)

    def PostToProto(self, pbobj):
        if hasattr(pbobj, "getproto"):
            return pbobj.getproto()
        return pbobj

    def PreToPyobj(self, pbobj, pyobj):
        return ProtoMapWrapper(pbobj, self._attrs_map), pyobj

    def PostToPyobj(self, pyobj):
        return pyobj

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

class ProtoWrapperBase:
    def __init__(self, proto):
        if isinstance(proto, ProtoWrapperBase):
            self._proto = proto.getproto()
            return
        self._proto = proto

    def getattr(self, item, default=None, _raise=False):
        raise NotImplementedError

    def setattr(self, key, value):
        raise NotImplementedError

    def hasattr(self, item):
        raise NotImplementedError

    def getproto(self):
        return self._proto


# 简单封装
class ProtoWrapper(ProtoWrapperBase):
    def getattr(self, item, default=None, _raise=False):
        if _raise:
            return getattr(self._proto, item)
        return getattr(self._proto, item, default)

    def setattr(self, key, value):
        setattr(self._proto, key, value)

    def hasattr(self, item):
        return hasattr(self._proto, item)
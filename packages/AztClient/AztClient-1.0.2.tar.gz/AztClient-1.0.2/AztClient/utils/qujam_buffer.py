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

class BufferQueue:
    def __init__(self):
        self._buf = bytearray()

    def enqueue(self, msg: bytes):
        self._buf.extend(msg)

    def dequeue(self, n=1) -> bytes:
        ret = self._buf[:n]
        self._buf = self._buf[n:]
        return bytes(ret)

    def dequeue_all(self) -> bytes:
        ret = self._buf
        self.clear()
        return bytes(ret)

    def drop(self, n=1):
        self._buf = self._buf[n:]

    def read(self, n=1) -> bytes:
        return bytes(self._buf[:n])

    def size(self):
        return len(self._buf)

    def clear(self):
        self._buf.clear()

    def __bool__(self):
        return not not self._buf

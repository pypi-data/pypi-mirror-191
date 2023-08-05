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
import struct
from .defalut_policy import MsgCodecBase


class BodySizeCodec(MsgCodecBase):
    def __init__(self, header_size=4, max_recv_size=None):
        self.m_header_size = header_size
        self.m_max_recv_size = max_recv_size

    def decode(self, buffer):
        body_size = self._get_body_size(buffer)
        if body_size is None:
            return None
        return buffer.dequeue(body_size)

    def encode(self, data: bytes):
        return struct.pack("I", len(data)) + data

    def _get_body_size(self, buffer):
        while buffer.size() > self.m_header_size:
            header_size = struct.unpack("I", buffer.read(self.m_header_size))[0]
            if self.m_max_recv_size is not None and header_size > self.m_max_recv_size:
                buffer.drop(self.m_header_size)
                continue

            if buffer.size() >= (header_size + self.m_header_size):
                buffer.drop(self.m_header_size)
                return header_size
            return None

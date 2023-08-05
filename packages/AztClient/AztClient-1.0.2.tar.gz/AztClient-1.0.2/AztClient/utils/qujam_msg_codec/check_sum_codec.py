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


class AztCheckSumCodec(MsgCodecBase):
    HEARTBEAT = 0

    def __init__(self, header_size=8, tail_size=4, max_recv_size=None):
        self.m_header_size = header_size
        self.m_tailer_size = tail_size
        self.m_max_recv_size = max_recv_size
        self._header_tailer_size = self.m_header_size + self.m_tailer_size

    def encode(self, data: bytes):
        body_size = len(data)
        packet = bytearray(self._header_tailer_size + body_size)
        packet[:self.m_header_size] = struct.pack("I", body_size) * 2
        if body_size:
            packet[self.m_header_size:self.m_header_size + body_size] = data
        packet[-self.m_tailer_size:] = struct.pack("i", self.check_sum(data))
        return bytes(packet)

    def decode(self, buffer):
        body_size = self._get_body_size(buffer)
        if body_size is None:
            return
        data = self.HEARTBEAT
        if body_size > 0:
            data = buffer.dequeue(body_size)
            tail = struct.unpack("i", buffer.dequeue(self.m_tailer_size))[0]
            return data if self.check_sum(data) == tail else None
        buffer.drop(self.m_tailer_size)
        return data

    def _get_body_size(self, buffer):
        while buffer.size() > self.m_header_size:
            size_tuple = struct.unpack("2I", buffer.read(self.m_header_size))
            body_size = size_tuple[0]  # 预留一位
            if self.m_max_recv_size and body_size > self.m_max_recv_size:
                buffer.drop(self.m_header_size)
                continue
            if buffer.size() >= (body_size + self.m_header_size + self.m_tailer_size):
                buffer.drop(self.m_header_size)
                return body_size
            return None

    @staticmethod
    def check_sum(data: bytes):
        if not data:
            return -1
        data_size = len(data)
        cksum = sum(struct.unpack(f"{int(data_size / 2)}H", data)) if not (data_size % 2) else (
                sum(struct.unpack(f"{int((data_size - 1) / 2)}H", data[:-1])) + data[-1])
        while cksum >> 16:
            cksum = (cksum >> 16) + (cksum & 0xffff)
        return ~cksum

    @classmethod
    def heartbeat(cls):
        return struct.pack("2Ii", 0, 0, -1)

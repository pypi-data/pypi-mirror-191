import numpy as np
import struct
from io import BytesIO
from typing import List, Tuple, BinaryIO, Union


class Parser:
    ADDR = 0xfe
    BLOCK_SZ: int = 0x1000
    PACKET_FMT = "1c1B3s1c"
    PACKET_LENGTH: int = struct.calcsize(PACKET_FMT)

    buffer: BinaryIO = BytesIO()
    index: int = -1

    def __init__(self) -> None:
        self.index = 0

    @staticmethod
    def sext24(d: bytes):
        """Convert 24-bit signed integer to 32-bit signed integer.

        Args:
            d (bytearray): bytes

        Returns:
            int: integer
        """
        if d[0] & 0x80:
            d = bytearray([0xff]) + d
        else:
            d = bytearray([0x00]) + d
        return struct.unpack('>i', d)[0]

    @classmethod
    def verify_packet(cls, data: bytes):
        return np.bitwise_xor.reduce(np.frombuffer(data[:-1], dtype=np.uint8)) == data[-1]

    def parse_packet(self, data: bytes) -> Union[None, np.uint16]:
        st = struct.unpack(self.PACKET_FMT, data)
        addr = st[1] >> 4
        n_digit = st[1] % 0x10
        value = self.sext24(st[2])
        self.index += 1
        return addr, value * 10 ** -n_digit, self.index

    def sync(self, buffer: bytes) -> Tuple[bool, List[Union[None, np.ndarray]]]:
        self.buffer.write(buffer)
        self.buffer.seek(0)

        while True:
            flag = self.buffer.read(1)
            if len(flag) != 1:
                return False, []
            if flag[0] == self.ADDR:
                self.buffer.seek(self.buffer.tell() - 1)
                break

        pkt = self.buffer.read(self.PACKET_LENGTH)
        if len(pkt) != self.PACKET_LENGTH:
            return False, []

        data_valid = self.verify_packet(pkt)
        if data_valid:
            res = [self.parse_packet(pkt)]
            while True:
                pkt = self.buffer.read(self.PACKET_LENGTH)
                if len(pkt) < self.PACKET_LENGTH:
                    self.buffer = BytesIO(pkt)
                    self.buffer.read()  # move pointer to end
                    break
                res.append(self.parse_packet(pkt))
            return True, res
        else:
            return False, []

    def submit_buffer(self, buffer: bytes) -> List[Union[None, np.ndarray]]:
        success, res = self.sync(buffer)
        self.state = "synced" if success else "unsynced"
        return res

    def reset(self):
        self.index = -1
        self.buffer = BytesIO()

from serial import Serial

from .Parser import Parser


class Sensor:
    def __init__(self, conn: Serial):
        self.conn = conn
        self.parser = Parser()
        pass

    def reset(self):
        self.conn.write(bytes([0xfe, 0xff, 0x01, 0x00, 0x00, 0x0d]))
        # self.conn.write(b'\xfe\xff\x01\x00\x00\x0d')
        self.parser.reset()
        pass

    def read_once(self):
        buf = self.conn.read(6)
        res = self.parser.submit_buffer(buf)
        return res[-1] if len(res) > 0 else None

    def read_batch(self):
        buf = self.conn.read(6)
        res = self.parser.submit_buffer(buf)
        return res

    def begin(self, interval_ms: int):
        pass

    def end(self):
        pass

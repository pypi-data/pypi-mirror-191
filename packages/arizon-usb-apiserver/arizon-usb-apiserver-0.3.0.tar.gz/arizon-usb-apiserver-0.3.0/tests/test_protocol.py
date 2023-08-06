from arizon_usb_apiserver import Parser

if __name__ == '__main__':
    pass
    p = Parser()
    res = p.submit_buffer(bytearray([0xfe, 0x11, 0x00, 0x01, 0xa8, 0x46]))
    print(res)
    res = p.submit_buffer(bytearray([0xfe, 0x11, 0x00, 0x14, 0x16, 0xed]))
    print(res)
    res = p.submit_buffer(bytearray([0xfe, 0x11, 0xff, 0xef, 0x7c, 0x83]))
    print(res)

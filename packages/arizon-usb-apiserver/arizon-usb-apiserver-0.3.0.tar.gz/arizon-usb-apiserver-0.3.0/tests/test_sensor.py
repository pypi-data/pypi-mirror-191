from serial import Serial

from arizon_usb_apiserver import Sensor

if __name__ == '__main__':
    conn = Serial("COM2", 115200)
    sensor = Sensor(conn)
    sensor.reset()
    while True:
        print(sensor.read_once())

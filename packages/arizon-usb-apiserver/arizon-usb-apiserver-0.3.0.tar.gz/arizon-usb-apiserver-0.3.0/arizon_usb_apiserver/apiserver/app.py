# import multiprocessing as mp
# import os
# import os.path as osp
# import signal
import argparse
import logging
import queue
import threading
import time
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from serial import Serial
from typing import List, Optional, Dict, Union

from arizon_usb_apiserver import Config as SensorConfig
from arizon_usb_apiserver import Sensor

app = FastAPI()


class Application:
    logger: logging.Logger
    option: SensorConfig
    start_fifo_ev: threading.Event
    force_data_queue: queue.Queue

    def __init__(self, cfg) -> None:
        if isinstance(cfg, SensorConfig):
            self.option = cfg
        elif isinstance(cfg, str):
            self.option = SensorConfig(cfg)
        elif isinstance(cfg, argparse.Namespace):
            self.option = SensorConfig(cfg.config)
        else:
            raise TypeError(
                "cfg must be SensorConfig, str, or argparse.Namespace"
            )

        self.logger = logging.getLogger("arizon.main")
        self.start_fifo_ev = threading.Event()
        self.force_data_queue = queue.Queue(maxsize=1024)

    def start_thread(self):
        self.logger.info(f"Start force data collection thread, serial port: {self.option.serial_port}, baudrate: {self.option.serial_baudrate}")

        def update_arizon_sensor_thread():
            while True:
                self.start_fifo_ev.wait()

                conn = Serial(self.option.serial_port, self.option.serial_baudrate)
                sensor = Sensor(conn)
                sensor.reset()
                while True:
                    data = sensor.read_once()
                    if data is None:
                        continue
                    while self.force_data_queue.full():
                        self.force_data_queue.get(block=False)
                    self.force_data_queue.put(
                        {
                            "addr": data[0],
                            "f": data[1],
                            "index": data[2],
                            "sys_ts_ns": time.time_ns()
                        },
                        block=False
                    )
                    if not self.start_fifo_ev.is_set():
                        conn.close()
                        break

        threading.Thread(target=update_arizon_sensor_thread,
                         daemon=True).start()

    def shutdown(self):
        return None

    def start_fifo(self) -> Optional[Exception]:
        self.logger.info("Start force data collection")
        self.start_fifo_ev.set()
        return None

    def stop_fifo(self) -> Optional[Exception]:
        self.logger.info("Stop force data collection")
        self.start_fifo_ev.clear()
        return None

    def clean_cached_force(self) -> Optional[Exception]:
        for _ in range(self.force_data_queue.qsize()):
            if not self.force_data_queue.empty():
                self.force_data_queue.get(block=False)
        return None

    @property
    def fifo_status(self) -> bool:
        return self.start_fifo_ev.is_set()

    def get(self) -> Optional[Dict[str, Union[int, float]]]:
        try:
            return self.force_data_queue.get(timeout=1e-2)
        except queue.Empty:
            return None

        except Exception as e:
            self.logger.error(f"Error: {e}")
            return None


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./hipnuc_config.yaml")
    run_args = parser.parse_args(sys.argv[1:])

    logging.basicConfig(level=logging.INFO)

    app = Application(run_args)
    app.start_thread()

    app.start_fifo_ev.set()

    try:
        while True:
            print(app.get())

    except KeyboardInterrupt as e:
        app.shutdown()

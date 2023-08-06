import argparse
import grpc
import logging
import time
from typing import Optional

from arizon_usb_apiserver.Config import Config as SensorConfig
from arizon_usb_apiserver.apiserver.server import get_server


def main(args):
    logging.basicConfig(level=logging.INFO)
    cfg = SensorConfig(args.config)
    if cfg.valid is False:
        logging.error("Invalid config file")
        exit(1)

    server = get_server(cfg)
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


def entry_point(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./arizon_config.yaml")
    run_args = parser.parse_args(argv[1:])
    main(run_args)


if __name__ == '__main__':
    import sys

    exit(entry_point(sys.argv))

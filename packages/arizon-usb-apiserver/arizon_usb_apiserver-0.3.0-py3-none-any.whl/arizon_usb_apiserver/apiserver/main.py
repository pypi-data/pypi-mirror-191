import argparse
import os

from .grpc_server import main as grpc_main
from .restful_server import main as restful_main

API_SERVER_RESTFUL = os.environ.get("API_SERVER_RESTFUL", "0") == "1"


def entry_point(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./arizon_config.yaml")
    run_args = parser.parse_args(argv[1:])

    if API_SERVER_RESTFUL:
        print("Launching RESTful server")
        restful_main(run_args)
    else:
        print("Launching gRPC server")
        grpc_main(run_args)


if __name__ == '__main__':
    import sys

    exit(entry_point(sys.argv))

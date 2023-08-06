import argparse
import time
import logging
from typing import Optional
import grpc
from .server import get_server
from hipnuc_usb_apiserver.Config import Config as IMUConfig

SERVER: Optional[grpc.server] = None

DEVELOP_DEBUG = False


def main(args):
    logging.basicConfig(level=logging.INFO)
    cfg = IMUConfig(args.config)

    server = get_server(cfg)
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


def entry_point(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./hipnuc_config.yaml")
    run_args = parser.parse_args(argv)
    return main(run_args)


if __name__ == '__main__':
    import sys
    exit(entry_point(sys.argv))

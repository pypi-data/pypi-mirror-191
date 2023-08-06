import argparse
import grpc
import logging
import time
from typing import Optional

from hipnuc_usb_apiserver.Config import Config as IMUConfig
from .server import get_server

SERVER: Optional[grpc.server] = None

DEVELOP_DEBUG = False


def main(args):
    logging.basicConfig(level=logging.INFO)
    cfg = IMUConfig(args.config)
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
    parser.add_argument("--config", type=str, default="./hipnuc_config.yaml")
    run_args = parser.parse_args(argv)
    return main(run_args)


if __name__ == '__main__':
    import sys

    exit(entry_point(sys.argv))

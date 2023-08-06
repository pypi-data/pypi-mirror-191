import argparse
import sys

import hipnuc_usb_apiserver.apiserver as apiserver
import hipnuc_usb_apiserver.cmd as cmd

parser = argparse.ArgumentParser()

args = sys.argv[1:]
if len(args) == 0:
    exit(print("No arguments provided"))
if args[0] == "configure":
    exit(cmd.configure(args[1:]))
elif args[0] == "apiserver":
    exit(apiserver.serve(args[1:]))
else:
    print("Unknown command: {}".format(args[0]))

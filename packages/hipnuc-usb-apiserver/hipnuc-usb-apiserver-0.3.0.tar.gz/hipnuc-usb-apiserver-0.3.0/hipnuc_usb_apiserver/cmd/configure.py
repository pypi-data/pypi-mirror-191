import pprint
import yaml
from py_cli_interaction import must_parse_cli_int, must_parse_cli_bool, must_parse_cli_string


def main(args):
    while True:
        api_port = must_parse_cli_int("Enter a port number", 1024, 65535, 8080)
        api_interface = must_parse_cli_string("Enter a interface", "0.0.0.0")
        serial_port = must_parse_cli_string("Enter a serial port")
        serial_baudrate = must_parse_cli_int(
            "Enter a serial baudrate", 0, 1500000, 921600)
        debug = must_parse_cli_bool("Debug mode", False)

        res = {
            "hipnuc_usb_apiserver": {
                "serial": [{
                    "port": serial_port,
                    "baudrate": serial_baudrate,
                    "report_datatype": {  # TODO: add more options
                        "imusol": True,
                        "gwsol": False,
                        "id": True,
                        "acc": False,
                        "gyr": False,
                        "mag": False,
                        "euler": False,
                        "quat": False,
                        "imusol_raw": True,
                        "gwsol_raw": True,
                    }
                }],
                "api": {
                    "port": api_port,
                    "interface": api_interface
                },
                "debug": debug
            }
        }
        print("Your configuration is:")
        pprint.pprint(res)
        confirm = must_parse_cli_bool("Confirm?", True)
        if confirm:
            break
        else:
            continue

    dest = must_parse_cli_string(
        "Enter save destination", "./hipnuc_config.yaml")
    with open(dest, 'w') as f:
        yaml.dump(res, f)


def entry_point(argv):
    main(None)


if __name__ == '__main__':
    import sys

    main(sys.argv)

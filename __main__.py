import sys
import argparse
import logging
from serial.tools.list_ports import comports
from hermess import App


# configure the command line parser
parser = argparse.ArgumentParser(description='HERMESS Ground Station Software')
groupSingle = parser.add_mutually_exclusive_group()
groupSingle.add_argument('--ports', action="store_true", help='List all available COM ports')
groupSingle.add_argument('-p', default=None, help='The port to use for the UART configuration')


if __name__ == '__main__':
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Display only all ports in terminal
    if args.ports:
        for name, desc, _ in comports():
            print(name + ' - ' + desc)
        sys.exit(0)

    if args.p is None:
        print('No Port selected')
        sys.exit(0)

    # run main loop
    sys.exit(App.run(args.p))

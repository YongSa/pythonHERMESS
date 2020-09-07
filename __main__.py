import sys
import argparse
from serial.tools.list_ports import comports
from Hermess import App

parser = argparse.ArgumentParser(description='select port')
parser.add_argument('--ports', action="store_true")
parser.add_argument('-p', default='COM3')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.ports:
        for name, desc, _ in comports():
            print(name + ' - ' + desc)
        sys.exit(0)
    sys.exit(App.run(args.p))

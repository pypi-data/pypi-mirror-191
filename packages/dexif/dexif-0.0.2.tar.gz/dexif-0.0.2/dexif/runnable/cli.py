# standard imports
import sys
import argparse

from dexif import *

argparser = argparse.ArgumentParser()
argparser.add_argument('-x', action='store_true', help='Interpret value as hex (will decode to float)')
argparser.add_argument('-i', action='store_true', help='Encode to integer value (instead of hex)')
argparser.add_argument('-p', action='store_true', help='Pad hex result')
argparser.add_argument('value', type=str, help='Value to encode or decode')
args = argparser.parse_args(sys.argv[1:])


def main():
    decode = False
    if args.x:
        decode = True
    elif len(args.value) > 1 and args.value[:2] == '0x':
        decode = True

    if decode:
        print(from_fixed(args.value))
        return
    r = to_fixed(args.value)
    if not args.i:
        r = hex(r)
        r = r[2:]
        if args.p:
            if len(r) % 2 != 0:
                r = '0' + r
    print(r)


if __name__ == '__main__':
    main()

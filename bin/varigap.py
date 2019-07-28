#!/usr/bin/env python3
""" Creates a Varipacker-format "gap" chunk """

import sys
import argparse
from itsybitser import varipacker

def main():
    """ Program entry point """

    parser = argparse.ArgumentParser(
        description="Creates a Varipacker-format \"gap\" chunk"
    )
    parser.add_argument("-c", "--comment", type=str,
                        help="Prepend the output with specified comment string")
    parser.add_argument("-n", "--omit-newline", action="store_true",
                        help="The ending newline character(s) will be omitted from the output")
    parser.add_argument(
        dest="length",
        type=int,
        help="Length of gap to encode"
    )
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding="UTF-8"),
                        help="Name of file in which to write the packed gap",
                        default=sys.stdout)
    args = parser.parse_args()

    varipacker_content = varipacker.encode_gap(args.length)
    if args.comment:
        args.outfile.write("# {}\n".format(args.comment))
    args.outfile.write(varipacker_content)
    if not args.omit_newline:
        args.outfile.write("\n")

if __name__ == "__main__":
    main()

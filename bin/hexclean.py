#!/usr/bin/env python3
""" Strip comments and normalize whitespace for Hextream format content """

import sys
import argparse
from itsybitser import hextream

def main():
    """ Program entry point """

    parser = argparse.ArgumentParser(
        description="Strip comments and normalize whitespace for Hextream format content"
    )
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding="UTF-8"),
                        help="Name of file with content to be cleaned",
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding="UTF-8"),
                        help="Name of file in which to write the cleaned content",
                        default=sys.stdout)
    args = parser.parse_args()

    hex_content = args.infile.read()
    binary_content = hextream.decode(hex_content)
    hex_content = hextream.encode(binary_content)
    args.outfile.write(hex_content)

if __name__ == "__main__":
    main()

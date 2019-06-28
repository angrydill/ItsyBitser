#!/usr/bin/env python3
""" Creates a Varipacker-format "gap" chunk """

import argparse
from itsybitser import varipacker

def main():
    parser = argparse.ArgumentParser(
        description="Creates a Varipacker-format \"gap\" chunk"
    )
    parser.add_argument(
        dest="length",
        type=int,
        help="Length of gap to encode"
    )

    args = parser.parse_args()
    varipacker_content = varipacker.encode_gap(args.length)
    print(varipacker_content)

if __name__ == "__main__":
    main()

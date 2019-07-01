#!/usr/bin/env python3
""" Produces list of map cell values, and cell offsets where they first appear """

import sys
import argparse
from itsybitser import hextream

def main():
    """ Program entry point """

    parser = argparse.ArgumentParser(
        description=(
            "Takes Hextream-encoded map data (as produced by mapextract.py) and produces" +
            " a comma-delimited list of unique cell values, and the offsets of the map" +
            " cells where those values first appear"
        )
    )
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding="UTF-8"),
                        help="Name of Hextream file with map data to be indexed",
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding="UTF-8"),
                        help="Name of file in which to write the map index",
                        default=sys.stdout)
    args = parser.parse_args()
    build_map_index(args.infile, args.outfile)

def build_map_index(infile, outfile):
    """ Produces list of map cell values, and cell offsets where they first appear """

    hex_content = infile.read()
    binary_content = hextream.decode(hex_content)

    map_index = {}
    for position, value in enumerate(binary_content):
        if not value in map_index:
            map_index[value] = position

    csv_map_index = "\n".join([
        "{},{}".format(value, position)
        for value, position in sorted(map_index.items())
    ])

    outfile.write("value,position\n{}\n".format(csv_map_index))

if __name__ == "__main__":
    main()

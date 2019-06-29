#!/usr/bin/env python3
""" Extract map cell content of a Tiled .tmx file as a commented Hextream """

import sys
import argparse
import json
from xml.etree import ElementTree

def main():
    """ Program entry point """
    parser = argparse.ArgumentParser(
        description="Extract map cell content of a Tiled .tmx file as a commented Hextream"
    )
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding="UTF-8"),
                        help="Name of .tmx file with content to be extracted",
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding="UTF-8"),
                        help="Name of file in which to write the extracted content",
                        default=sys.stdout)
    args = parser.parse_args()
    extract_map(args.infile, args.outfile)

def extract_map(infile, outfile):
    """ Extract the map cells from the Tiled map file """

    tmx_doc = ElementTree.parse(infile)

    layer_element = tmx_doc.find("./layer")
    width = int(layer_element.attrib["width"])

    # TMX files have the map data as a CSV list of tile numbers
    # (1 indexed, not 0 indexed as you might expect)
    csv_map_data = tmx_doc.find("./layer/data").text

    # Cap the text off in brackets and we have JSON...
    json_map_data = "[" + csv_map_data + "]"
    map_data = json.loads(json_map_data)

    line_buffer = []
    for cell_count, cell in enumerate(map_data):
        row = cell_count // width
        at_row_start = cell_count % width == 0
        if at_row_start or len(line_buffer) == 16:
            if line_buffer:
                outfile.write(" ".join(line_buffer) + "\n")
                line_buffer = []
            if at_row_start:
                outfile.write("# Row {:.<41}\n".format(row))
        line_buffer.append(format(cell - 1, "02X"))  # Cells are 1-indexed, not 0
    if line_buffer:
        outfile.write(" ".join(line_buffer) + "\n")

if __name__ == "__main__":
    main()

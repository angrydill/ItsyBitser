#!/usr/bin/env python3
""" Extract map cell content of a Tiled .tmx file as a commented Hextream """

import sys
import json
from xml.etree import ElementTree

def main(file_path):
    tmx_doc = ElementTree.parse(file_path)

    layer_element = tmx_doc.find("./layer")
    width = int(layer_element.attrib["width"])
    height = int(layer_element.attrib["height"])

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
        if at_row_start:
            if line_buffer:
                print(" ".join(line_buffer))
                line_buffer = []
            #print("# Row {}{}".format(row, "." * 40))
            print("# Row {:.<41}".format(row))
        line_buffer.append(format(cell - 1, "02X"))  # Cells are 1-indexed, not 0
        if len(line_buffer) == 16:
            print(" ".join(line_buffer))
            line_buffer = []
    if line_buffer:
        print(" ".join(line_buffer))

if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
    except IndexError:
        print("Usage: {} <filename>".format(sys.argv[0]))
        exit(1)
    main(file_path)

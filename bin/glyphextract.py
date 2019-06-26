#!/usr/bin/env python3
""" Extract 8x8 monochrome glyphs from a PNG-format "sprite atlas" file """

import sys
import png

BLACK_THRESHOLD = 64


def main(file_path):
    reader = png.Reader(filename=file_path)
    width, height, rgb_contents, metadata = reader.asRGB8()
    mono_content = [] * height
    for row in rgb_contents:
        print("".join([["  ", "[]"][row[i+0] + row[i+1] + row[i+2] > BLACK_THRESHOLD] for i in range(0, 3 * width, 3)]))

if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
    except IndexError:
        print("Usage: {} <filename>".format(sys.argv[0]))
        exit(1)
    main(file_path)

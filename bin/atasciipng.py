#!/usr/bin/env python3
""" Render ATASCII text as a PNG graphic

Copyright 2020 Randy Gill

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import argparse
import zlib
import pickle
import base64
import png


def main():
    """ Process command line arguments and render ATASCII text as a PNG graphic """

    parser = argparse.ArgumentParser(
        description="Utility that renders an ATASCII text file as a PNG graphic, with native Atari 8-bit font."
    )
    parser.add_argument(
        dest="infile",
        type=argparse.FileType("rb"),
        help="Name of file containing ATASCII text"
    )
    parser.add_argument(
        dest="outfile",
        type=argparse.FileType("wb"),
        help="Name of PNG file to create"
    )

    args = parser.parse_args()

    compressed_char_data = base64.decodebytes(bytes(CHARACTER_SET_DATA, encoding="ascii"))
    pickled_char_data = zlib.decompress(compressed_char_data)
    char_data = pickle.loads(pickled_char_data)

    source_lines = args.infile.read().rstrip(b"\x9b").split(b"\x9b")
    args.infile.close()

    png_width = 8 * max([len(line) for line in source_lines])
    png_height = len(source_lines) * 8

    pixels = []
    for i in range(png_height):
        pixels.append([0] * png_width)

    pixel_y = 0
    for source_line in source_lines:
        for scan_line in range(8):
            pixel_x = 0
            for source_byte in source_line:
                char_line_pixels = char_data[source_byte][scan_line]
                for pixel in char_line_pixels:
                    pixels[pixel_y][pixel_x] = pixel
                    pixel_x += 1
            pixel_y += 1

    png_writer =  png.Writer(png_width, png_height, greyscale=True, bitdepth=1)
    png_writer.write(args.outfile, pixels)
    args.outfile.close()

CHARACTER_SET_DATA = """
    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
"""
if __name__ == "__main__":
    main()

#!/usr/bin/env python3
""" Extract 8x8 monochrome glyphs from a PNG-format "sprite atlas" file """

import argparse
import png

BLACK_THRESHOLD = 64
GLYPH_WIDTH = 8
GLYPH_HEIGHT = 8
RGB_LENGTH = 3

class GlyphSet:

    def __init__(self, png_file):
        reader = png.Reader(file=png_file)
        width, height, rgb_content, _ = reader.asRGB8()

        self.rows = height // GLYPH_HEIGHT
        self.columns = width // GLYPH_WIDTH
        self._mono_content = []

        for row in rgb_content:
            self._mono_content.append([
                int(sum(row[i:i+RGB_LENGTH]) > BLACK_THRESHOLD)
                for i in range(0, RGB_LENGTH * width, RGB_LENGTH)
            ])

    def render(self, glyph_indexes=None):
        rendered_glyphs = []
        if glyph_indexes is None:
            glyph_indexes = list(range(0, self.rows * self.columns))
        for glyph_index in glyph_indexes:
            rendered_glyphs.append(self._render_glyph(glyph_index))
        return "\n".join(rendered_glyphs)

    def _render_glyph(self, glyph_index):
        ascii_rows = []
        hex_bytes = []
        for row in self._get_glyph_content(glyph_index):
            hex_bytes.append(format(int("".join([str(pixel) for pixel in row]), 2), "02X"))
            ascii_rows.append("".join([["  ", "[]"][pixel] for pixel in row]))
        body = "\n".join([
            "{} # {}".format(pair[0], pair[1])
            for pair in zip(hex_bytes, ascii_rows)
        ])
        head = "{:#^21}".format(" Glyph " + str(glyph_index) + " ")
        return "{}\n{}\n".format(head, body)

    def _get_glyph_origin(self, glyph_index):
        start_row = glyph_index // self.columns
        start_column = glyph_index % self.columns
        return (start_column * GLYPH_WIDTH, start_row * GLYPH_HEIGHT)

    def _get_glyph_content(self, glyph_index):
        x_pos, y_pos = self._get_glyph_origin(glyph_index)
        glyph_content = [
            row[x_pos:x_pos+GLYPH_WIDTH]
            for row in self._mono_content[y_pos:y_pos + GLYPH_HEIGHT]
        ]
        return glyph_content

def main():
    parser = argparse.ArgumentParser(
        description="Extracts 8x8 monochrome glyphs from a PNG-format \"sprite atlas\" file"
    )
    parser.add_argument(
        dest="png_file",
        type=argparse.FileType("rb"),
        help="Name of .png file to extract from"
    )
    parser.add_argument(
        "-p",
        "--glyph-positions",
        metavar="n",
        type=int, nargs="+",
        help="Relative position(s) (starting with 0) of glyph(s) to extract (default is all)"
    )

    args = parser.parse_args()
    glyphset = GlyphSet(args.png_file)
    print(glyphset.render(args.glyph_positions))

if __name__ == "__main__":
    main()

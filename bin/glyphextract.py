#!/usr/bin/env python3
""" Extract 8x8 monochrome glyphs from a PNG-format "sprite atlas" file """

import sys
import png

BLACK_THRESHOLD = 64
GLYPH_WIDTH = 8
GLYPH_HEIGHT = 8
RGB_LENGTH = 3

class GlyphSet:

    def __init__(self, file_path):
        reader = png.Reader(filename=file_path)
        width, height, rgb_content, _ = reader.asRGB8()
        
        self.rows = height // GLYPH_HEIGHT
        self.columns = width // GLYPH_WIDTH
        self._mono_content = []

        for row in rgb_content:
            #print("".join([["  ", "[]"][sum(row[i:i+RGB_LENGTH]) > BLACK_THRESHOLD] for i in range(0, RGB_LENGTH * width, RGB_LENGTH)]))
            self._mono_content.append([int(sum(row[i:i+RGB_LENGTH]) > BLACK_THRESHOLD) for i in range(0, RGB_LENGTH * width, RGB_LENGTH)])

    def render(self):
        print(self._ascii_render_glyph(7))
        #print(repr(self._get_glyph_content(5)))
        #print("rows={}, cols={}".format(self.rows, self.columns))

    def _ascii_render_glyph(self, glyph_index):
        ascii_rows = []
        for row in self._get_glyph_content(glyph_index):
            ascii_rows.append("".join([["  ", "[]"][pixel] for pixel in row]))
        return "\n".join(ascii_rows)

    def _get_glyph_origin(self, glyph_index):
        start_row = glyph_index // self.columns
        start_column = glyph_index % self.columns
        return (start_column * GLYPH_WIDTH, start_row * GLYPH_HEIGHT)

    def _get_glyph_content(self, glyph_index):
        x, y = self._get_glyph_origin(glyph_index)
        glyph_content = [row[x:x+GLYPH_WIDTH] for row in self._mono_content[y:y + GLYPH_HEIGHT]]
        return glyph_content

def main(file_path):
    glyphset = GlyphSet(file_path)
    glyphset.render()

if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
    except IndexError:
        print("Usage: {} <filename>".format(sys.argv[0]))
        exit(1)
    main(file_path)

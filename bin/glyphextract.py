#!/usr/bin/env python3
""" Extract 8x8 monochrome glyphs from a PNG-format "sprite atlas" file """

import argparse
from itsybitser.glyphset import GlyphSet

def main():
    """ Process command line arguments and use GlyphSet to render selected glyphs """

    def comma_range_list(arg):
        result = []
        for comma_range in arg.split(","):
            extents = comma_range.split("-")
            if len(extents) > 1:
                result.extend(range(int(extents[0]), int(extents[1]) + 1))
            else:
                result.append(int(extents[0]))
        return result

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
        metavar="n,n-n,n,n,n-n",
        type=comma_range_list,
        #nargs=1,
        help="Relative position(s) (starting with 0) of glyph(s) to extract (default is all)"
    )

    args = parser.parse_args()
    glyphset = GlyphSet(args.png_file)
    print(glyphset.render_glyphs(args.glyph_positions))

if __name__ == "__main__":
    main()

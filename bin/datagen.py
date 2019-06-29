#!/usr/bin/env python3
""" Generates Basic DATA statements from Varipacked content """

import sys
import argparse
import textwrap
from itsybitser import varipacker

def main():
    """ Program entry point """

    parser = argparse.ArgumentParser(
        description="Generates Basic DATA statements from Varipacked content"
    )
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding="UTF-8"),
                        help="Name of file with source Varipacked content",
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding="UTF-8"),
                        help="Name of file to which to write generated  DATA statements",
                        default=sys.stdout)
    parser.add_argument("-w", "--width", type=int, default=80,
                        help="Maximum overall line width (default is 80)")
    parser.add_argument("-t", "--basic-type", type=str, default="std",
                        help='"std" for standard Basic (default), "tbx" for Turbo Basic XL')
    args = parser.parse_args()

    width = args.width

    try:
        template, line_start, overhead = {
            "std": ("{} DATA \"{}\"\n", 1, 9),
            "tbx": ("{}D.{}\n", 0, 3),
        }[args.basic_type]
    except KeyError:
        sys.stderr.write(
            "{}: Unrecognized Basic type \"{}\"\n".format(sys.argv[0], args.basic_type)
        )
        exit(1)

    source_content = varipacker.distill(args.infile.read())
    wrapped_content = textwrap.wrap(source_content, width=(width - overhead))
    output_content = [
        template.format(line_count + line_start, line)
        for line_count, line in enumerate(wrapped_content)
    ]
    args.outfile.writelines(output_content)

if __name__ == "__main__":
    main()

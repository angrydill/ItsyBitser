#!/usr/bin/env python3
""" Packs/unpacks Hextream content to/from the Varipacker format """

import sys
import argparse
from itsybitser import hextream, varipacker

def main():

    parser = argparse.ArgumentParser(
        description="Packs/unpacks Hextream content to/from the Varipacker format"
    )
    commands = parser.add_mutually_exclusive_group(required=True)
    commands.add_argument("-p", "--pack", action="store_true",
                          help="Pack Hextream content into Varipacker format")
    commands.add_argument("-u", "--unpack", action="store_true",
                          help="Unpack Varipacker content into Hextream format")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding="UTF-8"),
                        help="Name of file with content to be packed/unpacked",
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding="UTF-8"),
                        help="Name of file in which to write packed/unpacked content",
                        default=sys.stdout)
    parser.add_argument("-c", "--comment", type=str,
                        help="Prepend the output with specified comment string")
    parser.add_argument("-n", "--omit-newline", action="store_true",
                        help="The ending newline character(s) will be omitted from the output")
    args = parser.parse_args()

    source_content = args.infile.read()

    if args.pack:
        binary_content = hextream.decode(source_content)
        output_content = varipacker.encode(binary_content)
    else:
        binary_content = varipacker.decode(varipacker.distill(source_content))
        output_content = hextream.encode(binary_content)

    if args.comment:
        args.outfile.write("# {}\n".format(args.comment))
    args.outfile.write(output_content)
    if not args.omit_newline:
        args.outfile.write("\n")

if __name__ == "__main__":
    main()

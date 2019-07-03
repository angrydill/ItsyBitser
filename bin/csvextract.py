#!/usr/bin/env python3
""" Extract column(S) from CSV file and encode in Hextream format """

import sys
import argparse
import textwrap
import csv

def main():
    """ Program entry point """

    def column_definition_list(arg):
        result = []
        for column_definition in arg.split(","):
            definition = column_definition.split(":")
            heading = definition[0]
            try:
                width = int(definition[1])
            except IndexError:
                width = 1
            if width < 1:
                raise ValueError("{}: Width must be greater than zero".format(sys.argv[0]))
            result.append({"heading": heading, "width": width})
        return result

    parser = argparse.ArgumentParser(
        description="Extract column(S) from CSV file and encode in Hextream format"
    )
    parser.add_argument(
        dest="infile", nargs="?", default=sys.stdin,
        type=argparse.FileType("r", encoding="UTF-8"),
        help="CSV file to extract data from"
    )
    parser.add_argument(
        dest="outfile", nargs="?", default=sys.stdout,
        type=argparse.FileType("w", encoding="UTF-8"),
        help="File to write extracted data to (in Hextream format)"
    )
    parser.add_argument(
        "-c",
        "--columns",
        metavar="heading:width[,heading:width,...]",
        type=column_definition_list,
        help="columns to extract; heading is column heading (line 1), width is in bytes"
    )
    parser.add_argument(
        "-m", "--comment", default="",
        type=str,
        help="Comment string to include at beginning of file"
    )
    args = parser.parse_args()

    extract_csv_content(args.infile, args.outfile, args.columns, args.comment)

def extract_csv_content(infile, outfile, columns, comment):
    """ Extract the content, transform, and write to the output file """

    hex_content = []
    reader = csv.DictReader(infile)
    for row in reader:
        line_content = []
        for column in columns:
            try:
                value = row[column["heading"]]
            except KeyError:
                sys.stderr.write("{}: Column with heading \"{}\" not found.\n".format(
                    sys.argv[0], column["heading"]))
                exit(1)
            try:
                value = int(value)
            except ValueError:
                sys.stderr.write("{}: Extracted value \"{}\" is not an integer\n".format(
                    sys.argv[0], value))
                exit(1)
            try:
                width = int(column["width"]) * 2
            except (KeyError, ValueError):
                width = 2
            hex_format = "0{}X".format(width)
            line_content.extend(reversed(textwrap.wrap(format(value, hex_format), 2)))
        hex_content.append(" ".join(line_content))
    if comment:
        comment = "# {}\n".format(comment)
    hex_content = "{}{}\n".format(comment, "\n".join(hex_content))
    outfile.write(hex_content)

if __name__ == "__main__":
    main()

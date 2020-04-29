#!/usr/bin/env python3
""" Generate colorized HTML listing of FastBasic code """

import sys
import re
from enum import Enum
import argparse

# The following encoding (basically an extension of Latin-1 typically
# associated with MS Windows) was chosen as it has a usable character
# glyph at 9b hex (ATASCII line feed). Note that UniCode and many others
# reserve that code and those around it for control characters.
ENCODING = "cp1252"
ATASCII_LINEFEED = str(b"\x9b", encoding=ENCODING)


class ScanState(Enum):
    """ Current state while lexing the BASIC code  """
    NEUTRAL = 0
    CODE = 1
    STRING = 2
    COMMENT = 3


def main():
    """ Program entry point """

    parser = argparse.ArgumentParser(
        description="Generate colorized HTML listing of FastBasic code"
    )
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding=ENCODING),
                        help="Name of FastBasic source code (ASCII/ATASCII) file",
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding=ENCODING),
                        help="Name of file in which to write the HTML listing",
                        default=sys.stdout)
    args = parser.parse_args()
    make_listing(args.infile, args.outfile)

def make_listing(infile, outfile):
    """ Generate the HTML listing """

    source = infile.read()
    output_html = process_source(source)
    outfile.write(output_html)

def process_source(source):
    """ Scans source, marks up lines with html """
    line_terminators = "\n\r" + ATASCII_LINEFEED
    statement_terminators = ":" + line_terminators
    style_block = """
        <style>
        pre {
            color: #bbbbbb;
            background-color: #111111;
            padding: 1em 1em 1em 1em;
            overflow-wrap: break-word;
            white-space: pre-wrap;
        }
        .comment {
            color: #33dd33;
        }
        .string {
            color: #ff8833;
        }
        </style>
    """
    output_html = ['<html><head>', style_block, '\n</head><body>\n<pre><code><span class="code">']
    state = ScanState.NEUTRAL
    prev_state = ScanState.NEUTRAL
    element_class = "code"
    for char in source:
        if char == "<":
            char = "&lt;"
        elif char == ">":
            char = "&gt;"
        elif char == "&":
            char = "&amp;"
        if state == ScanState.NEUTRAL:
            if char == '"':
                state = ScanState.STRING
            elif char in "'.":
                state = ScanState.COMMENT
            elif char not in " " + statement_terminators:
                state = ScanState.CODE
        elif state == ScanState.CODE:
            if char in statement_terminators:
                state = ScanState.NEUTRAL
            elif char == '"':
                state = ScanState.STRING
            elif char == "'":
                state = ScanState.COMMENT
        elif state == ScanState.STRING:
            if char == '"':
                state = ScanState.CODE
        else:    # state is ScanState.COMMENT (by elimination of all others)
            if char in line_terminators:
                state = ScanState.NEUTRAL
        if char in line_terminators:
            char = "\n"
        if state != prev_state:
            post_char = ""
            if state == ScanState.STRING:
                new_element_class = "string"
                post_char = char
                char = ""
            elif state == ScanState.COMMENT:
                new_element_class = "comment"
            else:
                new_element_class = "code"
            prev_state = state
            if new_element_class != element_class:
                element_class = new_element_class
                output_html.append('{0}</span><span class="{1}">{2}'.format(char, element_class, post_char))
            else:
                output_html.append(post_char + char)
        else:
            output_html.append(char)

    output_html.append("</code></pre></body></html>")
    return "".join(output_html)

if __name__ == "__main__":
    main()

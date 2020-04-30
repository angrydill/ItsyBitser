#!/usr/bin/env python3
""" Abbreviate FastBasic code, strip comments and pack into fewest possible lines """

import sys
import re
from enum import Enum
import argparse

DEFAULT_MAX_LINE_WIDTH = 255
# The following encoding (basically an extension of Latin-1 typically
# associated with MS Windows) was chosen as it has a usable character
# glyph at 9b hex (ATASCII line feed). Note that UniCode and many others
# reserve that code and those around it for control characters.
ENCODING = "cp1252"
ATASCII_LINEFEED = str(b"\x9b", encoding=ENCODING)

ABBREVIATIONS = [
    ["-MOVE", "-."],
    ["BGET", "BG."],
    ["BPUT", "BP."],
    ["BGET", "BG."],
    ["COLOR", "C."],
    ["DATA", "DA."],
    ["DEC", "DE."],
    ["DIM", "DI."],
    ["DPOKE", "D."],
    ["DRAWTO", "DR."],
    ["ELIF", "ELI."],
    ["ELSE", "E."],
    ["ENDIF", "END."],
    ["ENDPROC", "ENDP."],
    ["EXEC", "EXE."],
    ["EXIT", "EX."],
    ["FCOLOR", "FC."],
    ["FILLTO", "FI."],
    ["FOR", "F."],
    ["GET", "GE."],
    ["GRAPHICS", "G."],
    ["IF", "I."],
    ["INPUT", "IN."],
    ["LOOP", "L."],
    ["MOVE", "M."],
    ["MSET", "MS."],
    ["NEXT", "N."],
    ["OPEN", "O."],
    ["PAUSE", "PA."],
    ["PLOT", "PL."],
    ["PMGRAPHICS", "PM."],
    ["PMHPOS", "PMH."],
    ["POKE", "P."],
    ["POSITION", "POS."],
    ["PRINT", "?"],
    ["PROC", "PRO."],
    ["PUT", "PU."],
    ["REPEAT", "R."],
    ["SETCOLOR", "SE."],
    ["SOUND", "SO."],
    ["STEP", "S."],
    ["THEN", "T."],
    ["UNTIL", "U."],
    ["WEND", "WE."],
    ["WHILE", "W."],
    ["XIO", "X."]
]

class ScanState(Enum):
    """ Current state while lexing the BASIC code  """
    NEUTRAL = 0
    CODE = 1
    STRING = 2
    HEX = 3
    COMMENT = 4


def main():
    """ Program entry point """

    parser = argparse.ArgumentParser(
        description="Strip comments, abbreviate, and pack FastBasic code into fewest possible lines"
    )
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding=ENCODING),
                        help="Name of FastBasic source code (ASCII/ATASCII) file",
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding=ENCODING),
                        help="Name of file in which to write the minified content",
                        default=sys.stdout)
    parser.add_argument('-w', '--width', type=int, metavar='width', default=DEFAULT_MAX_LINE_WIDTH,
                        help='Maximum line width of the generated source code')
    args = parser.parse_args()
    minify(args.infile, args.outfile, args.width)

def minify(infile, outfile, max_width):
    """ Abbreviate and compact code to fit as few as possible lines """

    source = infile.read()
    statement_list = scan_for_statements(source)
    line_list = build_output_line_list(statement_list, max_width)
    outfile.write(ATASCII_LINEFEED.join(line_list))

def scan_for_statements(source):
    """ Scans source, builds statement list while ignoring comments and expanding abbreviations """
    line_terminators = "\n\r" + ATASCII_LINEFEED
    statement_terminators = ":'" + line_terminators
    statement_list = []
    accumulator = []
    state = ScanState.NEUTRAL
    last_space_position = None
    match_tree = build_match_tree(ABBREVIATIONS)
    source += ":"   # Colon is a sentinel needed to resolve final statement
    for char in source:
        if state == ScanState.NEUTRAL:
            if char == '"':
                state = ScanState.STRING
                accumulator.append('"')
            elif char in "'.":
                state = ScanState.COMMENT
            elif char not in " " + statement_terminators:
                state = ScanState.CODE
                accumulator.append(char)
        elif state == ScanState.CODE:
            if char in statement_terminators:
                statement = abbreviate(match_tree, "".join(accumulator))
                statement_list.append(statement)
                accumulator = []
                if char == "'":
                    state = ScanState.COMMENT
                else:
                    state = ScanState.NEUTRAL
            elif char != " ":
                accumulator.append(char)
                if char == '"':
                    state = ScanState.STRING
                else:
                    tail_window = ("".join(accumulator[-4:])).upper()
                    if re.match("[A-Z]AND", tail_window) and len(accumulator) - last_space_position == 3:
                        accumulator.insert(last_space_position, " ")
                    elif re.match(".[A-Z]OR", tail_window) and len(accumulator) - last_space_position == 2:
                        accumulator.insert(last_space_position, " ")
            else:
                last_space_position = len(accumulator)
        elif state == ScanState.STRING:
            if char == "$":
                state = ScanState.HEX
                hex_accumulator = []
            else:
                accumulator.append(char)
                if char == '"':
                    state = ScanState.CODE
        elif state == ScanState.HEX:
            hex_accumulator.append(char)
            if re.match("[0-9a-fA-F]", char):
                if len(hex_accumulator) == 2:
                    escape_value = int("".join(hex_accumulator), 16)
                    accumulator.append(chr(escape_value))
                    state = ScanState.STRING
            else:
                accumulator.append("$")
                accumulator.extend(hex_accumulator)
                state = ScanState.STRING
        else:    # state is ScanState.COMMENT (by elimination of all others)
            if char in line_terminators:
                state = ScanState.NEUTRAL
    return statement_list

def build_output_line_list(statement_list, max_width):
    """ build lines of code with statments separated by colons """
    line_list = []
    line = ""
    for statement in statement_list:
        if line:
            candidate_line = line + ":" + statement
            if len(candidate_line) > max_width:
                line_list.append(line)
                line = statement
            else:
                line = candidate_line
        else:
            line = statement
    line_list.extend([line, ""])    # Empty element so generated source ends in line feed
    return line_list

def abbreviate(match_tree, statement):
    """ Substitute abbreviation for statement keyword, if former exists """

    result = statement
    current_node = match_tree
    for position, letter in enumerate(statement.upper()):
        current_node = current_node.get(letter)
        if not isinstance(current_node, dict):
            if isinstance(current_node, str):
                result = current_node + statement[(position + 1):]
            break
    return result

def build_match_tree(abbreviation_list):
    """ Build the tree used to look up abbreviations """
    match_tree = {}
    for word, abbreviation in abbreviation_list:
        tree_node = match_tree
        for letter in word[:-1]:
            if letter not in tree_node:
                tree_node[letter] = {}
            tree_node = tree_node[letter]
        tree_node[word[-1]] = abbreviation
    return match_tree

def test_abbreviate_nothing():
    """ test abbreviate() with empty string arg. """
    statement = ""
    assert abbreviate(build_match_tree(ABBREVIATIONS), statement) == ""

def test_abbreviate_miss():
    """ test abbreviate() with xxx """
    statement = "PEEK(1234)"
    assert abbreviate(build_match_tree(ABBREVIATIONS), statement) == "PEEK(1234)"
    statement = "QUIT"
    assert abbreviate(build_match_tree(ABBREVIATIONS), statement) == "QUIT"
    statement = "ENDPRO"
    assert abbreviate(build_match_tree(ABBREVIATIONS), statement) == "ENDPRO"
    statement = "POSITIOM"
    assert abbreviate(build_match_tree(ABBREVIATIONS), statement) == "POSITIOM"

def test_abbreviate_all():
    """ test abbreviate() with xxx """
    statement = "ENDPROC"
    assert abbreviate(build_match_tree(ABBREVIATIONS), statement) == "ENDP."
    statement = "POSITION"
    assert abbreviate(build_match_tree(ABBREVIATIONS), statement) == "POS."

def test_abbreviate_partial():
    """ test abbreviate() with xxx """
    statement = "ENDPROC A"
    assert abbreviate(build_match_tree(ABBREVIATIONS), statement) == "ENDP. A"
    statement = "POSITION10,5"
    assert abbreviate(build_match_tree(ABBREVIATIONS), statement) == "POS.10,5"

def test_build_match_tree_with_empty():
    """ test build_match_tree() with empty list for input """
    abbreviation_list = []
    expected_tree = {}
    tree = build_match_tree(abbreviation_list)
    assert repr(tree) == repr(expected_tree)

def test_build_match_tree_with_pairs():
    """ test build_match_tree() with list of pairs for input """
    abbreviation_list = [["ELIF", "ELI."], ["ELSE", "E."]]
    expected_tree = {"E": {"L": {"I": {"F": "ELI."}, "S": {"E": "E."}}}}
    tree = build_match_tree(abbreviation_list)
    assert repr(tree) == repr(expected_tree)

if __name__ == "__main__":
    main()

""" Common functionality between varipacker and hextream modules """

import re

def compare(content1, content2):
    """ Compares two strings

    This compares two strings, while ignoring any whitespace characters
    (space, tab, carriage return, line feed, form feed, or vertical
    tab), and any comments (character sequences starting with "#" and
    extending to the end-of-line.

    - if strings are the same, will return -1
    - if strings are different, will return the (0-based) index of the
      first character where they differ """

    result = -1
    distilled_content1 = distill(content1)
    distilled_content2 = distill(content2)
    if distilled_content1 != distilled_content2:
        result = 0
        while distilled_content1[result] == distilled_content2[result]:
            result += 1
    return result

def distill(content):
    """ Removes whitespace and comments from string

    This removes any whitespace characters (space, tab, carriage return,
    line feed, form feed, and vertical tab), and any comments (character
    sequences starting with "#" and extending to the end-of-line from the
    passed-in string. """

    # Eliminate comments
    result = re.sub("#.*$", "", content, flags=re.MULTILINE)
    # Eliminate all whitespace (split by default splits on any WS char)
    result = ''.join(result.split())
    return result

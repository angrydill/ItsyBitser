""" Module to encode and decode binary data as ASCII hexadecimal characters """

import textwrap
from itsybitser import asciiencoding

WRAP_BYTES_PER_LINE = 16

def compare(content1, content2):
    """ Compares two hextreams

    This compares two hextreams, while ignoring any whitespace characters
    (space, tab, carriage return, line feed, form feed, or vertical
    tab), and any comments (character sequences starting with "#" and
    extending to the end-of-line.

    - if hextreams are the same, will return -1
    - if hextreams are different, will return the (0-based) index of the
      first character where they differ """
    return asciiencoding.compare(distill(content1), distill(content2))

def decode(content):
    """ Decode binary data from ASCII hexadecimal characters """
    return bytes.fromhex(distill(content))

def distill(content):
    """ Strip out comments, whitespace, and hex string prefix characters """
    result = asciiencoding.distill(content.upper())
    filter_prefix_characters = str.maketrans("", "", "\\xX$")
    result = result.replace("0X", "").translate(filter_prefix_characters)
    return result

def encode(content):
    """ Encode binary data as ASCII hexadecimal characters """
    result = " ".join([format(byte, "02X") for byte in content])
    # Break into lines of no more than 16 byte representations
    result = "\n".join(textwrap.wrap(result, width=(WRAP_BYTES_PER_LINE * 3 - 1)))
    return result

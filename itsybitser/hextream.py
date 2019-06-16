""" Class to encode and decode binary data as ASCII hexadecimal characters """

import textwrap
from itsybitser.asciiencoding import AsciiEncoding

WRAP_BYTES_PER_LINE = 16
HEX_RADIX = 16


class Hextream(AsciiEncoding):
    """ Class to encode and decode binary data as ASCII hexadecimal characters """

    def __init__(self):
        super().__init__()
        self.filter_prefix_characters = str.maketrans("", "", "\\xX$")

    def decode(self, content):
        """ Decode binary data from ASCII hexadecimal characters """
        result = self.distill(content)
        result = bytes([int(hex_string, HEX_RADIX) for hex_string in textwrap.wrap(result, 2)])
        return result

    def distill(self, content):
        """ Strip out comments, whitespace, and hex string prefix characters """
        result = super().distill(content.upper())
        result = result.replace("0X", "").translate(self.filter_prefix_characters)
        return result

    @staticmethod
    def encode(content):
        """ Encode binary data as ASCII hexadecimal characters """
        result = " ".join([format(byte, "02X") for byte in content])
        # Break into lines of no more than 16 byte representations
        result = "\n".join(textwrap.wrap(result, width=(WRAP_BYTES_PER_LINE * 3 - 1)))
        return result

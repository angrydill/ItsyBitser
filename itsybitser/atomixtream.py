""" Text encodes binary data, compressing where feasible """

from enum import Enum
from itsybitser.asciiencoding import AsciiEncoding

OFFSET = 48
RADIX = 64


class Atomixtream(AsciiEncoding):
    """ Text encodes binary data, compressing where feasible """

    def __init__(self):
        super().__init__()

    def decode(self, content):
        """ Decode binary data from Hextream (ASCII) """
        result = None
        return result

    def encode(self, content):
        """ Encode binary data as Hextream (ASCII) """
        result = None
        return result

    def encode_chunk(self, content, encoding):
        """ Encodes a byte sequence using specified encoding  """

        length = len(content)

        if encoding == self.Encoding.SEXTET_STREAM:
            result = "".join([chr(byte + OFFSET) for byte in content])
  
        elif encoding == self.Encoding.TRIAD_STREAM:
            result = []
            for i in range(0, (length + 1) // 2):
                byte = content[2 * i]
                try:
                    byte += content[2 * i + 1] * 8
                except IndexError:
                    pass
                result.append(chr(byte + OFFSET))
            result = "".join(result)

        elif encoding == self.Encoding.BASIC64:
            result = []
            for i in range(0, length):
                if not i % 3:
                    result.append(0)
                    hi_bits_index = len(result) - 1
                byte = content[i]
                hi_bits_shift = 2 * (3 - i % 3)
                result[hi_bits_index] += (byte & 192) >> hi_bits_shift
                result.append(byte & RADIX - 1)
            result = "".join([chr(byte + OFFSET) for byte in result])

        elif encoding == self.Encoding.SEXTET_RUN:
            if length:
                result = chr(content[0] + OFFSET)
            else:
                result = ""

        elif encoding == self.Encoding.OCTET_RUN:
            if length:
                result = chr(content[0] // RADIX + OFFSET) + chr((content[0] & (RADIX - 1)) + OFFSET)
            else:
                result = ""

        result = self.__encode_header(encoding, length) + result
        return result

    def encode_gap(self, length):
        """ Encodes instruction for decoder to skip forward length bytes """
        result = self.__encode_header(self.Encoding.GAP, length)
        return result

    def encode_terminus(self):
        """ Encodes indicator that there are no more chunks to decode """
        result = None
        return result

    class Encoding(Enum):
        """ Indicates technique to use when encoding a chunk """
        GAP = 0
        OCTET_RUN = 1
        SEXTET_RUN = 2
        TRIAD_STREAM = 3
        SEXTET_STREAM = 4
        HEADER = 5
        BASIC64 = 7

    def __encode_header(self, encoding, length):
        result = chr(encoding.value + length // RADIX * 8 + OFFSET) + chr(length % RADIX + OFFSET)
        return result

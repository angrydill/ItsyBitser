""" Text-encodes binary data, compressing where feasible """

from enum import Enum
from itsybitser.asciiencoding import AsciiEncoding

OFFSET = 48
RADIX = 64
SEXTET_MASK = 0b00111111
HIGH_BITS_MASK = 0b11000000
GROUP_LENGTH = 3


class VariPacker(AsciiEncoding):
    """ Text-encodes binary data, compressing where feasible """

    def __init__(self):
        super().__init__()
        self.encoders = {
            self.Encoding.LINEAR64: self.__encode_linear64,
            self.Encoding.OCTET_RUN: self.__encode_octet_run,
            self.Encoding.SEXTET_RUN: self.__encode_sextet_run,
            self.Encoding.SEXTET_STREAM: self.__encode_sextet_stream,
            self.Encoding.TRIAD_STREAM: self.__encode_triad_stream
        }

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
        result = self.encoders[encoding](content)
        result = self.__encode_header(encoding, len(content)) + result
        return result

    def encode_gap(self, length):
        """ Encodes instruction for decoder to skip forward length bytes """
        result = self.__encode_header(self.Encoding.GAP, length)
        return result

    @staticmethod
    def encode_terminus():
        """ Encodes indicator that there are no more chunks to decode """
        result = "00"
        return result

    class Encoding(Enum):
        """ Indicates technique to use when encoding a chunk """
        GAP = 0
        OCTET_RUN = 1
        SEXTET_RUN = 2
        TRIAD_STREAM = 3
        SEXTET_STREAM = 4
        HEADER = 5
        LINEAR64 = 7

    @staticmethod
    def __encode_linear64(content):
        result = []
        for content_index, byte in enumerate(content):
            group_position = content_index % GROUP_LENGTH
            if not group_position:
                high_bits_index = len(result)
                result.append(0)
            high_bits_shift = 2 * (GROUP_LENGTH - group_position)
            result[high_bits_index] += (byte & HIGH_BITS_MASK) >> high_bits_shift
            result.append(byte & SEXTET_MASK)
        result = "".join([chr(byte + OFFSET) for byte in result])
        return result

    @staticmethod
    def __encode_header(encoding, length):
        result = (
            chr(encoding.value + length // RADIX * 8 + OFFSET) +
            chr((length & SEXTET_MASK) + OFFSET)
        )
        return result

    @staticmethod
    def __encode_octet_run(content):
        if content:
            result = (
                chr(content[0] // RADIX + OFFSET) +
                chr((content[0] & SEXTET_MASK) + OFFSET)
            )
        else:
            result = ""
        return result

    @staticmethod
    def __encode_sextet_run(content):
        if content:
            result = chr(content[0] + OFFSET)
        else:
            result = ""
        return result

    @staticmethod
    def __encode_sextet_stream(content):
        result = "".join([chr(byte + OFFSET) for byte in content])
        return result

    @staticmethod
    def __encode_triad_stream(content):
        result = []
        for index in range(0, len(content), 2):
            byte = content[index]
            try:
                byte += content[index + 1] << 3
            except IndexError:
                pass
            result.append(chr(byte + OFFSET))
        result = "".join(result)
        return result

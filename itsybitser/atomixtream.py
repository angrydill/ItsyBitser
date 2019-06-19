""" Text encodes binary data, compressing where feasible """

from enum import Enum
from itsybitser.asciiencoding import AsciiEncoding

OFFSET = 48
RADIX = 64
SIX_BIT_MASK = 0b00111111
HI_BITS_MASK = 0b11000000


class Atomixtream(AsciiEncoding):
    """ Text encodes binary data, compressing where feasible """

    def __init__(self):
        super().__init__()
        self.encoders = {
            self.Encoding.BASIC64: self.__encode_basic64,
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

        length = len(content)

        if encoding == self.Encoding.SEXTET_STREAM:
            result = self.__encode_sextet_stream(content)
        elif encoding == self.Encoding.TRIAD_STREAM:
            result = self.__encode_triad_stream(content)
        elif encoding == self.Encoding.BASIC64:
            result = self.__encode_basic64(content)
        elif encoding == self.Encoding.SEXTET_RUN:
            result = self.__encode_sextet_run(content)
        elif encoding == self.Encoding.OCTET_RUN:
            result = self.__encode_octet_run(content)

        result = self.__encode_header(encoding, length) + result
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
        BASIC64 = 7

    @staticmethod
    def __encode_basic64(content):
        result = []
        length = len(content)
        for i in range(0, length):
            if not i % 3:
                result.append(0)
                hi_bits_index = len(result) - 1
            byte = content[i]
            hi_bits_shift = 2 * (3 - i % 3)
            result[hi_bits_index] += (byte & HI_BITS_MASK) >> hi_bits_shift
            result.append(byte & SIX_BIT_MASK)
        result = "".join([chr(byte + OFFSET) for byte in result])
        return result

    @staticmethod
    def __encode_header(encoding, length):
        result = (
            chr(encoding.value + length // RADIX * 8 + OFFSET) +
            chr((length & SIX_BIT_MASK) + OFFSET)
        )
        return result

    @staticmethod
    def __encode_octet_run(content):
        length = len(content)
        if length:
            result = (
                chr(content[0] // RADIX + OFFSET) +
                chr((content[0] & SIX_BIT_MASK) + OFFSET)
            )
        else:
            result = ""
        return result

    @staticmethod
    def __encode_sextet_run(content):
        length = len(content)
        if length:
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
        length = len(content)
        result = []
        for i in range(0, (length + 1) // 2):
            index = 2 * i
            byte = content[index]
            try:
                byte += content[index + 1] << 3
            except IndexError:
                pass
            result.append(chr(byte + OFFSET))
        result = "".join(result)
        return result

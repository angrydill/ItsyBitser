""" Text-encodes binary data, compressing where feasible """

from enum import Enum
from itsybitser import asciiencoding

OFFSET = 48
RADIX = 64
SEXTET_MASK = 0b00111111
HIGH_BITS_MASK = 0b11000000
GROUP_LENGTH = 3


class Encoding(Enum):
    """ Indicates technique to use when encoding a chunk """
    GAP = 0
    OCTET_RUN = 1
    SEXTET_RUN = 2
    TRIAD_STREAM = 3
    SEXTET_STREAM = 4
    HEADER = 5
    LINEAR64 = 7


def compare(content1, content2):
    """ Compares two VariPacker strings

    This compares two VariPacker strings, while ignoring any whitespace
    characters (space, tab, carriage return, line feed, form feed, or
    vertical tab), and any comments (character sequences starting with
    "#" and extending to the end-of-line.

    - if they are the same, will return -1
    - if they differ, will return the (0-based) index of the
      first character where they differ """
    #return asciiencoding.compare(distill(content1), distill(content2))
    return None

def decode(content):
    """ Decode binary data from VariPacker content (ASCII) """
    result = None
    return result

def distill(content):
    """ Strip out comments and whitespace from VariPacker content """
    #return asciiencoding.distill(content)
    return None

def encode(content):
    """ Encode binary content in VariPacker format (ASCII) """

    encoded_chunks = {}
    source_buffer = [byte for byte in content]
    source_buffer.append(None)   # Sentinal

    for encoding in (Encoding.SEXTET_RUN, Encoding.OCTET_RUN, Encoding.LINEAR64):
        run_encoding = False
        if encoding in (Encoding.SEXTET_RUN, Encoding.OCTET_RUN):
            run_encoding = True
        value_limit = 0xff
        if encoding == Encoding.SEXTET_RUN:
            value_limit = 0x3f
        source_chunk = []
        start_index = 0
        chunk_finished = False
        for index, byte in enumerate(source_buffer):
            if byte is None or byte > value_limit:
                chunk_finished = True
            elif run_encoding and source_chunk and byte != source_chunk[-1]:
                chunk_finished = True
            else:
                source_chunk.append(byte)
                chunk_finished = len(source_chunk) >= 511
            if chunk_finished:
                chunk_length = len(source_chunk)
                if chunk_length >= 6 or (source_chunk and encoding == Encoding.LINEAR64):
                    source_chunk = b"".join([bytes([byte]) for byte in source_chunk])
                    encoded_chunks[start_index] = encode_chunk(source_chunk, encoding)
                    source_buffer[start_index:start_index + chunk_length] = [None] * chunk_length
                start_index = index + 1
                source_chunk = []
                chunk_finished = False
    result = "".join([chunk for (_, chunk) in sorted(encoded_chunks.items())])
    return result + encode_terminus()

def encode_chunk(content, encoding):
    """ Encodes a byte sequence using specified encoding  """
    result = {
        Encoding.LINEAR64: _encode_linear64,
        Encoding.OCTET_RUN: _encode_octet_run,
        Encoding.SEXTET_RUN: _encode_sextet_run,
        Encoding.SEXTET_STREAM: _encode_sextet_stream,
        Encoding.TRIAD_STREAM: _encode_triad_stream
    }[encoding](content)
    return _encode_header(encoding, len(content)) + result

def encode_gap(length):
    """ Encodes instruction for decoder to skip forward length bytes """
    return _encode_header(Encoding.GAP, length)

def encode_terminus():
    """ Encodes indicator that there are no more chunks to decode """
    return "00"

def _encode_linear64(content):
    result = []
    for content_index, byte in enumerate(content):
        group_position = content_index % GROUP_LENGTH
        if not group_position:
            high_bits_index = len(result)
            result.append(0)
        high_bits_shift = 2 * (GROUP_LENGTH - group_position)
        result[high_bits_index] += (byte & HIGH_BITS_MASK) >> high_bits_shift
        result.append(byte & SEXTET_MASK)
    return "".join([chr(byte + OFFSET) for byte in result])

def _encode_header(encoding, length):
    result = (
        chr(encoding.value + length // RADIX * 8 + OFFSET) +
        chr((length & SEXTET_MASK) + OFFSET)
    )
    return result

def _encode_octet_run(content):
    if content:
        result = (
            chr(content[0] // RADIX + OFFSET) +
            chr((content[0] & SEXTET_MASK) + OFFSET)
        )
    else:
        result = ""
    return result

def _encode_sextet_run(content):
    if content:
        result = chr(content[0] + OFFSET)
    else:
        result = ""
    return result

def _encode_sextet_stream(content):
    return "".join([chr(byte + OFFSET) for byte in content])

def _encode_triad_stream(content):
    result = []
    for index in range(0, len(content), 2):
        byte = content[index]
        try:
            byte += content[index + 1] << 3
        except IndexError:
            pass
        result.append(chr(byte + OFFSET))
    return "".join(result)

""" Text-encodes binary data, compressing where feasible """

from enum import Enum
from itsybitser import asciiencoding

OFFSET = 48
RADIX = 64
HIGH_BITS_MASK = 0b11000000
SEXTET_MASK = 0b00111111
HIGH_TRIAD_MASK = 0b00111000
LOW_TRIAD_MASK = 0b00000111
LOW_DYAD_MASK = 0b00000011
LINEAR64_GROUP_LENGTH = 3
MAX_CHUNK_LENGTH = 511


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
    return asciiencoding.compare(distill(content1), distill(content2))

def decode(content):
    """ Decode binary data from VariPacker content (ASCII) """

    encoding_properties = {
        #             (encoding, cycle length, is run encoding)
        Encoding.GAP: (Encoding.GAP, 1, False),
        Encoding.HEADER: (Encoding.HEADER, 2, False),
        Encoding.LINEAR64: (Encoding.LINEAR64, 4, False),
        Encoding.OCTET_RUN: (Encoding.OCTET_RUN, 2, True),
        Encoding.SEXTET_RUN: (Encoding.SEXTET_RUN, 1, True),
        Encoding.SEXTET_STREAM: (Encoding.SEXTET_STREAM, 1, False),
        Encoding.TRIAD_STREAM: (Encoding.TRIAD_STREAM, 1, False)
    }

    result = bytearray()
    encoding, cycle_length, is_run_encoding = encoding_properties[Encoding.HEADER]
    cycle_count = 0

    for char in content:
        sextet = ord(char) - OFFSET
        if cycle_length > 1 and cycle_count == 0:
            holding_sextet = sextet
        else:
            if encoding == Encoding.HEADER:
                encoding, cycle_length, is_run_encoding = encoding_properties[
                    Encoding(holding_sextet & LOW_TRIAD_MASK)
                ]
                remaining_bytes = ((holding_sextet & HIGH_TRIAD_MASK) << 3) + sextet
                holding_sextet = 0
                cycle_count = -1
                if encoding == Encoding.GAP:
                    result.extend([0] * remaining_bytes)
                    encoding, cycle_length, is_run_encoding = encoding_properties[Encoding.HEADER]
            else:
                if is_run_encoding:   # SEXTET_RUN or OCTET_RUN
                    result.extend([(holding_sextet << 6) + sextet] * remaining_bytes)
                    remaining_bytes = 1
                elif encoding == Encoding.TRIAD_STREAM:
                    result.append(sextet & LOW_TRIAD_MASK)
                    if remaining_bytes > 1:
                        result.append((sextet & HIGH_TRIAD_MASK) >> 3)
                        remaining_bytes -= 1
                else:   # SEXTET_STREAM or LINEAR64
                    result.append(((holding_sextet & LOW_DYAD_MASK) << 6) + sextet)
                    holding_sextet = holding_sextet >> 2
                remaining_bytes -= 1
                if not remaining_bytes:
                    encoding, cycle_length, is_run_encoding = encoding_properties[Encoding.HEADER]
                    cycle_count = -1
        cycle_count = (cycle_count + 1) % cycle_length
    return bytes(result)

def distill(content):
    """ Strip out comments and whitespace from VariPacker content """
    return asciiencoding.distill(content)

def encode(content):
    """ Encode binary content in VariPacker format (ASCII) """

    # TODO optimize (consider pre-switch (2) and post-swith (2) overhead as
    # negative modifiers to min viable length), then refactor
    encoded_chunks = {}
    source_buffer = [byte for byte in content]
    source_buffer.append(None)   # Sentinal

    for encoding in (
            Encoding.SEXTET_RUN, Encoding.OCTET_RUN, Encoding.TRIAD_STREAM,
            Encoding.SEXTET_STREAM, Encoding.LINEAR64
        ):
        value_limit, min_viable_length, is_run_encoding = {
            Encoding.LINEAR64: (0xff, 1, False),
            Encoding.OCTET_RUN: (0xff, 7, True),
            Encoding.SEXTET_RUN: (0x3f, 6, True),
            Encoding.SEXTET_STREAM: (0x3f, 14, False),
            Encoding.TRIAD_STREAM: (0x07, 6, False)
        }[encoding]

        source_chunk = []
        start_index = 0
        chunk_finished = False

        for index, byte in enumerate(source_buffer):
            if byte is None or byte > value_limit:
                chunk_finished = True
            elif is_run_encoding and source_chunk and byte != source_chunk[-1]:
                # If this is different from the last byte then the run is done
                chunk_finished = True
            else:
                source_chunk.append(byte)
                chunk_finished = len(source_chunk) >= MAX_CHUNK_LENGTH
            if chunk_finished:
                chunk_length = len(source_chunk)
                if chunk_length >= min_viable_length:
                    source_chunk = b"".join([bytes([byte]) for byte in source_chunk])
                    encoded_chunks[start_index] = encode_chunk(source_chunk, encoding)
                    # Fill region of the chunk in the buffer with Nones, so it
                    # doesn't get encoded on the next pass
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
        group_position = content_index % LINEAR64_GROUP_LENGTH
        if not group_position:
            high_bits_index = len(result)
            result.append(0)
        high_bits_shift = 2 * (LINEAR64_GROUP_LENGTH - group_position)
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

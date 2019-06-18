""" Unit test cases for Atomixtream class """

from itsybitser.atomixtream import Atomixtream

def test_encode_sextet_stream():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"\x00\x01\x3e\x3f\x3f\x3e\x01\x00",
        Atomixtream.Encoding.SEXTET_STREAM
    )
    assert result == "4801noon10"

def test_encode_sextet_stream_empty():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"",
        Atomixtream.Encoding.SEXTET_STREAM
    )
    assert result == "40"

def test_encode_sextet_stream_full():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"\x2a" * 511,
        Atomixtream.Encoding.SEXTET_STREAM
    )
    assert result == "lo" + "Z" * 511

def test_encode_triad_stream():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"\x00\x01\x06\x07\x07\x06\x01\x00",
        Atomixtream.Encoding.TRIAD_STREAM
    )
    assert result == "388ng1"

def test_encode_triad_stream_empty():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"",
        Atomixtream.Encoding.TRIAD_STREAM
    )
    assert result == "30"

def test_encode_triad_stream_full():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"\x01" * 511,
        Atomixtream.Encoding.TRIAD_STREAM
    )
    assert result == "ko" + ("9" * 255) + "1"

def test_encode_basic64_empty():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"",
        Atomixtream.Encoding.BASIC64
    )
    assert result == "70"

def test_encode_basic64_length1():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"\xff",
        Atomixtream.Encoding.BASIC64
    )
    assert result == "713o"

def test_encode_basic64_length2():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"\xff\x77",
        Atomixtream.Encoding.BASIC64
    )
    assert result == "727og"

def test_encode_basic64_length3():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"\xff\x77\xaa",
        Atomixtream.Encoding.BASIC64
    )
    assert result == "73WogZ"

def test_encode_basic64_length4():
    atomixtream = Atomixtream()
    result = atomixtream.encode_chunk(
        b"\xff\x77\xaa\xfe",
        Atomixtream.Encoding.BASIC64
    )
    assert result == "74WogZ3n"


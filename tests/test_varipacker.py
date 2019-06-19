""" Unit test cases for VariPacker class """

from itsybitser.varipacker import VariPacker

def test_encode_sextet_stream():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\x00\x01\x3e\x3f\x3f\x3e\x01\x00",
        VariPacker.Encoding.SEXTET_STREAM
    )
    assert result == "4801noon10"

def test_encode_sextet_stream_empty():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"",
        VariPacker.Encoding.SEXTET_STREAM
    )
    assert result == "40"

def test_encode_sextet_stream_maximal():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\x2a" * 511,
        VariPacker.Encoding.SEXTET_STREAM
    )
    assert result == "lo" + "Z" * 511

def test_encode_triad_stream():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\x00\x01\x06\x07\x07\x06\x01\x00",
        VariPacker.Encoding.TRIAD_STREAM
    )
    assert result == "388ng1"

def test_encode_triad_stream_empty():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"",
        VariPacker.Encoding.TRIAD_STREAM
    )
    assert result == "30"

def test_encode_triad_stream_maximal():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\x01" * 511,
        VariPacker.Encoding.TRIAD_STREAM
    )
    assert result == "ko" + ("9" * 255) + "1"

def test_encode_linear64_empty():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"",
        VariPacker.Encoding.LINEAR64
    )
    assert result == "70"

def test_encode_linear64_length1():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\xff",
        VariPacker.Encoding.LINEAR64
    )
    assert result == "713o"

def test_encode_linear64_length2():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\xff\x77",
        VariPacker.Encoding.LINEAR64
    )
    assert result == "727og"

def test_encode_linear64_length3():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\xff\x77\xaa",
        VariPacker.Encoding.LINEAR64
    )
    assert result == "73WogZ"

def test_encode_linear64_length4():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\xff\x77\xaa\xfe",
        VariPacker.Encoding.LINEAR64
    )
    assert result == "74WogZ3n"

def test_encode_linear64_maximal():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\xff" * 511,
        VariPacker.Encoding.LINEAR64
    )
    assert result == "o" * 682 + "3o"

def test_encode_sextet_run_empty():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"",
        VariPacker.Encoding.SEXTET_RUN
    )
    assert result == "20"

def test_encode_sextet_run():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\x2a" * 7,
        VariPacker.Encoding.SEXTET_RUN
    )
    assert result == "27Z"

def test_encode_sextet_run_maximal():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\x3e" * 511,
        VariPacker.Encoding.SEXTET_RUN
    )
    assert result == "jon"

def test_encode_octet_run_empty():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"",
        VariPacker.Encoding.OCTET_RUN
    )
    assert result == "10"

def test_encode_octet_run():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\xfa" * 7,
        VariPacker.Encoding.OCTET_RUN
    )
    assert result == "173j"

def test_encode_octet_run_maximal():
    varipacker = VariPacker()
    result = varipacker.encode_chunk(
        b"\xdd" * 511,
        VariPacker.Encoding.OCTET_RUN
    )
    assert result == "io3M"

def test_encode_gap_empty():
    varipacker = VariPacker()
    result = varipacker.encode_gap(0)
    assert result == "00"

def test_encode_gap():
    varipacker = VariPacker()
    result = varipacker.encode_gap(7)
    assert result == "07"

def test_encode_gap_maximal():
    varipacker = VariPacker()
    result = varipacker.encode_gap(511)
    assert result == "ho"

def test_encode_terminus():
    varipacker = VariPacker()
    result = varipacker.encode_terminus()
    assert result == "00"


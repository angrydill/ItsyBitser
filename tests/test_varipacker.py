""" Unit test cases for varipacker class """

from itsybitser import varipacker

def test_encode_sextet_stream():
    result = varipacker.encode_chunk(
        b"\x00\x01\x3e\x3f\x3f\x3e\x01\x00",
        varipacker.Encoding.SEXTET_STREAM
    )
    assert result == "4801noon10"

def test_encode_sextet_stream_empty():
    result = varipacker.encode_chunk(
        b"",
        varipacker.Encoding.SEXTET_STREAM
    )
    assert result == "40"

def test_encode_sextet_stream_maximal():
    result = varipacker.encode_chunk(
        b"\x2a" * 511,
        varipacker.Encoding.SEXTET_STREAM
    )
    assert result == "lo" + "Z" * 511

def test_encode_triad_stream():
    result = varipacker.encode_chunk(
        b"\x00\x01\x06\x07\x07\x06\x01\x00",
        varipacker.Encoding.TRIAD_STREAM
    )
    assert result == "388ng1"

def test_encode_triad_stream_empty():
    result = varipacker.encode_chunk(
        b"",
        varipacker.Encoding.TRIAD_STREAM
    )
    assert result == "30"

def test_encode_triad_stream_maximal():
    result = varipacker.encode_chunk(
        b"\x01" * 511,
        varipacker.Encoding.TRIAD_STREAM
    )
    assert result == "ko" + ("9" * 255) + "1"

def test_encode_linear64_empty():
    result = varipacker.encode_chunk(
        b"",
        varipacker.Encoding.LINEAR64
    )
    assert result == "70"

def test_encode_linear64_length1():
    result = varipacker.encode_chunk(
        b"\xff",
        varipacker.Encoding.LINEAR64
    )
    assert result == "713o"

def test_encode_linear64_length2():
    result = varipacker.encode_chunk(
        b"\xff\x77",
        varipacker.Encoding.LINEAR64
    )
    assert result == "727og"

def test_encode_linear64_length3():
    result = varipacker.encode_chunk(
        b"\xff\x77\xaa",
        varipacker.Encoding.LINEAR64
    )
    assert result == "73WogZ"

def test_encode_linear64_length4():
    result = varipacker.encode_chunk(
        b"\xff\x77\xaa\xfe",
        varipacker.Encoding.LINEAR64
    )
    assert result == "74WogZ3n"

def test_encode_linear64_maximal():
    result = varipacker.encode_chunk(
        b"\xff" * 511,
        varipacker.Encoding.LINEAR64
    )
    assert result == "o" * 682 + "3o"

def test_encode_sextet_run_empty():
    result = varipacker.encode_chunk(
        b"",
        varipacker.Encoding.SEXTET_RUN
    )
    assert result == "20"

def test_encode_sextet_run():
    result = varipacker.encode_chunk(
        b"\x2a" * 7,
        varipacker.Encoding.SEXTET_RUN
    )
    assert result == "27Z"

def test_encode_sextet_run_maximal():
    result = varipacker.encode_chunk(
        b"\x3e" * 511,
        varipacker.Encoding.SEXTET_RUN
    )
    assert result == "jon"

def test_encode_octet_run_empty():
    result = varipacker.encode_chunk(
        b"",
        varipacker.Encoding.OCTET_RUN
    )
    assert result == "10"

def test_encode_octet_run():
    result = varipacker.encode_chunk(
        b"\xfa" * 7,
        varipacker.Encoding.OCTET_RUN
    )
    assert result == "173j"

def test_encode_octet_run_maximal():
    result = varipacker.encode_chunk(
        b"\xdd" * 511,
        varipacker.Encoding.OCTET_RUN
    )
    assert result == "io3M"

def test_encode_gap_empty():
    result = varipacker.encode_gap(0)
    assert result == "00"

def test_encode_gap():
    result = varipacker.encode_gap(7)
    assert result == "07"

def test_encode_gap_maximal():
    result = varipacker.encode_gap(511)
    assert result == "ho"

def test_encode_terminus():
    result = varipacker.encode_terminus()
    assert result == "00"

def test_encode_empty():
    result = varipacker.encode(b"")
    assert result == varipacker.encode_terminus()

def test_encode_all_linear64_single_chunk():
    content = (b"\x40\x00\x00\x40" * 127) + b"\x40\x00\x00"
    result = varipacker.encode(content)
    assert result == "".join([
        varipacker.encode_chunk(content, varipacker.Encoding.LINEAR64),
        varipacker.encode_terminus()
    ])

def test_encode_all_linear64_double_chunk():
    content = ((b"\x40\x00\x00\x40" * 127) + b"\x40\x00\x00") * 2
    result = varipacker.encode(content)
    assert result == "".join([
        varipacker.encode_chunk(content[0:511], varipacker.Encoding.LINEAR64),
        varipacker.encode_chunk(content[0:511], varipacker.Encoding.LINEAR64),
        varipacker.encode_terminus()
    ])

def test_encode_all_sextet_run_single_chunk():
    content = b"\x39" * 511
    result = varipacker.encode(content)
    assert result == "".join([
        varipacker.encode_chunk(content, varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_terminus()
    ])

def test_encode_all_sextet_run_double_chunk():
    content = b"\x39" * 1022
    result = varipacker.encode(content)
    assert result == "".join([
        varipacker.encode_chunk(content[0:511], varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_chunk(content[0:511], varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_terminus()
    ])

def test_encode_alternating_sextet_octet_run():
    content = (b"\x39" * 10) + (b"\x40" * 10) + (b"\x39" * 10) + (b"\x40" * 10)
    result = varipacker.encode(content)
    assert result == "".join([
        varipacker.encode_chunk(b"\x39" * 10, varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_chunk(b"\x40" * 10, varipacker.Encoding.OCTET_RUN),
        varipacker.encode_chunk(b"\x39" * 10, varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_chunk(b"\x40" * 10, varipacker.Encoding.OCTET_RUN),
        varipacker.encode_terminus()
    ])

def test_encode_sextet_octet_run_with_linear64():
    content = (b"\x39" * 10) + b"\x61\x62" + (b"\x40" * 10) + b"\x77" +  (b"\x39" * 10) + (b"\x40" * 10)
    result = varipacker.encode(content)
    assert result == "".join([
        varipacker.encode_chunk(b"\x39" * 10, varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_chunk(b"\x61\x62", varipacker.Encoding.LINEAR64),
        varipacker.encode_chunk(b"\x40" * 10, varipacker.Encoding.OCTET_RUN),
        varipacker.encode_chunk(b"\x77", varipacker.Encoding.LINEAR64),
        varipacker.encode_chunk(b"\x39" * 10, varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_chunk(b"\x40" * 10, varipacker.Encoding.OCTET_RUN),
        varipacker.encode_terminus()
    ])

def test_encode_all_but_sextet_stream():
    content = (b"\x39" * 10) + b"\x61\x62\x01\x02\x03\x04\x05\x06" + (b"\x40" * 10) + b"\x77" +  (b"\x39" * 10) + (b"\x40" * 10)
    result = varipacker.encode(content)
    assert result == "".join([
        varipacker.encode_chunk(b"\x39" * 10, varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_chunk(b"\x61\x62", varipacker.Encoding.LINEAR64),
        varipacker.encode_chunk(b"\x01\x02\x03\x04\x05\x06", varipacker.Encoding.TRIAD_STREAM),
        varipacker.encode_chunk(b"\x40" * 10, varipacker.Encoding.OCTET_RUN),
        varipacker.encode_chunk(b"\x77", varipacker.Encoding.LINEAR64),
        varipacker.encode_chunk(b"\x39" * 10, varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_chunk(b"\x40" * 10, varipacker.Encoding.OCTET_RUN),
        varipacker.encode_terminus()
    ])

def test_encode_all():
    content = b"\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e" + (b"\x39" * 10) + b"\x61\x62\x01\x02\x03\x04\x05\x06" + (b"\x40" * 10) + b"\x77" +  (b"\x39" * 10) + (b"\x40" * 10)
    result = varipacker.encode(content)
    assert result == "".join([
        varipacker.encode_chunk(b"\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e", varipacker.Encoding.SEXTET_STREAM),
        varipacker.encode_chunk(b"\x39" * 10, varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_chunk(b"\x61\x62", varipacker.Encoding.LINEAR64),
        varipacker.encode_chunk(b"\x01\x02\x03\x04\x05\x06", varipacker.Encoding.TRIAD_STREAM),
        varipacker.encode_chunk(b"\x40" * 10, varipacker.Encoding.OCTET_RUN),
        varipacker.encode_chunk(b"\x77", varipacker.Encoding.LINEAR64),
        varipacker.encode_chunk(b"\x39" * 10, varipacker.Encoding.SEXTET_RUN),
        varipacker.encode_chunk(b"\x40" * 10, varipacker.Encoding.OCTET_RUN),
        varipacker.encode_terminus()
    ])

def test_distill_whitespace():
    clean_content = varipacker.encode(bytes(range(0,100)))
    dirty_content = clean_content[:20] + " " + clean_content[20:30] + "\r\n" + clean_content[30:]
    assert varipacker.distill(dirty_content) == clean_content

def test_distill_comments():
    clean_content = varipacker.encode(bytes(range(0,100)))
    dirty_content = "#comment1\n" + clean_content[:40] + "# coment 2 \r\n" + clean_content[40:]
    assert varipacker.distill(dirty_content) == clean_content

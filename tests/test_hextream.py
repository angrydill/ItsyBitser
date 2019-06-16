""" Unit Tests for class Hextream """

from itsybitser import Hextream

def test_encode_empty():
    """ encode empty bytes sequence """
    hextream = Hextream()
    result = hextream.encode(b"")
    assert result == ""

def test_encode_single_byte():
    """ encode one byte sequence """
    hextream = Hextream()
    result = hextream.encode(b"\xab")
    assert result == "AB"

def test_encode_multiple_bytes():
    """ encode several byte sequence """
    hextream = Hextream()
    result = hextream.encode(b"\xab\x01\x9a\xa9\xff")
    assert result == "AB 01 9A A9 FF"

def test_encode_long_sequence():
    """ encode byte sequence long enough for output to wrap """
    hextream = Hextream()
    result = hextream.encode(bytes(range(0, 40)))
    assert result == (
        "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F\n" +
        "10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F\n"+
        "20 21 22 23 24 25 26 27"
    )

def test_decode_empty():
    """ decode empty bytes sequence """
    hextream = Hextream()
    result = hextream.decode("")
    assert result == b""

def test_decode_single_byte():
    """ decode one byte sequence """
    hextream = Hextream()
    result = hextream.decode("AB")
    assert result == b"\xab"

def test_decode_multiple_bytes():
    """ decode several byte sequence """
    hextream = Hextream()
    result = hextream.decode("AB019AA9FF")
    assert result == b"\xab\x01\x9a\xa9\xff"

def test_decode_comments_whitespace():
    """ decode byte sequence from hextream w/comments and whitespace """
    hextream = Hextream()
    result = hextream.decode("AB 01 9A A9FF\n#a comment\nbbcc#inlinecomment\n\tdD")
    assert result == b"\xab\x01\x9a\xa9\xff\xbb\xcc\xdd"

def test_decode_with_prefixes():
    """ decode byte sequence from hextream with common hex prefix characters """
    hextream = Hextream()
    result = hextream.decode("AB $01 0x9A \\xA9")
    assert result == b"\xab\x01\x9a\xa9"

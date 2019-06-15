""" Unit Tests for class AsciiEncoder """

from itsybitser import AsciiEncoding

def test_distill_remove_whitespace():
    """ Removal of spaces, tabs, LF, CR, FF, and VT """
    ascii_encoding = AsciiEncoding()
    result = ascii_encoding.distill("  A 1h\f3$BD  \n 4 []2\r\t  zy5C\v ")
    assert result == "A1h3$BD4[]2zy5C"

def test_distill_remove_comments():
    """ Removal of sequences starting w/"#" and extending to EOL """
    ascii_encoding = AsciiEncoding()
    result = ascii_encoding.distill(
        "# comment line \n \t #comment after whitespace\nABCD12 # Inline Comment\n34\n#"
    )
    assert result == "ABCD1234"

def test_compare_simple_same():
    """ Compare verbatum """
    ascii_encoding = AsciiEncoding()
    result = ascii_encoding.compare(
        "vBIybIF&WBFE&WOF*f4((*N44wr9[]{}", "vBIybIF&WBFE&WOF*f4((*N44wr9[]{}"
    )
    assert result == -1

def test_compare_simple_different():
    """ Compare different strings """
    ascii_encoding = AsciiEncoding()
    result = ascii_encoding.compare(
        "vBIybIF&WBFE&WOF*f4((*N44wr9[]{}", "vBIybI&WBFE&WOF*f4((*N44wr9[]{}"
    )
    assert result == 6

def test_compare_whitespaced_same():
    """ Compare same except for (ignored) whitespace """
    ascii_encoding = AsciiEncoding()
    result = ascii_encoding.compare(
        "vBIybIF&WBFE&WOF*f\n4((*N44w r9[]{}", "vBIy bIF&W\rBFE&WOF*f4((*N44wr9[]{}"
    )
    assert result == -1

def test_compare_whitespaced_different():
    """ Compare different strings w/ different (ignored) whitespace """
    ascii_encoding = AsciiEncoding()
    result = ascii_encoding.compare(
        "vBIybIF&WBFE&WOF*f\n4((*N44w r9[-]{}", "vBIy bIF&W\rBFE&WOF*f4((*N44wr9[]{}"
    )
    assert result == 29

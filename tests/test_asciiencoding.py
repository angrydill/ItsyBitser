""" Unit Tests for asciiencoding module """

from itsybitser import asciiencoding

def test_distill_remove_whitespace():
    """ Removal of spaces, tabs, LF, CR, FF, and VT """
    result = asciiencoding.distill("  A 1h\f3$BD  \n 4 []2\r\t  zy5C\v ")
    assert result == "A1h3$BD4[]2zy5C"

def test_distill_remove_comments():
    """ Removal of sequences starting w/"#" and extending to EOL """
    result = asciiencoding.distill(
        "# comment line \n \t #comment after whitespace\nABCD12 # Inline Comment\n34\n#"
    )
    assert result == "ABCD1234"

def test_compare_simple_same():
    """ Compare verbatum """
    result = asciiencoding.compare(
        "vBIybIF&WBFE&WOF*f4((*N44wr9[]{}", "vBIybIF&WBFE&WOF*f4((*N44wr9[]{}"
    )
    assert result == -1

def test_compare_simple_different():
    """ Compare different strings """
    result = asciiencoding.compare(
        "vBIybIF&WBFE&WOF*f4((*N44wr9[]{}", "vBIybI&WBFE&WOF*f4((*N44wr9[]{}"
    )
    assert result == 6

def test_compare_whitespaced_same():
    """ Compare same except for (ignored) whitespace """
    result = asciiencoding.compare(
        "vBIybIF&WBFE&WOF*f\n4((*N44w r9[]{}", "vBIy bIF&W\rBFE&WOF*f4((*N44wr9[]{}"
    )
    assert result == -1

def test_compare_whitespaced_different():
    """ Compare different strings w/ different (ignored) whitespace """
    result = asciiencoding.compare(
        "vBIybIF&WBFE&WOF*f\n4((*N44w r9[-]{}", "vBIy bIF&W\rBFE&WOF*f4((*N44wr9[]{}"
    )
    assert result == 29

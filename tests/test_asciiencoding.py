""" Unit Tests for class AsciiEncoder """

import unittest
from itsybitser import AsciiEncoding


class TestAsciiEncoding(unittest.TestCase):

    def test_distill_remove_whitespace(self):
        ascii_encoding = AsciiEncoding()
        result = ascii_encoding.distill("  A 1h\f3$BD  \n 4 []2\r\t  zy5C\v ")
        assert result == "A1h3$BD4[]2zy5C"

    def test_distill_remove_comments(self):
        ascii_encoding = AsciiEncoding()
        result = ascii_encoding.distill(
            "# comment line \n \t #comment after whitespace\nABCD12 # Inline Comment\n34\n#"
        )
        self.assertEqual(result, "ABCD1234")

    def test_compare_simple_same(self):
        ascii_encoding = AsciiEncoding()
        result = ascii_encoding.compare(
            "vBIybIF&WBFE&WOF*f4((*N44wr9[]{}", "vBIybIF&WBFE&WOF*f4((*N44wr9[]{}"
        )
        self.assertEqual(result, -1)

    def test_compare_simple_different(self):
        ascii_encoding = AsciiEncoding()
        result = ascii_encoding.compare(
            "vBIybIF&WBFE&WOF*f4((*N44wr9[]{}", "vBIybI&WBFE&WOF*f4((*N44wr9[]{}"
        )
        self.assertEqual(result, 6)

    def test_compare_whitespaced_same(self):
        ascii_encoding = AsciiEncoding()
        result = ascii_encoding.compare(
            "vBIybIF&WBFE&WOF*f\n4((*N44w r9[]{}", "vBIy bIF&W\rBFE&WOF*f4((*N44wr9[]{}"
        )
        self.assertEqual(result, -1)

    def test_compare_whitespaced_different(self):
        ascii_encoding = AsciiEncoding()
        result = ascii_encoding.compare(
            "vBIybIF&WBFE&WOF*f\n4((*N44w r9[-]{}", "vBIy bIF&W\rBFE&WOF*f4((*N44wr9[]{}"
        )
        self.assertEqual(result, 29)

if __name__ == "__main__":
    unittest.main()

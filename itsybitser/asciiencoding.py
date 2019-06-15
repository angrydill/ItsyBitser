""" Common functionality between Atomixtream and Hextream classes """

import re


class AsciiEncoding:

    def __init__(self):
        self.comment_regex = re.compile("#.*$", re.MULTILINE)

    def compare(self, content1, content2):
        result = -1
        distilled_content1 = self.distill(content1)
        distilled_content2 = self.distill(content2)
        if distilled_content1 != distilled_content2:
            result = 0
            while distilled_content1[result] == distilled_content2[result]:
                result += 1
        return result

    def distill(self, content):
        # Eliminate comments
        result = self.comment_regex.sub("", content)
        # Eliminate all whitespace (split by default splits on any WS char)
        result = ''.join(result.split())
        return result

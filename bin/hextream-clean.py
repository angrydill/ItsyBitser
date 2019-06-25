#!/usr/bin/env python3
""" Strip comments and normalize whitespace for Hextream format content """

import sys
from itsybitser import hextream

def main():
       hex_content = sys.stdin.read()
       binary_content = hextream.decode(hex_content)
       hex_content = hextream.encode(binary_content)
       print(hex_content)

if __name__ == "__main__":
    main()

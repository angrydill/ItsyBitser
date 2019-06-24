#!/usr/bin/env python3
""" Encode content in Hextream format into the Varipacker format """

import sys
from itsybitser import hextream, varipacker

def main():
       hex_content = sys.stdin.read()
       binary_content = hextream.decode(hex_content)
       varipacker_content = varipacker.encode(binary_content)
       print(varipacker_content)

if __name__ == "__main__":
    main()

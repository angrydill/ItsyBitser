#!/usr/bin/env python3
""" Decode content in Varipacker format back to Hextream format """

import sys
from itsybitser import hextream, varipacker

def main():
       varipacker_content = sys.stdin.read()
       binary_content = varipacker.decode(varipacker.distill(varipacker_content))
       hex_content = hextream.encode(binary_content)
       print(hex_content)

if __name__ == "__main__":
    main()

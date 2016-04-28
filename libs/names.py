#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import ucd

class lookup:

    def __init__(self):
        pass

    def name(self, char):        
        id = ord(char)
        hex = "%04X" % id

        logging.debug("char: %s id: %s hex: %s" % (char, id, hex))
        return ucd.UCD_MAP.get(hex, None)

if __name__ == '__main__':

    import sys

    input = sys.argv[1:]
    input = " ".join(input)

    input = input.decode('utf-8')

    ref = lookup()

    for char in input:
        name = ref.name(char)
        print "%s is %s" % (char, name)

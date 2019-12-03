#!/usr/bin/python3

import sys, struct

romFileName = sys.argv[1]
address = int(sys.argv[2], 16)

with open(romFileName, 'rb') as romFile:
    romFile.seek(address)
    value = struct.unpack("B", romFile.read(1))
    print("{}: {}".format(hex(address), hex(value[0])))


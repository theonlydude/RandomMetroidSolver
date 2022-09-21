#!/usr/bin/python3

# ./extract_data.py ~/supermetroid_random/super_metroid.smc 0x12E3D9 0x8F > spore.pal

import sys, struct

rom = sys.argv[1]
address = int(sys.argv[2], 16)
length = int(sys.argv[3], 16)

with open(rom, 'rb') as romFile:
    romFile.seek(address)
    data = []
    for i in range(length):
        data.append(struct.unpack("B", romFile.read(1))[0])
    print("{}: {},".format(address, data))

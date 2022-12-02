#!/usr/bin/python3

# ./extract_data.py ~/supermetroid_random/super_metroid.smc 0x12E3D9 0x8F > spore.pal

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

import struct
from rom.rom import snes_to_pc, pc_to_snes

rom = sys.argv[1]
address = int(sys.argv[2], 16)
if address >= 0x800000:
    address = snes_to_pc(address)
length = int(sys.argv[3], 16)
try:
    display = sys.argv[4]
except:
    display = None

with open(rom, 'rb') as romFile:
    romFile.seek(address)
    data = []
    for i in range(length):
        data.append(struct.unpack("B", romFile.read(1))[0])
    if display is None:
        # used by tools/gen_sprite_palettes.sh
        print("{}: {},".format(address, data))
    else:
        for i in range(length):
            if i % 2 == 0:
                print("{}: {}".format(hex(address+i), hex(data[i] + (data[i+1] << 8))))

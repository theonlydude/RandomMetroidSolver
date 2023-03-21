#!/usr/bin/python3

import sys, os
from shutil import copyfile

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc, pc_to_snes

romName = sys.argv[1]
rom = RealROM(romName)

paths = [0xB3A058, 0xB3A05A, 0xB3A32A, 0xB3A6BC, 0xB3AA24, 0xB3ADFE, 0xB3B16A, 0xB3B556, 0xB3B956, 0xB3BC86, 0xB3C086, 0xB3C290, 0xB3C690, 0xB3C9CC, 0xB3CDCC, 0xB3D140, 0xB3D4A2, 0xB3D880, 0xB3DA00, 0xB3DA02, 0xB3DB9A, 0xB3DB9C, 0xB3DD40, 0xB3DD42, 0xB3DE7C, 0xB3DE7E, 0xB3DFDE, 0xB3DFE0, 0xB3E14E]
for path in paths:
    rom.seek(snes_to_pc(path))
    print("org ${:06x}".format(path))
    out = []
    while True:
        x = rom.readByte()
        y = rom.readByte()
        if x == 0x80 and y == 0x00:
            # the end
            out.append((x,y))
            print("    db "+", ".join("${:02x},${:02x}".format(x,y) for x,y in out))
            break
        if x == 0x01:
            x = 0xff
        elif x == 0xff:
            x = 0x01
        out.append((x, y))

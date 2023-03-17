#!/usr/bin/python3

import sys, os
from shutil import copyfile

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc, pc_to_snes
from rom.leveldata import Spritemap, Transform
from rom.ips import IPS_Patch

romName = sys.argv[1]
rom = RealROM(romName)

spritemaps = [
    # bt sitting on the ground
    0xAA8C33,

    # bt standing up
    0xAA8CB7,
    0xAA8D3B,
    0xAA8DC4,
    0xAA8E43,
    0xAA8EC2,
    0xAA8F46,

    # bt statue breaking
    0x8D8DFB,
    0x8D8E02,
    0x8D8E09,
    0x8D8E10,
    0x8D8E17,
    0x8D8E1E,
    0x8D8E25,
    0x8D8E2C
]

asms = {}
for addr in spritemaps:
    spritemap = Spritemap(rom, addr)
    spritemap.transform(Transform.Mirror)
    asmAddr, asm = spritemap.displayASM()
    asms[asmAddr] = asm

print("==== updated spritemaps:")
for asmAddr in sorted(asms.keys()):
    print(asms[asmAddr])

rom.close()


#!/usr/bin/python3

import sys, os, argparse
from shutil import copyfile

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc, pc_to_snes

vanillaRom = RealROM(sys.argv[1])

# if last two tiles are used we also have to copy them to escape tiles
escapeTilesAddr = snes_to_pc(0x94C800)

vanillaRom.seek(escapeTilesAddr)

# a 16 8x8 4bpp tiles row size
rowSize = 32 * 16
for _ in range(32*4):
    vanillaRom.writeByte(0)
lastRow8Addr = escapeTilesAddr + rowSize
vanillaRom.seek(lastRow8Addr)
for _ in range(32*4):
    vanillaRom.writeByte(0)

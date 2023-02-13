#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
dir_path = os.path.dirname(sys.path[0])
sys.path.append(dir_path)

from rom.rom import snes_to_pc, RealROM
from rom.compression import Compressor

romFile = sys.argv[1]
addr = int(sys.argv[2], 16)
if addr >= 0x800000:
    addr = snes_to_pc(addr)

rom = RealROM(romFile)
output = Compressor().decompress(rom, addr)
compressed_length, data = output

print("at {} compressed: {} uncompressed: {}".format(hex(addr), compressed_length, len(data)))

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
outFile = None
if len(sys.argv) > 3:
    outFile = sys.argv[3]
outAddr = None
if len(sys.argv) > 4:
    outAddr = int(sys.argv[4], 16)
    if outAddr >= 0x800000:
        outAddr = snes_to_pc(outAddr)

rom = RealROM(romFile)
output = Compressor().decompress(rom, addr)
compressed_length, data = output

print("at {} compressed: {} uncompressed: {}".format(hex(addr), compressed_length, len(data)))

if outFile is not None:
    with open(outFile, "a+"): # create if does not exist
        pass
    outRom = RealROM(outFile)
    if outAddr is not None:
        outRom.seek(outAddr)
    outRom.write(bytearray(data))
    outRom.close()

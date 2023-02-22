#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
dir_path = os.path.dirname(sys.path[0])
sys.path.append(dir_path)

from rom.rom import snes_to_pc, RealROM
from rom.compression import Compressor

inFile = sys.argv[1]
outFile = sys.argv[2]
outAddr = None
if len(sys.argv) > 3:
    outAddr = int(sys.argv[3], 16)
    if outAddr >= 0x800000:
        outAddr = snes_to_pc(outAddr)

with open(inFile, "rb") as gfx:
    output = Compressor("Slow").compress(gfx.read())

if outFile is not None:
    with open(outFile, "a+"): # create if does not exist
        pass
    outRom = RealROM(outFile)
    if outAddr is not None:
        outRom.seek(outAddr)
    outRom.write(bytearray(output))
    outRom.close()

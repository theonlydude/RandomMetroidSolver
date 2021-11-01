#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# extract ship tiles & layout & palette from hack, generate an ips in the end.

from rom.rom import RealROM, snes_to_pc
from rom.compression import Compressor

vanilla = sys.argv[1]

tileAddr = snes_to_pc(0x95A82F)
tilemapAddr = snes_to_pc(0x96FE69)

vanillaRom = RealROM(vanilla)

_, tileData = Compressor().decompress(vanillaRom, tileAddr)        
_, tilemapData = Compressor().decompress(vanillaRom, tilemapAddr)        

tileBytes = [b.to_bytes(1, byteorder='little') for b in tileData]
with open('ship7.gfx', 'wb') as ship:
    for byte in tileBytes:
        ship.write(byte)

tilemapBytes = [b.to_bytes(1, byteorder='little') for b in tilemapData]
with open('ship7.tilemap', 'wb') as tilemap:
    for byte in tilemapBytes:
        tilemap.write(byte)

print("ship7.gfx and ship7.tilemap extracted")

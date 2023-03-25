#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM
from rom.map import AreaMap

tile_to_replace = int(sys.argv[1], 16)
tile_replacement = int(sys.argv[2], 16)
maps = sys.argv[3:]

def replaceTile(areaMap, rom):
    for x in range(areaMap.width):
        for y in range(areaMap.height):
            tile = areaMap.getTile(x, y)
            if tile.idx == tile_to_replace:
                print("$%02x to $%02x at (%d, %d)" % (tile_to_replace, tile_replacement, x, y))
                tile.idx = tile_replacement
                areaMap.writeBGtile(rom, x, y)

for m in maps:
    print("Replacing tiles in "+m)
    rom = RealROM(m)
    areaMap = AreaMap.load(rom)
    replaceTile(areaMap, rom)
    rom.close()

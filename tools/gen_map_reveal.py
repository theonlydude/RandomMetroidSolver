#!/usr/bin/env python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

map_path = sys.argv[1]
map_data_path = sys.argv[2]
map_data_reveal_path = sys.argv[3]

from rom.map import AreaMap
from rom.rom import RealROM

map_rom = RealROM(map_path)
map_data_rom = RealROM(map_data_path)

with open(map_data_reveal_path, "a+"):
    # create if does not exist
    pass
map_data_reveal_rom = RealROM(map_data_reveal_path)

areaMap = AreaMap.load(map_rom, map_data_rom)

map_rom.close()
map_data_rom.close()

EMPTY_TILE = 0x1f

for x in range(areaMap.width):
    for y in range(areaMap.height):
        tile = areaMap.getTile(x, y)
        tile.present = tile.idx != EMPTY_TILE

areaMap.savePresence(map_data_reveal_rom)

map_data_reveal_rom.close()

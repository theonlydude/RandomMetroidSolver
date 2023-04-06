#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM
from rom.map import AreaMap, BGtile
from map.mirror_offsets import getOffsetFromFilePath

vanilla_map_path = sys.argv[1]
vanilla_presence_path = sys.argv[2]
mirror_map_path = sys.argv[3]
mirror_presence_path = sys.argv[4]

vanilla_map_rom = RealROM(vanilla_map_path)
vanilla_presence_rom = RealROM(vanilla_presence_path)

with open(mirror_map_path, "a+"):
    # create if does not exist
    pass

with open(mirror_presence_path, "a+"):
    # create if does not exist
    pass

mirror_map_rom = RealROM(mirror_map_path)
mirror_presence_rom = RealROM(mirror_presence_path)

vanillaMap = AreaMap.load(vanilla_map_rom, vanilla_presence_rom)

vanilla_map_rom.close()
vanilla_presence_rom.close()

mirrorMap = AreaMap()

EMPTY_TILE = 0x1f

w = vanillaMap.width
offset = getOffsetFromFilePath(vanilla_map_path)
mirrorX = lambda x: (w - offset - x) % w

for x in range(vanillaMap.width):
    for y in range(vanillaMap.height):
        tile = vanillaMap.getTile(x, y)
        if tile.idx == EMPTY_TILE:
            mirrorTile = tile
        else:
            mirrorTile = BGtile(tile.idx, tile.pal, prio=tile.prio, hFlip=not tile.hFlip, vFlip=tile.vFlip)
        mirrorMap.setTile(mirrorX(x), y, mirrorTile)

mirrorMap.save(mirror_map_rom)
mirrorMap.savePresence(mirror_presence_rom)

mirror_map_rom.close()
mirror_presence_rom.close()

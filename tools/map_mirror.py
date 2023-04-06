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
S_TILES = [0xB5, 0xB6, 0xB7]
R_TILES = [0xC5, 0xC6, 0xC7]

S_R_MIRROR_IDX = {0: 2, 1: 1, 2:0}

w = vanillaMap.width
offset = getOffsetFromFilePath(vanilla_map_path)
mirrorX = lambda x: (w - offset - x) % w

for x in range(vanillaMap.width):
    for y in range(vanillaMap.height):
        tile = vanillaMap.getTile(x, y)
        if tile.idx == EMPTY_TILE:
            mirrorTile = tile
        elif tile.idx in S_TILES:
            i = S_TILES.index(tile.idx)
            mirrorTile = BGtile(S_TILES[S_R_MIRROR_IDX[i]], tile.pal, prio=tile.prio, hFlip=tile.hFlip, vFlip=tile.vFlip)
        elif tile.idx in R_TILES:
            i = R_TILES.index(tile.idx)
            mirrorTile = BGtile(R_TILES[S_R_MIRROR_IDX[i]], tile.pal, prio=tile.prio, hFlip=tile.hFlip, vFlip=tile.vFlip)
        else:
            mirrorTile = BGtile(tile.idx, tile.pal, prio=tile.prio, hFlip=not tile.hFlip, vFlip=tile.vFlip)
        mirrorTile.present = tile.present
        mirrorMap.setTile(mirrorX(x), y, mirrorTile)

mirrorMap.save(mirror_map_rom)
mirrorMap.savePresence(mirror_presence_rom)

mirror_map_rom.close()
mirror_presence_rom.close()

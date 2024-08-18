#!/usr/bin/python3

import sys, os, colorsys
sys.path.append(os.path.dirname(sys.path[0]))

from rom.map import AreaMap
from rom.rom import RealROM

mapRomPath = sys.argv[1]
mapRom = RealROM(mapRomPath)
presenceRom = RealROM(sys.argv[2])
ramDump = RealROM(sys.argv[3])

offsets = {
    "crateria": 0xCD52,
    "brinstar": 0xCE52,
    "norfair": 0xCF52,
    "wrecked_ship": 0xD052,
    "maridia": 0xD152,
    "tourian": 0xD252,
    "ceres": 0xD352
}

for area, offset in offsets.items():
    if area in mapRomPath:
        print("%s map" % area)
        areaOffset = offset
        break

orig = AreaMap.load(mapRom, presenceRom)
explored = AreaMap.load(mapRom, ramDump, presenceOffset=areaOffset)

orig_count = 0
explored_count = 0

for x in range(orig.width):
    for y in range(orig.height):
        orig_tile = orig.getTile(x, y)
        explored_tile = explored.getTile(x, y)
        if orig_tile.present:
            orig_count += 1
        if explored_tile.present:
            explored_count += 1
        if orig_tile.present and not explored_tile.present:
            print("Unexplored: %d, %d" % (x, y))
        if explored_tile.present and not orig_tile.present:
            print("Weird: %d, %d" % (x, y))

print("orig: %d, explored: %d" % (orig_count, explored_count))

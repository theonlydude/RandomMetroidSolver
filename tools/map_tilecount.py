#!/usr/bin/python3

import sys, os, json

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

mapDataDir = sys.argv[1]
outPath = sys.argv[2]

from rom.map import AreaMap
from collections import defaultdict

maps = {
    "brinstar": AreaMap(),
    "ceres": AreaMap(),
    "crateria": AreaMap(),
    "maridia": AreaMap(),
    "norfair": AreaMap(),
    "tourian": AreaMap(),
    "wrecked_ship": AreaMap()
}

def loadDataPath(area, prefix="normal"):
    mapDataPath = "%s/%s_%s.json" % (mapDataDir, prefix, area)
    regionMap = maps[area]
    with open(mapDataPath, "r") as fp:
        mapData = json.load(fp)
    print("Loaded "+mapDataPath)
    for graphArea, rooms in mapData.items():
        for room, coords in rooms.items():
            for c in coords:
                x, y = c[0], c[1]
                regionMap.setTile(x, y, graphArea)

def countAreaTiles(destDict):
    for m in maps.values():
        for x in range(m.width):
            for y in range(m.height):
                t = m.getTile(x, y)
                if t is not None:
                    destDict[t] += 1

outData = {
    "vanilla_layout": defaultdict(int),
    "area_rando": defaultdict(int)
}

# "normal" (= area rando) variant
for area in maps.keys():
    loadDataPath(area)

countAreaTiles(outData["area_rando"])

# override some tile with "alt" (= vanilla layout) variant
for area in maps.keys():
    try:
        loadDataPath(area, "alt")
    except FileNotFoundError:
        # alt variant often doesn't exist
        pass
   
countAreaTiles(outData["vanilla_layout"])

areaSum = sum(outData["area_rando"].values())
vanillaSum = sum(outData["vanilla_layout"].values())

assert areaSum == vanillaSum, f"Total tile count discrepency! area: {areaSum}, vanilla: {vanillaSum}"

print("Writing "+outPath)
with open(outPath, "w") as fp:
    json.dump(outData, fp, indent=4)

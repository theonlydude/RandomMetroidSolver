#!/usr/bin/python3

import sys, os, json
from map.mirror_offsets import getOffsetFromFilePath

vanilla_json = sys.argv[1]
mirror_json = sys.argv[2]

w = 64
offset = getOffsetFromFilePath(vanilla_json)
mirrorX = lambda x: (w - offset - x) % w

with open(vanilla_json, "r") as fp:
    map_area_data = json.load(fp)

with open(mirror_json, "w") as fp:
    for area, areaData in map_area_data.items():
        for room, coordsList in areaData.items():
            for coords in coordsList:
                coords[0] = mirrorX(coords[0])
    json.dump(map_area_data, fp, indent=4)

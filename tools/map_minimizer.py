#!/usr/bin/python3

import sys, os, json

sys.path.append(os.path.dirname(sys.path[0]))

from rom.map import AreaMap
from graph.graph_utils import graphAreas

flavor = sys.argv[1]

flavorStr = "_" + flavor if flavor != "vanilla" else ""
mapDataPath = f"tools/map/graph_area{flavorStr}/normal_"

dummyMap = AreaMap() # to get byte offsets from coords

area_maps = {
    "brinstar": "Brinstar",
    "norfair": "Norfair",
    "maridia": "Maridia",
    "crateria": "Crateria",
    "wrecked_ship": "WreckedShip"
}

roomsToKeep = [
    "Kraid Room", "Varia Suit Room",
    "Draygon's Room", "Space Jump Room",
    "Ridley's Room", "Ridley Tank Room",
    "Phantoon's Room"
]

for graphArea in graphAreas:
    if graphArea in ["Ceres", "Tourian"]:
        continue
    asmPath = f"patches/{flavor}/src/remove_{graphArea}.asm"
    with open(asmPath, "w") as asm:
        asm.write(f'''
lorom
arch 65816

incsrc "sym/map_data.asm"
''')
        for areaName, area in area_maps.items():
            if graphArea == "Crateria" and area == "Crateria":
                # never remove Crateria graph area in Crateria map as it is in the escape
                continue
            with open(mapDataPath + areaName + ".json", "r") as fp:
                mapData = json.load(fp)
            graphAreaMapData = mapData.get(graphArea)
            if graphAreaMapData is None:
                continue
            asm.write(f'''
;;; tiles for {area}
''')
            for room, coords in graphAreaMapData.items():
                if room in roomsToKeep:
                    continue
                asm.write(f'''
;;; tiles for room "{room}"
''')
                for c in coords:
                    x, y = c[0], c[1]
                    offset = dummyMap.getOffset(x, y, mapOffset=0)
                    asm.write(f'''
org map_data_{area}+${offset:x}  ; ({x}, {y})
    dw $001f   ; empty tile
''')

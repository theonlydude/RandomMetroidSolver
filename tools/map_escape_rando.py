#!/usr/bin/python3

import sys, os, json

sys.path.append(os.path.dirname(sys.path[0]))

from rom.map import AreaMap

flavor = sys.argv[1]

flavorStr = "_" + flavor if flavor != "vanilla" else ""
mapDataPath = f"tools/map/graph_area{flavorStr}/normal_"

removedRooms = {
    "brinstar": ("Brinstar", "GreenPinkBrinstar", ["Brinstar Pre-Map Room", "Brinstar Map Room"]),
    "norfair": ("Norfair", "Norfair", ["Norfair Map Room"]),
    "wrecked_ship": ("WreckedShip", "WreckedShip", ["Wrecked Ship Map Room"]),
    "maridia": ("Maridia", "WestMaridia", ["Maridia Map Room"])
}

dummyMap = AreaMap() # to get byte offsets from coords

asmPath = f"patches/{flavor}/src/map_data_escape_rando.asm"
with open(asmPath, "w") as asm:
    asm.write(f'''
lorom
arch 65816

incsrc "sym/map_data.asm"
''')
    for areaName, areaData in removedRooms.items():
        area, graphArea, roomList = areaData
        asm.write(f'''
;;; tiles for {area}
''')
        with open(mapDataPath + areaName + ".json", "r") as fp:
            mapData = json.load(fp)
        for room in roomList:
            asm.write(f'''
;;; tiles for room "{room}"
''')
            coords = mapData[graphArea][room]
            for c in coords:
                x, y = c[0], c[1]
                offset = dummyMap.getOffset(x, y, mapOffset=0)
                asm.write(f'''
org map_data_{area}+${offset:x}  ; ({x}, {y})
    dw $001f   ; empty tile
''')

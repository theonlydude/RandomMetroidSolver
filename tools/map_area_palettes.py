#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

mapDataPath = sys.argv[1]
binPath = sys.argv[2]
presencePath = sys.argv[3]
asmPath = sys.argv[4]
area = sys.argv[5]

import json
from rom.map import palettesByArea, AreaMap
from rom.rom import RealROM

palettes = palettesByArea[area]
mapRom = RealROM(binPath)
presenceRom = RealROM(presencePath)
areaMap = AreaMap.load(mapRom, presenceRom)

with open(mapDataPath, "r") as fp:
    mapData = json.load(fp)

with open(asmPath, "w") as asm:
    asm.write("include\n")
    for graphArea, rooms in mapData.items():
        asm.write(f'''
;;; tiles for graph area {graphArea}
''')
        pal = palettes[graphArea]
        for room, coords in rooms.items():
            if room == "__unexplorable__":
                continue
            asm.write(f'''
;;; tiles for room "{room}"
''')
            for c in coords:
                x, y = c[0], c[1]
                tile = areaMap.getTile(x, y)
                if not tile.present:
                    print(f"Ignored absent tile at ({x}, {y}) in room {room}")
                    continue
                tile.pal = pal
                tileWord = tile.toWord()
                offset = areaMap.getOffset(x, y, mapOffset=0)
                asm.write(f'''
org map_data_{area}+${offset:x}  ; ({x}, {y})
     dw ${tileWord:0>4x}  ; {str(tile)}
''')

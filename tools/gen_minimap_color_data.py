#!/usr/bin/python3

import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

asm = sys.argv[1]

layout = "area"
if len(sys.argv) > 2:
    layout = sys.argv[2]

from rooms import rooms as rooms
from map.minimap import MinimapPalettesConfig
from rom.map import palettesByArea

alt = layout == "alt"

flavor = "vanilla"
if "mirror" in asm:
    flavor = "mirror"

dataDirs = {
    "vanilla": "tools/map/graph_area",
    "mirror": "tools/map/graph_area_mirror"
}

minimapCfg = MinimapPalettesConfig(dataDir=dataDirs[flavor], binMapDir=f"patches/{flavor}/src/map", alt=alt)
tripletsAddresses = {}
explored_pals = [2, 0, 6]
nPalettes = 8
palette_triplet_size = 2*nPalettes

with open(asm, "w") as src:
    src.write('lorom\narch 65816\n\nincsrc "sym/map.asm"\nincsrc "area_colors.asm"\n\n')
    # write palette triplets configs
    for roomType in minimapCfg.roomTypes.values():
        tripletId = roomType.paletteTripletId
        if tripletId not in tripletsAddresses:
            src.write(f"org map_MinimapTilePaletteTables+{palette_triplet_size*tripletId}\n")
            label = f"palette_triplet_{tripletId}"
            tripletsAddresses[tripletId] = label
            triplet = roomType.paletteTriplet
            src.write(f";;; {triplet}\n")
            src.write(f"{label}:\n")
            for pal in range(nPalettes):
                if pal in triplet:
                    p = explored_pals[triplet.index(pal)]
                elif pal == 2: # unexplored
                    p = 3
                else:
                    p = pal
                src.write("\tdw $%04x ; pal %d: %d\n" % ((p << 10) | 0x2000, pal, p))
    src.write("\nwarnpc map_MinimapTilePaletteTables_limit\n")
    # write palette data table
    src.write("\norg map_minimap_color_data\n")
    allRoomTypes = []
    for roomType in minimapCfg.roomTypes.values():
        if roomType not in allRoomTypes:
            allRoomTypes.append(roomType)
    colorLists = {}
    for roomType in sorted(allRoomTypes, key=lambda rt: rt.id):
        roomNames = [room for room, rt in minimapCfg.roomTypes.items() if rt == roomType]
        src.write(f";;; {roomNames}\n")
        src.write(f"minimap_room_type_{roomType.id}:\n")
        graphAreas = roomType.graphAreas
        triplet = roomType.paletteTriplet
        src.write(f"\tdw {tripletsAddresses[roomType.paletteTripletId]}\n")
        for graphArea in roomType.graphAreas:
            if graphArea is not None:
                src.write(f"\tdw !AreaColor_{graphArea}\n")
            else:
                src.write("\tdw !vanilla_etank_color\n")
        for i in range(len(graphAreas), 3):
            src.write("\tdw !vanilla_etank_color\n")
    src.write("\nwarnpc map_minimap_color_data_limit\n")

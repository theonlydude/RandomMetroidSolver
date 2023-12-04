#!/usr/bin/python3

import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

asm = sys.argv[1]

layout = "area"
if len(sys.argv) > 2:
    layout = sys.argv[2]

from rooms import rooms as rooms
from map.minimap import MinimapPalettesConfig

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
            src.write(f"{label}:\n")
            triplet = sorted(list(roomType.paletteTriplet))
            for pal in range(nPalettes):
                if pal in triplet:
                    p = explored_pals[triplet.index(pal)]
                else:
                    p = pal
                src.write("\tdw $%04x\n" % ((p << 10) | 0x2000))
    src.write("\nwarnpc map_MinimapTilePaletteTables_limit\n")
    # write palette data table
    src.write("\norg map_minimap_color_data\n")
    allRoomTypes = []
    for roomType in minimapCfg.roomTypes.values():
        if roomType not in allRoomTypes:
            allRoomTypes.append(roomType)
    for roomType in sorted(allRoomTypes, key=lambda rt: rt.id):
        src.write(f"minimap_room_type_{roomType.id}:\n")
        graphAreas = sorted(list(roomType.graphAreas))
        src.write(f"\tdw {tripletsAddresses[roomType.paletteTripletId]}\n")
        for i in range(3):
            if i < len(graphAreas):
                area = f"!AreaColor_{graphAreas[i]}"
            else:
                area = "!vanilla_etank_color"
            src.write(f"\tdw {area}\n")
    src.write("\nwarnpc map_minimap_color_data_limit\n")

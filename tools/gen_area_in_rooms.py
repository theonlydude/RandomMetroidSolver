#!/usr/bin/python3

import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

# generate asm files putting graph area ID, and minimap room type ID in "Unused Pointer" field in all room states

vanilla=sys.argv[1]
asm=sys.argv[2]

layout="area"
if len(sys.argv) > 3:
    layout=sys.argv[3]

from graph.graph_utils import graphAreas as areas
from rooms import rooms as rooms_area
from rooms import rooms_alt
from map.minimap import MinimapPalettesConfig

rooms = {}
for room in rooms_area:
    rooms[room['Name']] = room
alt = layout == "alt"
if alt:
    for room in rooms_alt:
        rooms[room['Name']] = room

flavor = "vanilla"
if "mirror" in asm:
    flavor = "mirror"

dataDirs = {
    "vanilla": "tools/map/graph_area",
    "mirror": "tools/map/graph_area_mirror"
}

minimapCfg = MinimapPalettesConfig(dataDir=dataDirs[flavor], binMapDir=f"patches/{flavor}/src/map", alt=alt)

from rom.rom import pc_to_snes, RealROM

rom = RealROM(vanilla)

statesChecksArgSize = {
    0xe5eb: 2,
    0xe612: 1,
    0xe629: 1
}

with open(asm, "w") as src:
    src.write("lorom\narch 65816\n\n")
    for room in rooms.values():
#        print(room["Name"])
        def processState(stateWordAddr):
            graphAreaId = areas.index(room['GraphArea'])
            minimapTypeId = minimapCfg.roomTypes[room["Name"]].id
            src.write(";;; %s\norg $8f%04x\n\tdb $%02x, $%02x\n" % (room['Name'], stateWordAddr+16, graphAreaId, minimapTypeId))
        address = room['Address']+11
        # process additionnal states
        while True:
            w=rom.readWord(address)
            if w == 0xe5e6:
                break
            address += 2 + statesChecksArgSize.get(w, 0)
            processState(rom.readWord(address))
            address += 2
        # default state
        processState((address+2)-0x70000)

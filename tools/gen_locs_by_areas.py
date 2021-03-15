#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# generate asm file listing vanilla locs IDs by area ID
asm=sys.argv[1]

# area ID is index in this list
areas = ["Ceres", "Crateria", "GreenPinkBrinstar", "RedBrinstar", "WreckedShip", "Kraid", "Norfair", "Crocomire", "LowerNorfair", "WestMaridia", "EastMaridia", "Tourian"]

from graph.location import locationsDict

def getLocIdsByArea(area):
    return [loc.Id for loc in locationsDict.values() if loc.Id is not None and loc.GraphArea == area] + [0xff]

with open(asm, "w") as src:
    src.write("locs_by_areas:\n\tdw "+','.join(["locs_"+area for area in areas]))
    for area in areas:
        src.write("\nlocs_"+area+":\n")
        locIds = getLocIdsByArea(area)
        src.write("\tdw "+','.join(["$%02x" % locId for locId in locIds]))
    src.write("\nprint pc\n")

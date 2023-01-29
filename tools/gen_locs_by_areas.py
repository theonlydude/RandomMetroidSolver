#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from graph.graph_utils import graphAreas as areas

# generate asm file listing vanilla locs IDs by area ID
asm=sys.argv[1]

from graph.location import locationsDict

def getLocIdsByArea(area):
    return [loc.Id for loc in locationsDict.values() if loc.Id is not None and not loc.isBoss() and loc.GraphArea == area] + [0xff]

with open(asm, "w") as src:
    src.write("include\n\n%export(locs_by_areas)\n\tdw "+','.join(["locs_"+area for area in areas]))
    src.write("\n%export(locs_start)")
    for area in areas:
        src.write("\n%export(locs_"+area+")\n")
        locIds = getLocIdsByArea(area)
        src.write("\tdb "+','.join(["$%02x" % locId for locId in locIds]))
    src.write("\n%export(locs_end)\n")

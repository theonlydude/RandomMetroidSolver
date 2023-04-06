#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from map.mirror_offsets import getOffsetFromFilePath
import graph.vanilla.graph_locations
from graph.location import locationsDict

w = 64
for locName, loc in locationsDict.items():
    if loc.MapAttrs is not None:
        offset = getOffsetFromFilePath(loc.Area)
        x = (w - offset - loc.MapAttrs.X) % w
        print(f"type(locationsDict['{locName}']).MapAttrs = LocationMapAttrs({x}, {loc.MapAttrs.Y}, {loc.MapAttrs.TileKind}, hFlip={not loc.MapAttrs.hFlip}, vFlip={loc.MapAttrs.vFlip})\n")

#!/usr/bin/python3

import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

from map.mirror_offsets import getOffsetFromFilePath
from graph.vanilla.map_tiles import objectives

w = 64 * 8

with open("graph/mirror/map_icons.py", "w") as fp:
    fp.write("def mirrorIcons(objectives):\n")
    for obj, objEntry in objectives.items():
        x, y = objEntry["map_coords_px"]
        offset = getOffsetFromFilePath(objEntry["area"])
        mx = (w - offset*8 - x) % w
        fp.write(f'\tobjectives["{obj}"]["map_coords_px"] = ({mx}, {y})\n')

#!/usr/bin/python3

import sys, os

dir_path = os.path.dirname(sys.path[0])
sys.path.append(dir_path)

# convert a yy-chr RGB palette line to asm
from utils.colors import RGB_24_to_15

pal = sys.argv[1]
line = int(sys.argv[2], 16)

nColors = 16
lineSize = nColors*3

asm = "dw "

with open(pal, "rb") as rgbPal:
    rgbPal.seek(line*lineSize)
    for i in range(nColors):
        colorRaw = rgbPal.read(3)
        rgb = RGB_24_to_15((int(colorRaw[0]), int(colorRaw[1]), int(colorRaw[2])))
        if i > 0:
            asm += ", "
        asm += "$%04x" % rgb

print(asm)

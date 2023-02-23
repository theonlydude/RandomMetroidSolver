#!/usr/bin/python3

import sys, os

dir_path = os.path.dirname(sys.path[0])
sys.path.append(dir_path)

# convert a yy-chr RGB palette line to asm
pal = sys.argv[1]
line = int(sys.argv[2], 16)

def RGB_24_to_15(color_tuple):
    R_adj = int(color_tuple[0])//8
    G_adj = int(color_tuple[1])//8
    B_adj = int(color_tuple[2])//8

    c = B_adj * 1024 + G_adj * 32 + R_adj
    return (c)

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

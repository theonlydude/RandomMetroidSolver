#!/usr/bin/python3

import sys, os

dir_path = os.path.dirname(sys.path[0])
sys.path.append(dir_path)

# convert a yy-chr RGB palette line to asm
from utils.colors import RGB_24_to_15, RGB_15_to_24
from rom.rom import RealROM

nColors = 16
lineSize = nColors*3

pal = sys.argv[1]

def yychr2asm(args):
    line = int(args[0], 16)
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

def bin2yychr(args):
    nLines = int(args[0])
    outFile = args[1]
    offset = int(args[2], 16) if len(args) > 2 else 0
    rom = RealROM(pal)
    rom.seek(offset)
    with open(outFile, "wb") as outPal:
        for _ in range(nLines):
            for _ in range(nColors):
                r, g, b = RGB_15_to_24(rom.readWord())
                rgb = [int(r*256), int(g*256), int(b*256)]
                outPal.write(bytearray(rgb))
    rom.close()

modes = {
    ".pal": yychr2asm,
    ".bin": bin2yychr,
    ".sfc": bin2yychr
}

_, ext = os.path.splitext(pal)
mode = modes.get(ext)
if mode is None:
    raise RuntimeError("Unknown palette extension: "+str(ext))

mode(sys.argv[2:])

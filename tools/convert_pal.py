#!/usr/bin/python3

import sys, os

dir_path = os.path.dirname(sys.path[0])
sys.path.append(dir_path)

from utils.colors import Palette

pal = sys.argv[1]

def yychr2asm(args):
    line = int(args[0], 16)
    Palette.load_yychr(pal, lines=[line]).print_asm()

def bin2yychr(args):
    nLines = int(args[0])
    outFile = args[1]
    offset = int(args[2], 16) if len(args) > 2 else 0
    Palette.load_snes(pal, offset=offset, lines=list(range(nLines))).save_yychr(outFile)

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

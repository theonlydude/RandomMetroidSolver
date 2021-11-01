#!/usr/bin/python3

import sys, os
from shutil import copyfile

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# extract ship palettes during outro mode7

from rom.rom import RealROM, snes_to_pc


rom = RealROM(sys.argv[1])

def extractRGB(color):
    R = ((color      ) % 32)
    G = ((color//32  ) % 32)
    B = ((color//1024) % 32)
    return (R, G, B)

def readPalette(rom, addr):
    rom.seek(addr)
    palette = []
    for i in range(16):
        palette.append(extractRGB(rom.readWord()))
    return palette

paletteAddr = snes_to_pc(0x8DD6BA) + 6

palettes = []
for i in range(16):
    addr = paletteAddr + 0x24*i
    palettes.append(readPalette(rom, addr))

# the one with the final colors is the last one
basePalette = palettes[-1]
#for palette in palettes:
#    print(palette)

# compute % inc/dec relative to base palette
evolution = []
for palette in palettes[:-1]:
    paletteEvol = []
    for color, base in zip(palette, basePalette):
        evol = [round(100 * (c - b) / b, 2) if b > 0 else c for c, b in zip(color, base)]
        paletteEvol.append(evol)
    evolution.append(paletteEvol)

for evol in evolution:
    print(evol)

# apply percent to base palette
computedPalettes = []
for evol in evolution:
    computedPalette = []
    for perc, color in zip(evol, basePalette):
        computedPalette.append([min(int(c + (c * p) / 100), 31) if c > 0 else p for p, c in zip(perc, color)])
    computedPalettes.append(computedPalette)
computedPalettes.append(basePalette)

for orig, new in zip(palettes, computedPalettes):
    print("")
    print(["({:2}, {:2}, {:2})".format(c[0], c[1], c[2]) for c in orig])
    print(["({:2}, {:2}, {:2})".format(c[0], c[1], c[2]) for c in new])

print(evolution)
print(len(evolution))


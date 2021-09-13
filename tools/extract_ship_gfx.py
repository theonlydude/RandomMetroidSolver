#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# extract ship tiles & layout & palette from hack, generate an ips in the end.

from rom.rom import snes_to_pc

vanilla = sys.argv[1]

tileAddr = [snes_to_pc(0xADB600), snes_to_pc(0xADC600)]
paletteAddr = [snes_to_pc(0xA2A59E), snes_to_pc(0xA2A5BE)]

with open(vanilla, 'rb') as vanillaRom:
    vanillaRom.seek(tileAddr[0])
    tileBytes = vanillaRom.read(tileAddr[1] - tileAddr[0])
    vanillaRom.seek(paletteAddr[0])
    paletteBytes = vanillaRom.read(paletteAddr[1] - paletteAddr[0])
with open('ship.gfx', 'wb') as ship:
    ship.write(tileBytes)
with open('ship.pal', 'wb') as palette:
    palette.write(paletteBytes)

print("ship.gfx and ship.pal extracted")

#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc, pc_to_snes
from rom.leveldata import Spritemap, Tilemap, Transform

romName = sys.argv[1]
rom = RealROM(romName)

spritemaps = [
0xA4CC3D,
0xA4CC94,
0xA4CCEB,
0xA4CD1F,
0xA4CD53,
0xA4CDA0,
0xA4CDED,
0xA4CDF9,
0xA4CE05,
0xA4CE0C,
0xA4CE13,
0xA4CE1A,
0xA4CE21,
0xA4CE28,
0xA4CE2F,
0xA4CE3B,
0xA4CE4C,
0xA4CE67,
0xA4CE7D,
0xA4CE84,
0xA4CE8B,
0xA4CE92,
0xA4CEC1,
0xA4CEF0,
0xA4CF15,
0xA4CF44,
0xA4CF69,
0xA4CF93,
0xA4CFBD,
0xA4CFE7,
0xA4D011,
0xA4D03B,
0xA4D065,
0xA4D08F,
0xA4D0B9,
0xA4D0E3,
0xA4D10D,
0xA4D137,
0xA4D161,
0xA4D18B,
0xA4D1B5,
0xA4D1DF,
0xA4D209,
0xA4D238,
0xA4D267,
0xA4D28C,
0xA4D2BB,
0xA4D2E0,
0xA4D30F,
0xA4D334,
0xA4D363,
0xA4D388,
0xA4D3B7,
0xA4D3E6,
0xA4D3FC,
0xA4D412,
0xA4D428,
0xA4D43E,
0xA4D454,
0xA4D465,
0xA4D47B,
0xA4D48C,
0xA4D493,
0xA4D4B3,
0xA4D4D3,
0xA4D4F3,
0xA4D509,
0xA4D515,

0xA4DB04,
0xA4DB79,
0xA4DC25,
0xA4DD08,
0xA4DE1D,
0xA4DE97,
0xA4DF48,
0xA4E030,

0xA4E74A,
0xA4E7A1,
0xA4E7F8,
0xA4E82C,
0xA4E860,
0xA4E8AD,
0xA4E8FA,
0xA4E906,
0xA4E912,
0xA4E919,
0xA4E920,
0xA4E927,
0xA4E92E,
0xA4E935,
0xA4E93C,
0xA4E948,
0xA4E959,
0xA4E974,
0xA4E98A,
0xA4E991,
0xA4E998,
0xA4E99F,
0xA4E9CE,
0xA4E9FD,
0xA4EA22,
0xA4EA51,
0xA4EA76,
0xA4EAA0,
0xA4EACA,
0xA4EAF4,
0xA4EB1E,
0xA4EB48,
0xA4EB72,
0xA4EB9C,
0xA4EBC6,
0xA4EBF0,
0xA4EC1A,
0xA4EC44,
0xA4EC6E,
0xA4EC98,
0xA4ECC2,
0xA4ECEC,
0xA4ED16,
0xA4ED45,
0xA4ED74,
0xA4ED99,
0xA4EDC8,
0xA4EDED,
0xA4EE1C,
0xA4EE41,
0xA4EE70,
0xA4EE95,
0xA4EEC4,
0xA4EEF3,
0xA4EF09,
0xA4EF1F,
0xA4EF35,
0xA4EF4B,
0xA4EF61,
0xA4EF72,
0xA4EF88,
0xA4EF99,
0xA4EFA0,
0xA4EFC0,
0xA4EFE0,
0xA4F000,
0xA4F016,
0xA4F022,

0xA4F5F3,
0xA4F5FA,
0xA4F60B,
0xA4F61C,
0xA4F62D,
0xA4F63E,
0xA4F64F,
0xA4F660,
0xA4F66C,
0xA4F673,

# Enemy projectile $8F9D (Crocomire bridge crumbling)
0x8D8109,
# Enemy projectile $90C1 (Crocomire spike wall pieces)
0x8D8110,
]


tilemaps = [
0xA4D51C,
0xA4D600,
0xA4D6DA,
0xA4D7B6,
0xA4D7EA,
0xA4D81E,
0xA4D852,
0xA4D876,
0xA4D89A,
0xA4D8BE,
0xA4DA4A,

0xA4F029,
0xA4F10D,
0xA4F1D3,
0xA4F2A5,
0xA4F2D9,
0xA4F30D,
0xA4F341,
0xA4F365,
0xA4F389,
0xA4F3AD,
0xA4F539,
]

asms = {}

# spritemaps
for addr in spritemaps:
    spritemap = Spritemap(rom, addr)
    spritemap.transform(Transform.Mirror)
    asmAddr, asm = spritemap.displayASM()
    asms[asmAddr] = asm

# extended spritemaps, update x
for start, end in [(0xA4BFC4, 0xA4CB00), (0xA4E1FE, 0xA4E720)]:
    curAddr = start
    while curAddr < end:
        rom.seek(snes_to_pc(curAddr))
        count = rom.readWord()
        for i in range(count):
            xAddr = curAddr + 2 + i*8
            rom.seek(snes_to_pc(xAddr))
            x = rom.readWord()
            invx = ((~x)+1) & 0xffff
            if x != invx:
                asms[xAddr] = """org ${:6x}
        dw ${:04x}""".format(xAddr, invx)
        curAddr += 2 + count*8

# tilemaps
crocSize = (32, 14)
rowSize = 0x40
for addr in tilemaps:
    tilemap = Tilemap(rom, addr, crocSize, rowSize)
    tilemap.transform(Transform.Mirror)
    asmAddr, asm = tilemap.displayASM()
    asms[asmAddr] = asm

# hitboxes
for start, end in [(0xA4CB05, 0xA4CC3D), (0xA4E720, 0xA4E74A)]:
    curAddr = start
    while curAddr < end:
        rom.seek(snes_to_pc(curAddr))
        count = rom.readWord()
        print("hitbox @{:x} with {} elements".format(curAddr, count))
        for i in range(count):
            baseAddr = curAddr + 2 + i*12
            rom.seek(snes_to_pc(baseAddr))
            x1 = rom.readWord()
            y1 = rom.readWord()
            x2 = rom.readWord()
            y2 = rom.readWord()
            invx1 = ((~x1)+1) & 0xffff
            invx2 = ((~x2)+1) & 0xffff

            if x1 & 0x8000 != 0 and x2 & 0x8000 != 0:
                if invx1 > invx2:
                    nx1 = invx2
                    nx2 = invx1
                else:
                    nx1 = invx1
                    nx2 = invx2
            elif x1 & 0x8000 != 0 and x2 & 0x8000 == 0:
                nx1 = invx2
                nx2 = invx1
            elif x1 & 0x8000 == 0 and x2 & 0x8000 != 0:
                raise Exception("x2 < x1 in hitbox {:x}".format(baseAddr))
            elif x1 & 0x8000 == 0 and x2 & 0x8000 == 0:
                if x1 > x2:
                    raise Exception("x1 > x2 in hitbox {:x}".format(baseAddr))
                nx1 = invx2
                nx2 = invx1

            asms[baseAddr] = """org ${:6x}
        dw ${:04x},${:04x},${:04x},${:04x}""".format(baseAddr, nx1, y1, nx2, y2)

        curAddr += 2 + count*12

# special BG2 when croc is melting
rowLength = 32*2
for addr in [0xA49C79, 0xA49E7B]:
    for row in range(8):
        rowAddr = addr + row*rowLength
        rom.seek(snes_to_pc(rowAddr))
        tiles = []
        for i in range(16):
            t = rom.readWord()
            if t != 0x0338: # if not empty tile
                vflip = (t >> 14) & 1
                vflip = 1 - vflip
                t = (t & 0xbfff) | (vflip << 14)
            tiles.insert(0, t)
        asms[rowAddr] = """org ${:6x}
    dw {}""".format(rowAddr, ",".join("${:04x}".format(t) for t in tiles))

print("==== updated spritemaps/tilemaps/hitboxes:")
for asmAddr in sorted(asms.keys()):
    print(asms[asmAddr])

rom.close()


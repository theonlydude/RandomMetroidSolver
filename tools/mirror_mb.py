#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc, pc_to_snes
from rom.leveldata import Spritemap, Tilemap, Transform
from rom.ips import IPS_Patch

romName = sys.argv[1]
rom = RealROM(romName)

spritemaps = [
0xA9A586,
0xA9A5BF,
0xA9A5F8,
0xA9A62C,
0xA9A660,
0xA9A694,
0xA9A69B,
0xA9A6D9,
0xA9A717,
0xA9A750,
0xA9A789,
0xA9A7C2,
0xA9A7F1,
0xA9A811,
0xA9A83B,
0xA9A85B,
0xA9A862,
0xA9A86E,
0xA9A87A,
0xA9A890,
0xA9A8A6,
0xA9A8D5,
0xA9A8F5,
0xA9A91F,
0xA9A93F,
0xA9A946,
0xA9A952,
0xA9A95E,
0xA9A974,
0xA9AD3E,
0xA9AD6D,
# falling tubes, already mirrored when mb moved to screen 4
#0xA9ADA1,
#0xA9ADD5,
#0xA9AE09,
#0xA9AE33,
#0xA9AE5D,

# Enemy projectile $CB83 (Mother Brain's rainbow beam charging)
0x8D93DB,
0x8D9414,
0x8D9439,
0x8D945E,
0x8D9483,
0x8D94B7,

# Enemy projectile $CB91/$CB9F (Mother Brain's drool)
0x8D94FF,
0x8D9506,
0x8D950D,
0x8D9514,
0x8D951B,
0x8D9522,
0x8D9529,
0x8D9530,
0x8D9537,
0x8D9543,

# Enemy projectile $CB2F (Mother Brain's purple breath - big)
0x8D954F,
0x8D955B,
0x8D9571,
0x8D9596,
0x8D95C0,
0x8D95E5,
0x8D9605,
0x8D961B,

# Enemy projectile $CB3D (Mother Brain's purple breath - small)
0x8D9627,
0x8D962E,
0x8D963A,
0x8D9650,
0x8D9666,
0x8D9677,
0x8D9688,
0x8D9694,

# Enemy projectile $CB21 (Mother Brain's exploded escape door particles)
0x8D969B,
0x8D96A2,
0x8D96A9,
0x8D96B0,
0x8D96B7,
0x8D96BE,
0x8D96C5,
0x8D96CC,
]

tilemaps = [
0xA9A98A,
0xA9AA4E,
0xA9AAEA,
0xA9AB70,
0xA9ABF6,
0xA9AC76,
0xA9ACE4,
]

asms = {}

# spritemaps
for addr in spritemaps:
    spritemap = Spritemap(rom, addr)
    spritemap.transform(Transform.Mirror)
    asmAddr, asm = spritemap.displayASM()
    asms[asmAddr] = asm

# extended spritemaps, update x
for start, end in [(0xA99FA0, 0xA9A4AC)]:
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
for start, end, length in [(0xA9A4AC, 0xA9A586, 12), (0xA9B427, 0xA9B455, 8)]:
    curAddr = start
    while curAddr < end:
        rom.seek(snes_to_pc(curAddr))
        count = rom.readWord()
        print("hitbox @{:x} with {} elements".format(curAddr, count))
        for i in range(count):
            baseAddr = curAddr + 2 + i*length
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

        curAddr += 2 + count*length

print("==== updated spritemaps/tilemaps/hitboxes:")
for asmAddr in sorted(asms.keys()):
    print(asms[asmAddr])

rom.close()

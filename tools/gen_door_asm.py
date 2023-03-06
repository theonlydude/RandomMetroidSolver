#!/usr/bin/python3
# generated mirrored door asm for scrolls updates

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc, pc_to_snes
from rom.leveldata import Room, Transform, Door
from rom.ips import IPS_Patch
from tools.rooms import rooms

vanillaRomName = sys.argv[1]
vanillaRom = RealROM(vanillaRomName)

asms = {}
for roomSpec in rooms:
    roomAddr = pc_to_snes(roomSpec["Address"])
    print("---- room @{:06x} - {}".format(roomAddr, roomSpec["Name"]))
    room = Room(vanillaRom, roomAddr)
    for door in room.doors:
        door.transform(Transform.Mirror, (room.width, room.height))
    for door in room.doors:
        if door.customASM != 0x8f0000:
            asmhead = ";;; Door to Room ${:04x}: {}\n".format(roomAddr & 0xffff, roomSpec["Name"])
            asmAddr, asm = door.displayASM()
            asm = asmhead + asm
            asms[asmAddr] = asm

print("==== updated scroll asm:")
for asmAddr in sorted(asms.keys()):
    print(asms[asmAddr])

vanillaRom.close()


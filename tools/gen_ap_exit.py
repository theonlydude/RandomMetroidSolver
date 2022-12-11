#!/usr/bin/env python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from graph.vanilla.graph_access import accessPointsDict
from rom.rom import RealROM, pc_to_snes, snes_to_pc

rom = RealROM(sys.argv[1])

for apName, ap in accessPointsDict.items():
    if ap.Internal:
        continue

    doorPtr = ap.ExitInfo['DoorPtr']
    address = snes_to_pc(0x830000 | doorPtr)

    rom.seek(address)
    DoorPtr = "0x{0:0{1}X}".format(doorPtr, 4)
    DestinationRoomHeaderPointer = "0x{0:0{1}X}".format(rom.readWord(), 4)
    BitFlag = "0x{0:0{1}X}".format(rom.readByte(), 2)
    Direction = "0x{0:0{1}X}".format(rom.readByte(), 2)
    XposLow = "0x{0:0{1}X}".format(rom.readByte(), 2)
    YPosLow = "0x{0:0{1}X}".format(rom.readByte(), 2)
    XPosHigh = "0x{0:0{1}X}".format(rom.readByte(), 2)
    YPosHigh = "0x{0:0{1}X}".format(rom.readByte(), 2)
    DistanceFromDoor = "0x{0:0{1}X}".format(rom.readWord(), 4)
    CustomDoorASM = "0x{0:0{1}X}".format(rom.readWord(), 4)

    print("""accessPointsDict['{}'].ExitInfo.update({{
    'DoorPtr': {},
    'direction': {},
    'cap': ({}, {}),
    'bitFlag': {},
    'screen': ({}, {}),
    'distanceToSpawn': {},
    'doorAsmPtr': {}
}})""".format(apName, DoorPtr, Direction, XposLow, YPosLow, BitFlag, XPosHigh, YPosHigh, DistanceFromDoor, CustomDoorASM))


for apName, ap in accessPointsDict.items():
    if ap.Internal:
        continue

    roomAddr = snes_to_pc(0x8f0000 | ap.RoomInfo['RoomPtr'])
    # read room size in screens
    rom.seek(roomAddr + 4)
    swidth = rom.readByte()
    sheight = rom.readByte()
    # a screen is 256 pixels long
    pwidth = swidth * 256

    samusX = ap.EntryInfo['SamusX']
    samusX = pwidth - 1 - samusX
    samusY = ap.EntryInfo['SamusY']

    print("""accessPointsDict['{}'].EntryInfo = {{
    'SamusX': {},
    'SamusY': {}
}}""".format(apName, hex(samusX), hex(samusY)))

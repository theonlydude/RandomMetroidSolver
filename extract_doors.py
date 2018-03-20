#!/usr/bin/python

# get info from https://github.com/DJuttmann/SM3E

import sys, struct
from rooms import rooms

def concatBytes(b0, b1, b2):
    return b0 + (b1 << 8) + (b2 << 16)

def LRtoPC(B):
    B_1 = B >> 16
    B_2 = B & 0xFFFF
    # return 0 if invalid LoROM address
    if B_1 < 0x80 or B_1 > 0xFFFFFF or B_2 < 0x8000:
        return 0
    A_1 = (B_1 - 0x80) >> 1
    # if B_1 is even, remove most significant bit
    A_2 = B_2 & 0x7FFF if (B_1 & 1) == 0 else B_2

    return (A_1 << 16) | A_2

def readDoorsPtrs(romFile, roomInfo):
    size = roomInfo['doorCount'] * 2
    doorsPtr = LRtoPC(roomInfo['doorsPtr'])
    print("doorsPtr {} LRtoPC {}".format(hex(roomInfo['doorsPtr']), hex(doorsPtr)))
    romFile.seek(doorsPtr)
    data = struct.unpack("B"*size, romFile.read(size))

    doorPtrs = []
    for n in range(0, roomInfo['doorCount']):
        doorPtrs.append(concatBytes(data[2*n], data[2*n + 1], 0x83))

    roomInfo['doorPtrs'] = doorPtrs

    print("doorPtrs: {}".format([hex(d) for d in doorPtrs]))

def readDoorsData(romFile, roomInfo):
    size = 12

    doorData = []

    for doorPtr in roomInfo['doorPtrs']:
        doorPtr = LRtoPC(doorPtr)
        romFile.seek(doorPtr)
        data = struct.unpack("B"*size, romFile.read(size))
        print([hex(d) for d in data])

        if data[0] == 0 and data[1] == 0:
            doorData.append({'type': 'elevator',
                             'startAddressPC': doorPtr})
        else:
            #      RoomPtr         = Tools.ConcatBytes (b [0], b [1], 0x8F);
            #      Bitflag         = b [2];
            #      Direction       = b [3];
            #      DoorCapX        = b [4];
            #      DoorCapY        = b [5];
            #      ScreenX         = b [6];
            #      ScreenY         = b [7];
            #      DistanceToSpawn = Tools.ConcatBytes (b [8], b [9]);
            #      DoorAsmPtr      = Tools.ConcatBytes (b [10], b [11], 0x8F);
            #      startAddressPC = addressPC;
            doorData.append({'type': 'door',
                             'roomPrt': hex(concatBytes(data[0], data[1], 0x8F)),
                             'doorAsmPtr': hex(concatBytes(data[10], data[11], 0x8F)),
                             'startAddressPC': hex(doorPtr)})

    roomInfo['doorData'] = doorData
    print("doorData: {}".format(doorData))

def readRooms(romFileName):
    #    RoomIndex         = b [0];
    #    Area              = b [1];
    #    MapX              = b [2];
    #    MapY              = b [3];
    #    Width             = b [4];
    #    Height             = b [5];
    #    UpScroller        = b [6];
    #    DownScroller      = b [7];
    #    SpecialGfxBitflag = b [8];
    #    DoorsPtr          = Tools.ConcatBytes (b [9], b [10], 0x8F);
    HeaderSize = 11

    with open(romFileName, 'r') as romFile:
        for roomInfo in rooms:
            romFile.seek(roomInfo['address']+9)

            value = struct.unpack("B"*2, romFile.read(2))

            doorsPtr = concatBytes(value[0], value[1], 0x8F)
            roomInfo['doorsPtr'] = doorsPtr
            print("{} ({}) doorsPtr: {}".format(roomInfo['name'], hex(roomInfo['address']), hex(doorsPtr)))

            readDoorsPtrs(romFile, roomInfo)
            readDoorsData(romFile, roomInfo)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing param: ROM")
        sys.exit(1)

    readRooms(sys.argv[1])

#!/usr/bin/python

# get info from https://github.com/DJuttmann/SM3E

import sys, struct
from rooms import roomsDoor
rooms = roomsDoor

def concatBytes(b0, b1, b2=0):
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
    doorsPtr = roomInfo['doorsPtr']
    romFile.seek(doorsPtr)
    data = struct.unpack("B"*size, romFile.read(size))

    doorPtrs = []
    for n in range(0, roomInfo['doorCount']):
        doorPtrs.append(LRtoPC(concatBytes(data[2*n], data[2*n + 1], 0x83)))

    roomInfo['doorPtrs'] = doorPtrs

def matchDirection(roomDirection, doorDirection):
    if roomDirection == 'all':
        return True
    if roomDirection == 'up' and doorDirection in (0x3, 0x7):
        return True
    if roomDirection == 'down' and doorDirection in (0x2, 0x6):
        return True
    if roomDirection == 'left' and doorDirection in (0x1, 0x5):
        return True
    if roomDirection == 'right' and doorDirection in (0x0, 0x4):
        return True
    return False

def readDoorsData(romFile, roomInfo):
    size = 12

    doorData = []

    #print("Doors raw data:")
    for doorPtr in roomInfo['doorPtrs']:
        romFile.seek(doorPtr)
        data = struct.unpack("B"*size, romFile.read(size))
        # print("{}: {}".format(hex(doorPtr), [hex(d) for d in data]))

        if data[0] != 0 and data[1] != 0:
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
            if matchDirection(roomInfo['direction'], data[3]):
                doorData.append({'doorPtr': hex(doorPtr),
                                 'roomPrt': hex(concatBytes(data[0], data[1])),
                                 'bitFlag': hex(data[2]),
                                 'direction': hex(data[3]),
                                 'capX': hex(data[4]),
                                 'capY': hex(data[5]),
                                 'screenX': hex(data[6]),
                                 'screenY': hex(data[7]),
                                 'distanceToSpawn': hex(concatBytes(data[8], data[9])),
                                 'doorAsmPtr': hex(concatBytes(data[10], data[11], 0x8F))})

    roomInfo['doorData'] = doorData
    #print("Doors Data:")
    for d in doorData:
        print("\"doorPtr\": {}, \"roomPrt\": {}, \"direction\": {}, \"cap\": ({}, {}), \"screen\": ({}, {}), \"distanceToSpawn\": {}, \"doorAsmPtr\": {}, \"bitFlag\": {}".format(d['doorPtr'], d['roomPrt'], d['direction'], d['capX'], d['capY'], d['screenX'], d['screenY'], d['distanceToSpawn'], d['doorAsmPtr'], d['bitFlag']))

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
            romFile.seek(roomInfo['address'])
            data = struct.unpack("B"*HeaderSize, romFile.read(HeaderSize))
            roomInfo['area'] = data[1]
            doorsPtr = LRtoPC(concatBytes(data[9], data[10], 0x8F))
            roomInfo['doorsPtr'] = doorsPtr
            print("")
            print("{} ({}) in area: {}".format(roomInfo['name'], hex(roomInfo['address']), hex(roomInfo['area'])))

            readDoorsPtrs(romFile, roomInfo)
            readDoorsData(romFile, roomInfo)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing param: ROM")
        sys.exit(1)

    readRooms(sys.argv[1])

#!/usr/bin/python3

# get info from https://github.com/DJuttmann/SM3E

import sys, os
# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rooms import rooms
from rom.rom import RealROM
from utils.utils import removeChars

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
    size = roomInfo['DoorCount'] * 2
    doorsPtr = roomInfo['DoorsPtr']
    romFile.seek(doorsPtr)
    data = romFile.read(size)

    doorPtrs = []
    for n in range(0, roomInfo['DoorCount']):
        doorPtrs.append(LRtoPC(concatBytes(data[2*n], data[2*n + 1], 0x83)))

    roomInfo['DoorPtrs'] = doorPtrs

direction2name = {
    0x03: 'up',
    0x07: 'up',
    0x02: 'down',
    0x06: 'down',
    0x01: 'left',
    0x05: 'left',
    0x00: 'right',
    0x04: 'right'
}

def matchDirection(roomDirection, doorDirection):
    if roomDirection == 'all':
        return True
    return roomDirection == direction2name[doorDirection]

def readDoorsData(romFile, roomInfo):
    size = 12

    doorData = []

    #print("Doors raw data:")
    for doorPtr in roomInfo['DoorPtrs']:
        romFile.seek(doorPtr)
        data = romFile.read(size)
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
            doorData.append({'doorPtr': doorPtr,
                             'roomPtr': concatBytes(data[0], data[1]),
                             'bitFlag': data[2],
                             'direction': data[3],
                             'capX': data[4],
                             'capY': data[5],
                             'screenX': data[6],
                             'screenY': data[7],
                             'distanceToSpawn': concatBytes(data[8], data[9]),
                             'doorAsmPtr': concatBytes(data[10], data[11], 0x8F)})

    roomInfo['DoorData'] = doorData
    #for d in doorData:
    #    print("\"doorPtr\": {}, \"roomPtr\": {}, \"direction\": {}, \"cap\": ({}, {}), \"screen\": ({}, {}), \"distanceToSpawn\": {}, \"doorAsmPtr\": {}, \"bitFlag\": {}".format(hex(d['doorPtr']), hex(d['roomPtr']), hex(d['direction']), hex(d['capX']), hex(d['capY']), hex(d['screenX']), hex(d['screenY']), hex(d['distanceToSpawn']), hex(d['doorAsmPtr']), hex(d['bitFlag'])))

class RoomHeader:
    Size = 11
    RoomIndex = 0
    Area = 1
    MapX = 2
    MapY = 3
    Width = 4
    Height = 5
    UpScroller = 6
    DownScroller = 7
    SpecialGfxBitflag = 8
    DoorsPtr1 = 9
    DoorsPtr2 = 10

class Areas:
    Crateria = 0
    Brinstar = 1
    Norfair = 2
    WreckedShip = 3
    Maridia = 4
    Tourian = 5
    Ceres = 6
    Debug = 7

    id2name = {
        Crateria: "Crateria",
        Brinstar: "Brinstar",
        Norfair: "Norfair",
        WreckedShip: "WreckedShip",
        Maridia: "Maridia",
        Tourian: "Tourian",
        Ceres: "Ceres",
        Debug: "Debug"
    }

def readRooms(romFileName):
    romFile = RealROM(romFileName)
    for roomInfo in rooms:
        romFile.seek(roomInfo['Address'])
        data = romFile.read(RoomHeader.Size)
        roomInfo['RoomIndex'] = data[RoomHeader.RoomIndex]
        roomInfo['Area'] = data[RoomHeader.Area]
        roomInfo['MapX'] = data[RoomHeader.MapX]
        roomInfo['MapY'] = data[RoomHeader.MapY]
        roomInfo['Width'] = data[RoomHeader.Width]
        roomInfo['Height'] = data[RoomHeader.Height]
        roomInfo['UpScroller'] = data[RoomHeader.UpScroller]
        roomInfo['DownScroller'] = data[RoomHeader.DownScroller]
        roomInfo['SpecialGfxBitflag'] = data[RoomHeader.SpecialGfxBitflag]
        roomInfo['DoorsPtr'] = LRtoPC(concatBytes(data[RoomHeader.DoorsPtr1], data[RoomHeader.DoorsPtr2], 0x8F))
        #print("")
        #print("{} ({}) ({} x {}) in area: {}".format(roomInfo['Name'], hex(roomInfo['Address']), hex(roomInfo['Width']), hex(roomInfo['Height']), Areas.id2name[roomInfo['Area']]))

        readDoorsPtrs(romFile, roomInfo)
        readDoorsData(romFile, roomInfo)

    roomsGraph = {}
    for roomInfo in rooms:
        nodeName = removeChars(roomInfo['Name'], "][ '-")
        address = roomInfo['Address'] & 0xFFFF
        roomsGraph[address] = {'Name': nodeName, 'Area': roomInfo['Area'], 'Width': roomInfo['Width'], 'Height': roomInfo['Height'], 'Doors': {}}
        for doorData in roomInfo["DoorData"]:
            roomsGraph[address]['Doors'][doorData['doorPtr']] = {'roomPtr': doorData['roomPtr'], 'exitScreenX': doorData['screenX'], 'exitScreenY': doorData['screenY'], 'exitDirection': doorData['direction']}

    # get screen data from corresponding door
    for (entryRoomAddress, entryRoom) in roomsGraph.items():
        for entryDoorData in entryRoom["Doors"].values():
            exitRoomAddress = entryDoorData['roomPtr']
            exitRoom = roomsGraph[exitRoomAddress]
            found = False
            for exitDoorData in exitRoom['Doors'].values():
                #if entryRoom['Name'] in ['GrappleTutorialRoom1', 'GrappleBeamRoom']:
                    #print("entry doors count: {} exit doors count: {}".format(len(entryRoom["Doors"]), len(exitRoom['Doors'])))
                    #print("{}/{} -> {}/{} ({})".format(entryRoom['Name'], hex(entryRoomAddress), exitRoom['Name'], hex(exitDoorData['roomPtr']), roomsGraph[exitDoorData['roomPtr']]['Name']))
                if exitDoorData['roomPtr'] == entryRoomAddress:
                    #if entryRoom['Name'] in ['GrappleTutorialRoom1', 'GrappleBeamRoom']:
                        #print("exitDoorData['roomPtr'] {} == entryRoomAddress {}".format(hex(exitDoorData['roomPtr']), hex(entryRoomAddress)))
                    for entryDoorData in entryRoom['Doors'].values():
                        if entryDoorData['roomPtr'] == exitRoomAddress:
                            entryDoorData['entryScreenX'] = exitDoorData['exitScreenX']
                            entryDoorData['entryScreenY'] = exitDoorData['exitScreenY']
                            entryDoorData['entryDirection'] = exitDoorData['exitDirection']
                            found = True
                #else:
                    #if entryRoom['Name'] in ['GrappleTutorialRoom1', 'GrappleBeamRoom']:
                        #print("exitDoorData['roomPtr'] {} != entryRoomAddress {}".format(hex(exitDoorData['roomPtr']), hex(entryRoomAddress)))
            #if found == False:
                #print("door not found ({} -> {})".format(entryRoom['Name'], exitRoom['Name']))
                #print("-----------------------------------------------------------------------------")

    #print(roomsGraph)

    print("""digraph {
size="30,30!";
graph [overlap=orthoxy, splines=false, nodesep="1"];
node [shape="plaintext",fontsize=30];
edge [color="#0025fa80"];
""")
    for (address, roomInfo) in roomsGraph.items():
        if roomInfo['Area'] == Areas.Tourian:
            src = roomInfo['Name']
            print("{} [label = {}];".format(roomInfo['Name'], genLabel(roomInfo['Name'], roomInfo["Width"], roomInfo["Height"])))
            for doorData in roomInfo["Doors"].values():
                dstInfo = roomsGraph[doorData['roomPtr']]
                dst = dstInfo['Name']
                print("{}:x{}{}:{} -> {}:x{}{}:{};".format(src, doorData.get('entryScreenX'), doorData.get('entryScreenY'), getDir(doorData.get('entryDirection')), dst, doorData.get('exitScreenX'), doorData.get('exitScreenY'), getDir(doorData.get('exitDirection'))))
    print("}")

def genLabel(name, sizeX, sizeY):
    ret = """<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
    <TR><TD colspan="{}">{}</TD></TR>""".format(sizeX, name)
    for y in range(sizeY):
        ret += """<TR>"""
        for x in range(sizeX):
            ret += """<TD PORT="x{}{}">({},{})</TD>""".format(x, y, x, y)
        ret += """</TR>"""
    ret += """</TABLE>>"""
    return ret

def getDir(direction):
    if direction in [3,7]: # up
        return 's'
    elif direction in [2,6]: # down
        return 'n'
    elif direction in [1,5]: # left
        return 'e'
    elif direction in [0,4]: # right
        return 'w'

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing param: ROM")
        sys.exit(1)

    readRooms(sys.argv[1])

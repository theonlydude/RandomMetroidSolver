#!/usr/bin/python3

import sys, os
from enum import IntEnum

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))
sys.path.insert(0, os.path.dirname(sys.path[0]))

from logic.logic import Logic
from rom.flavor import RomFlavor
from rom.rom import RealROM, pc_to_snes, snes_to_pc
from rom.leveldata import Room
from utils.doorsmanager import DoorsManager, plmFacing
from graph.graph_utils import getAccessPoint, GraphUtils

# for vanilla the vanilla rom
# for mirror the vanilla rom + mirror base patchs (in RomPatcher.IPSPatches['Logic']['mirror'])

rom = RealROM(sys.argv[1])
logic = sys.argv[2]

Logic.factory(logic)
RomFlavor.factory()
locations = Logic.locations

locationsDict = {pc_to_snes(loc.Address): loc for loc in locations}
locationsName = set([loc.Name for loc in locations])
accessPoints = Logic.accessPoints
patchDict = RomFlavor.patchAccess.getDictPatches()
additionalPLMs = RomFlavor.patchAccess.getAdditionalPLMs()

crateria = {}
tourian = {}
green_pink_bt = {}
red_bt = {}
wreckedship = {}
west_maridia = {}
east_maridia = {}
kraid_lair = {}
norfair = {}
lower_norfair = {}
crocomire = {}
phantoon = {}
draygon = {}
kraid = {}
ridley = {}

# each area map is 64x32 screens in game
# vanilla area id
class Area(IntEnum):
    Crateria = 0
    Brinstar = 1
    Norfair = 2
    WreckedShip = 3
    Maridia = 4
    Tourian = 5
    Ceres = 6
    Debug = 7

roomsAddr = {}
roomsAddr["vanilla"] = [0x8f91f8, 0x8f92b3, 0x8f92fd, 0x8f93aa, 0x8f93d5, 0x8f93fe, 0x8f9461, 0x8f948c, 0x8f94cc, 0x8f94fd, 0x8f9552, 0x8f957d, 0x8f95a8, 0x8f95d4, 0x8f95ff, 0x8f962a, 0x8f965b, 0x8f968f, 0x8f96ba, 0x8f975c, 0x8f97b5, 0x8f9804, 0x8f9879, 0x8f98e2, 0x8f990d, 0x8f9938, 0x8f9969, 0x8f9994, 0x8f99bd, 0x8f99f9, 0x8f9a44, 0x8f9a90, 0x8f9ad9, 0x8f9b5b, 0x8f9b9d, 0x8f9bc8, 0x8f9c07, 0x8f9c35, 0x8f9c5e, 0x8f9c89, 0x8f9cb3, 0x8f9d19, 0x8f9d9c, 0x8f9dc7, 0x8f9e11, 0x8f9e52, 0x8f9e9f, 0x8f9f11, 0x8f9f64, 0x8f9fba, 0x8f9fe5, 0x8fa011, 0x8fa051, 0x8fa07b, 0x8fa0a4, 0x8fa0d2, 0x8fa107, 0x8fa130, 0x8fa15b, 0x8fa184, 0x8fa1ad, 0x8fa1d8, 0x8fa201, 0x8fa22a, 0x8fa253, 0x8fa293, 0x8fa2ce, 0x8fa2f7, 0x8fa322, 0x8fa37c, 0x8fa3ae, 0x8fa3dd, 0x8fa408, 0x8fa447, 0x8fa471, 0x8fa4b1, 0x8fa4da, 0x8fa521, 0x8fa56b, 0x8fa59f, 0x8fa5ed, 0x8fa618, 0x8fa641, 0x8fa66a, 0x8fa6a1, 0x8fa6e2, 0x8fa70b, 0x8fa734, 0x8fa75d, 0x8fa788, 0x8fa7b3, 0x8fa7de, 0x8fa815, 0x8fa865, 0x8fa890, 0x8fa8b9, 0x8fa8f8, 0x8fa923, 0x8fa98d, 0x8fa9e5, 0x8faa0e, 0x8faa41, 0x8faa82, 0x8faab5, 0x8faade, 0x8fab07, 0x8fab3b, 0x8fab64, 0x8fab8f, 0x8fabd2, 0x8fac00, 0x8fac2b, 0x8fac5a, 0x8fac83, 0x8facb3, 0x8facf0, 0x8fad1b, 0x8fad5e, 0x8fadad, 0x8fadde, 0x8fae07, 0x8fae32, 0x8fae74, 0x8faeb4, 0x8faedf, 0x8faf14, 0x8faf3f, 0x8faf72, 0x8fafa3, 0x8fafce, 0x8faffb, 0x8fb026, 0x8fb051, 0x8fb07a, 0x8fb0b4, 0x8fb0dd, 0x8fb106, 0x8fb139, 0x8fb167, 0x8fb192, 0x8fb1bb, 0x8fb1e5, 0x8fb236, 0x8fb283, 0x8fb2da, 0x8fb305, 0x8fb32e, 0x8fb37a, 0x8fb3a5, 0x8fb40a, 0x8fb457, 0x8fb482, 0x8fb4ad, 0x8fb4e5, 0x8fb510, 0x8fb55a, 0x8fb585, 0x8fb5d5, 0x8fb62b, 0x8fb656, 0x8fb698, 0x8fb6c1, 0x8fb6ee, 0x8fb741, 0x8fc98e, 0x8fca08, 0x8fca52, 0x8fcaae, 0x8fcaf6, 0x8fcb8b, 0x8fcbd5, 0x8fcc27, 0x8fcc6f, 0x8fcccb, 0x8fcd13, 0x8fcd5c, 0x8fcda8, 0x8fcdf1, 0x8fce40, 0x8fce8a, 0x8fced2, 0x8fcefb, 0x8fcf54, 0x8fcf80, 0x8fcfc9, 0x8fd017, 0x8fd055, 0x8fd08a, 0x8fd0b9, 0x8fd104, 0x8fd13b, 0x8fd16d, 0x8fd1a3, 0x8fd1dd, 0x8fd21c, 0x8fd252, 0x8fd27e, 0x8fd2aa, 0x8fd2d9, 0x8fd30b, 0x8fd340, 0x8fd387, 0x8fd3b6, 0x8fd3df, 0x8fd408, 0x8fd433, 0x8fd461, 0x8fd48e, 0x8fd4c2, 0x8fd4ef, 0x8fd51e, 0x8fd54d, 0x8fd57a, 0x8fd5a7, 0x8fd5ec, 0x8fd617, 0x8fd646, 0x8fd69a, 0x8fd6d0, 0x8fd6fd, 0x8fd72a, 0x8fd765, 0x8fd78f, 0x8fd7e4, 0x8fd81a, 0x8fd845, 0x8fd86e, 0x8fd898, 0x8fd8c5, 0x8fd913, 0x8fd95e, 0x8fd9aa, 0x8fd9d4, 0x8fd9fe, 0x8fda2b, 0x8fda60, 0x8fdaae, 0x8fdae1, 0x8fdb31, 0x8fdb7d, 0x8fdbcd, 0x8fdc19, 0x8fdc65, 0x8fdcb1, 0x8fdcff, 0x8fdd2e, 0x8fdd58, 0x8fddc4, 0x8fddf3, 0x8fde23, 0x8fde4d, 0x8fde7a, 0x8fdea7, 0x8fdede, 0x8fdf1b, 0x8fdf45, 0x8fdf8d, 0x8fdfd7, 0x8fe021, 0x8fe06b, 0x8fe0b5]

roomsAddr["mirror"] = roomsAddr["vanilla"][:]
# new MB room
roomsAddr["mirror"].append(0x8ffd40)

# loop on room, for each get it's area, map x/y, width/height, plms
# loop on plms to get doors/items
# for door get direction and screen x/y
# for item get screen x/y
rooms = {}
for roomAddrS in roomsAddr[logic]:
    roomAddrPC = snes_to_pc(roomAddrS)
    room = Room(rom, roomAddrPC)
    room.loadPLMs()
    rooms[roomAddrS] = room

# match room plm and loc address
items = {}
foundLocs = set()
for roomAddrS, room in rooms.items():
    for itemAddr in room.items:
        # old croc etank
        if itemAddr == 0x8f8ba4:
            continue
        loc = locationsDict[itemAddr]
        itemPlm = room.plms[itemAddr]
        items[itemAddr] = {'loc': loc, 'itemPlm': itemPlm, 'room': roomAddrS}
        foundLocs.add(loc.Name)

for itemAddr, values in items.items():
    print("{}: room: {} loc: {} x: {} y: {}".format(hex(itemAddr), hex(values['room']) , values['loc'].Name, values['itemPlm'][1], values['itemPlm'][2]))

missingLocs = locationsName - foundLocs
print("missingLocs: {}".format(missingLocs))

# match room plm and doors addresses
doorsDict = {door.address: door for door in DoorsManager.doors.values()}
doorsName = set([door.name for door in DoorsManager.doors.values()])

doors = {}
foundDoors = set()
for roomAddrS, room in rooms.items():
    for doorAddr in room.doors:
        # we don't have all doors in varia (like some grey doors in some states)
        if doorAddr not in doorsDict:
            continue
        door = doorsDict[doorAddr]
        doorPlm = room.plms[doorAddr]
        doors[doorAddr] = {'door': door, 'doorPlm': doorPlm, 'room': roomAddrS, 'facing': plmFacing[doorPlm[0]]}
        foundDoors.add(door.name)

for doorAddr, values in doors.items():
    print("{}: room: {} door: {} x: {} y: {} facing: {}".format(hex(doorAddr), hex(values['room']) , values['door'].name, values['doorPlm'][1], values['doorPlm'][2], values['facing']))

missingDoors = doorsName - foundDoors
print("missingDoors: {}".format(missingDoors))


# object in tiles coordinates in room
def getMapPos(roomPos, objPos):
    (roomX, roomY) = roomPos
    (objX, objY) = objPos
    x = roomX + objX // 0x10
    y = roomY + objY // 0x10
    byteIndex = (y + (x & 0x20)) * 4 + (x & 0x1F) // 8
    # first line of map is unused, so add 4 to ignore it (8 bytes per lines, but 4 in each page)
    byteIndex += 4
    bitMask = 0x80 >> (x & 7)
    return (byteIndex, bitMask)

print("    nothingScreens = {")
print('        "{}": {{'.format(logic))
for item in items.values():
    room = rooms[item['room']]
    roomX = room.mapX
    roomY = room.mapY
    itemPlm = item['itemPlm']
    itemX = itemPlm[1]
    itemY = itemPlm[2]
    (byteIndex, bitMask) = getMapPos((roomX, roomY), (itemX, itemY))

    # "Energy Tank, Gauntlet": {"byteIndex": 14, "bitMask": 64, "room": 0x965b, "area": "Crateria"},
    print('            "{}": {{"byteIndex": {}, "bitMask": {}, "room": {}, "area": "{}"}},'.format(
        item['loc'].Name, byteIndex, bitMask, hex(pc_to_snes(room.dataAddr) & 0xffff), Area(room.area).name))
print("        },")
print("    }")


print("    doorsScreen = {")
print('        "{}": {{'.format(logic))
for door in doors.values():
    doorObj = door['door']
    room = rooms[door['room']]
    roomX = room.mapX
    roomY = room.mapY
    doorPlm = door['doorPlm']
    doorX = doorPlm[1]
    doorY = doorPlm[2]
    (byteIndex, bitMask) = getMapPos((roomX, roomY), (doorX, doorY))

    # 'LandingSiteRight': {"byteIndex": 23, "bitMask": 1, "room": 0x91f8, "area": "Crateria"},
    print('            "{}": {{"byteIndex": {}, "bitMask": {}, "room": {}, "area": "{}"}},'.format(
        doorObj.name, byteIndex, bitMask, hex(pc_to_snes(room.dataAddr) & 0xffff), Area(room.area).name))
print("        },")
print("    }")

accessPointsIds = {
    "areaAccessPoints": [
        "Lower Mushrooms Left", 
        "Green Pirates Shaft Bottom Right", 
        "Moat Right", 
        "Keyhunter Room Bottom", 
        "Morph Ball Room Left", 
        "Green Brinstar Elevator", 
        "Green Hill Zone Top Right", 
        "Noob Bridge Right", 
        "West Ocean Left", 
        "Crab Maze Left", 
        "Lava Dive Right", 
        "Three Muskateers Room Left", 
        "Warehouse Zeela Room Left", 
        "Warehouse Entrance Left", 
        "Warehouse Entrance Right", 
        "Single Chamber Top Right", 
        "Kronic Boost Room Bottom Left", 
        "Crocomire Speedway Bottom", 
        "Crocomire Room Top", 
        "Main Street Bottom", 
        "Crab Hole Bottom Left", 
        "Red Fish Room Left", 
        "Crab Shaft Right", 
        "Aqueduct Top Left", 
        "Le Coude Right", 
        "Red Tower Top Left", 
        "Caterpillar Room Top Right", 
        "Red Brinstar Elevator", 
        "East Tunnel Right", 
        "East Tunnel Top Right", 
        "Glass Tunnel Top", 
        "Golden Four", 
    ],

    "bossAccessPoints": [
        "PhantoonRoomOut", 
        "PhantoonRoomIn", 
        "RidleyRoomOut", 
        "RidleyRoomIn", 
        "KraidRoomOut", 
        "KraidRoomIn", 
        "DraygonRoomOut", 
        "DraygonRoomIn", 
    ],

    "escapeAccessPoints": [
        'Tourian Escape Room 4 Top Right', 
        'Climb Bottom Left', 
        'Green Brinstar Main Shaft Top Left', 
        'Basement Left', 
        'Business Center Mid Left', 
        'Crab Hole Bottom Right', 
    ]
}

for aptype, aps in accessPointsIds.items():
    print("    {} = {{".format(aptype))
    print('        "{}": {{'.format(logic))
    for apName in aps:
        ap = getAccessPoint(apName)
        roomPtr = ap.RoomInfo['RoomPtr']

        blinking = 'Blinking[{}]'.format(apName)

        plm = None
        if blinking in additionalPLMs:
            plm = additionalPLMs[blinking]['plm_bytes_list'][0]
        elif blinking in patchDict:
            for addr, data in patchDict[blinking].items():
                if (pc_to_snes(addr) >> 16) == 0x8f:
                    plm = data
                    break

        room = rooms[0x8f0000 + roomPtr]
        roomX = room.mapX
        roomY = room.mapY
        if plm is not None:
            doorX = plm[2]
            doorY = plm[3]
        else:
            # most escape AP don't blink... so get data directly from access points
            oppositeApName = GraphUtils.getVanillaExit(apName)
            oppositeAp = getAccessPoint(oppositeApName)
            doorX = oppositeAp.ExitInfo['cap'][0]
            doorY = oppositeAp.ExitInfo['cap'][1]
        (byteIndex, bitMask) = getMapPos((roomX, roomY), (doorX, doorY))

        # "Lower Mushrooms Left": {"byteIndex": 36, "bitMask": 1, "room": 0x9969, "area": "Crateria"},
        print('            "{}": {{"byteIndex": {}, "bitMask": {}, "room": {}, "area": "{}"}},'.format(
            apName, byteIndex, bitMask, hex(roomPtr), Area(room.area).name))
    print("        },")
    print("    }")

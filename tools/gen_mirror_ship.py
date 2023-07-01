#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM
from rom.leveldata import Room, BoundingRect

# rom with collision ship patch applied
vanillaRom = RealROM(sys.argv[1])
# minimum mirrortroid rom
mirrorRom = RealROM(sys.argv[2])

# landing site
roomAddr = 0x8f91f8
vRoom = Room(vanillaRom, roomAddr)
mRoom = Room(mirrorRom, roomAddr)

# all states have same level data in landing site
vLevelData = vRoom.levelData[vRoom.defaultRoomState.levelDataPtr]
mLevelData = mRoom.levelData[mRoom.defaultRoomState.levelDataPtr]

# copy level data behind ship
screen = (4, 4)
boundingRect = BoundingRect((0, 0, 256, 192))

# as ships are symmetrical we don't have to mirror level data
mLevelData.pasteLayout(vLevelData.copyLayout(screen, boundingRect), screen, boundingRect)

vanillaSize = 5165
mLevelData.write(vanillaSize)

vanillaRom.close()
mirrorRom.close()

#!/usr/bin/python3

import sys, os
from shutil import copyfile

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# extract ship tiles & layout & palette from hack, generate an ips in the end.

from rom.rom import RealROM, snes_to_pc
from rom.ips import IPS_Patch
from rom.leveldata import LevelData, Ship, Room

vanilla = sys.argv[1]
hack = sys.argv[2]
fixEscape = len(sys.argv) > 2

print("fix escape: {}".format(fixEscape))

# copy vanilla in tmpfile
tmpfile = '/tmp/vanilla.sfc'
copyfile(vanilla, tmpfile)

# extract data from hack
addresses = {
    "tilesAddr": {"vanilla": [snes_to_pc(0xADB600), snes_to_pc(0xADC600)],
                  "hack":    [snes_to_pc(0xADB600), snes_to_pc(0xADC600)]},
    "palettesAddr": {"vanilla": [snes_to_pc(0xA2A59E), snes_to_pc(0xA2A5BE)],
                     "hack":    [snes_to_pc(0xA2A59E), snes_to_pc(0xA2A5BE)]},
    "glowSpritemapsInstructionList": {"vanilla": [snes_to_pc(0x8dca4e), snes_to_pc(0x8DCAAA)],
                                      "hack":    [snes_to_pc(0x8dca4e), snes_to_pc(0x8DCAAA)]},
    "spritemapsInstructionList": {"vanilla": [snes_to_pc(0xA2A5BE), snes_to_pc(0xA2A622)],
                                  "hack":    [snes_to_pc(0xA2A5BE), snes_to_pc(0xA2A622)]},
    "instructionList": {"vanilla": [snes_to_pc(0xA2A644), snes_to_pc(0xA2A783)],
                        "hack":    [snes_to_pc(0xA2A644), snes_to_pc(0xA2A783)]},
    "spritemaps": {"vanilla": [snes_to_pc(0xA2AD81), snes_to_pc(0xA2AFF3)],
                   "hack":    [snes_to_pc(0xA2AD81), snes_to_pc(0xA2AFF3)]},
    "enemyHeader": {"vanilla": [snes_to_pc(0xA0D07F), snes_to_pc(0xA0D0FF)],
                    "hack":    [snes_to_pc(0xA0D07F), snes_to_pc(0xA0D0FF)]},
    "enemySet": {"vanilla": [snes_to_pc(0xA1883D), snes_to_pc(0xA18870)],
                 "hack":    [snes_to_pc(0xA1883D), snes_to_pc(0xA18870)]},
    #"enemyGfxName": [snes_to_pc(0xB4818C), snes_to_pc(0xB48193)],
    "enemyGfx": {"vanilla": [snes_to_pc(0xB48193), snes_to_pc(0xB4819E)],
                 "hack":    [snes_to_pc(0xB48193), snes_to_pc(0xB4819E)]}
}

needCopy = {
    "tilesAddr": False,
    "palettesAddr": False,
    "glowSpritemapsInstructionList": False,
    "spritemapsInstructionList": False,
    "instructionList": False,
    "spritemaps": False,
    "enemyHeader": False,
    "enemySet": False,
    #"enemyGfxName": False,
    "enemyGfx": False
}

hackRom = RealROM(hack)
vanillaRom = RealROM(tmpfile)

# level data are compressed, extract tiles in ship screen based on spritemaps
landingSiteAddr = snes_to_pc(0x8F91F8)

vLandingSite = Room(vanillaRom, landingSiteAddr)
vLevelDataAddr = vLandingSite.defaultRoomState.levelDataPtr
vRoomScreenSize = (vLandingSite.width, vLandingSite.height)

hLandingSite = Room(hackRom, landingSiteAddr)
hLevelDataAddr = hLandingSite.defaultRoomState.levelDataPtr
hRoomScreenSize = (hLandingSite.width, hLandingSite.height)

print("hack landing site addr: {} size: {}".format(hex(hLevelDataAddr), hRoomScreenSize))
print("vanilla landing site addr: {} size: {}".format(hex(vLevelDataAddr), vRoomScreenSize))

vlevelData = LevelData(vanillaRom, snes_to_pc(vLevelDataAddr), vRoomScreenSize)
hlevelData = LevelData(hackRom, snes_to_pc(hLevelDataAddr), hRoomScreenSize)

vLandingSite.loadEnemies()
hLandingSite.loadEnemies()

# search for ship in loaded enemies
shipTopInitAi = 0xA644
shipBottomInitAi = 0xA6D2
vShips = {}
for enemy in vLandingSite.enemies:
    if enemy.initAi == shipTopInitAi:
        vShips["top"] = enemy
    elif enemy.initAi == shipBottomInitAi:
        vShips["bottom"] = enemy
if "top" not in vShips or "bottom" not in vShips:
    raise Exception("ship top/bottom not found in vanilla landing site enemies (using initAi)")

hShips = {}
for enemy in hLandingSite.enemies:
    if enemy.initAi == shipTopInitAi:
        hShips["top"] = enemy
    elif enemy.initAi == shipBottomInitAi:
        hShips["bottom"] = enemy
if "top" not in hShips or "bottom" not in hShips:
    raise Exception("ship top/bottom not found in hack landing site enemies (using initAi)")

#print("vanilla enemies: {}".format([hex(enemy) for enemy in vEnemies]))

# check if ship has relocated palette
vanillaPaletteAddr = 0xA59E
if hShips["top"].palette != vanillaPaletteAddr:
    addr = snes_to_pc(0xA20000+hShips["top"].palette)
    addresses["palettesAddr"]["hack"] = [addr, addr+32]
    print("ship top has relocated palette addr: {}".format(hex(addr)))
if hShips["bottom"].palette != vanillaPaletteAddr:
    addr = snes_to_pc(0xA20000+hShips["bottom"].palette)
    addresses["palettesAddr"]["hack"] = [addr, addr+32]
    print("ship bottom has relocated palette addr: {}".format(hex(addr)))

vShipScreen = (int(vShips["top"].Xpos/256), int(vShips["top"].Ypos/256))
hShipScreen = (int(hShips["top"].Xpos/256), int(hShips["top"].Ypos/256))

print("vShip screen: {}".format(vShipScreen))
print("hShip screen: {}".format(hShipScreen))

#print("vanilla screen")
#vlevelData.debug()
#vlevelData.displayScreen(vShipScreen)
#print("")
#
#print("hack screen")
#hlevelData.debug()
#hlevelData.displayScreen(hShipScreen)
#print("")

print("load vanilla ship top")
vShipTop = Ship("ship top", vanillaRom, vShips["top"], (0x80, 0x60))
print("load vanilla ship bottom")
vShipBottom = Ship("ship bottom", vanillaRom, vShips["bottom"], (0x80, 0x88))
print("")

#print("bts behind vanilla ship top")
#vlevelData.displaySubScreen(vShipScreen, vShipTop.spritemap.boundingRect)
#print("")
#
#print("bts behind vanilla ship bottom")
#vlevelData.displaySubScreen(vShipScreen, vShipBottom.spritemap.boundingRect)
#print("")

print("load hack ship")
# TODO::compute center from ??
hShipTop = Ship("ship top", hackRom, hShips["top"], (0x80, 0x60))
hShipBottom = Ship("ship bottom", hackRom, hShips["bottom"], (0x80, 0x88))
print("")

#print("bts behind hack ship top")
#hlevelData.displaySubScreen(hShipScreen, hShipTop.spritemap.boundingRect)
#print("")
#
#print("bts behind hack ship bottom")
#hlevelData.displaySubScreen(hShipScreen, hShipBottom.spritemap.boundingRect)
#print("")

# first empty behind vanilla ship in case hack sprite is smaller
vlevelData.emptyLayout(vShipScreen, vShipTop.spritemap.boundingRect)
vlevelData.emptyLayout(vShipScreen, vShipBottom.spritemap.boundingRect)

# copy level data behind ship
vlevelData.pasteLayout(hlevelData.copyLayout(hShipScreen, hShipTop.spritemap.boundingRect), vShipScreen, hShipTop.spritemap.boundingRect)
vlevelData.pasteLayout(hlevelData.copyLayout(hShipScreen, hShipBottom.spritemap.boundingRect), vShipScreen, hShipBottom.spritemap.boundingRect)

print("updated bts behind vanilla ship top")
vlevelData.displaySubScreen(vShipScreen, hShipTop.spritemap.boundingRect)
print("")

print("updated bts behind vanilla ship bottom")
vlevelData.displaySubScreen(vShipScreen, hShipBottom.spritemap.boundingRect)
print("")

if not fixEscape:
    vlevelData.write(5165)

for name, addrRange in addresses.items():
    print("check {} at {}".format(name, hex(addrRange["vanilla"][0])))
    diffFound = False
    for addrV, addrH in zip(range(addrRange["vanilla"][0], addrRange["vanilla"][1]), range(addrRange["hack"][0], addrRange["hack"][1])):
        hByte = hackRom.readByte(addrH)
        vByte = vanillaRom.readByte(addrV)
        if hByte != vByte:
            print("difference between vanilla and hack detected")
            diffFound = True
            break
    if name not in ["enemySet", "enemyHeader"]:
        needCopy[name] = diffFound
    if diffFound and addrRange["vanilla"][1] - addrRange["vanilla"][0] < 256:
        hBytes = []
        vBytes = []
        for addrV, addrH in zip(range(addrRange["vanilla"][0], addrRange["vanilla"][1]), range(addrRange["hack"][0], addrRange["hack"][1])):
            hBytes.append(hackRom.readByte(addrH))
            vBytes.append(vanillaRom.readByte(addrV))
        print("vanilla: {}".format([hex(b) for b in vBytes]))
        print("hack:    {}".format([hex(b) for b in hBytes]))

    print("end check {}".format(name))
    print("")

if not fixEscape:
    # copy data
    for name, diff in needCopy.items():
        if not diff:
            continue
        print("copy {} from hack".format(name))
        tmpBytes = []
        addrs = addresses[name]
        for addr in range(addrs["hack"][0], addrs["hack"][1]):
            tmpBytes.append(hackRom.readByte(addr))
        vanillaRom.seek(addrs["vanilla"][0])
        for byte in tmpBytes:
            vanillaRom.writeByte(byte)

# also copy last line of ship tiles in escape sequence
rowSize = 1024
hAddr = addresses["tilesAddr"]["hack"][0] + rowSize * 3
vAddr = snes_to_pc(0x94C800)
hackRom.seek(hAddr)
vanillaRom.seek(vAddr)
for i in range(rowSize):
    vanillaRom.writeByte(hackRom.readByte())

vanillaRom.close()

# generate ips between vanilla & tempfile
patch = IPS_Patch.create(open(vanilla, 'rb').read(), open(tmpfile, 'rb').read())
out = hack+'.ips'
patch.save(out)
print("ips generated: {}".format(out))

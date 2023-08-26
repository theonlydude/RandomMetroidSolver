from graph.vanilla.graph_access import accessPointsDict as vanillaAPDict
from logic.cache import Cache
from rom.rom_patches import RomPatches
from utils.parameters import Settings
import copy

accessPointsDict = copy.deepcopy(vanillaAPDict)

# can now ggg
accessPointsDict['Business Center'].connectInternal(
    'Grapple Escape',
    Cache.ldeco(lambda sm: sm.wand(
        sm.canGreenGateGlitch(),
        sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Bubble']))
    )
)
accessPointsDict['East Tunnel Top Right'].traverse = Cache.ldeco(lambda sm: sm.wor(
    RomPatches.has(RomPatches.AreaRandoGatesBase),
    sm.canGreenGateGlitch())
)
# can no longer bgg
accessPointsDict['Business Center'].connectInternal(
    'Crocomire Speedway Bottom',
    Cache.ldeco(lambda sm: sm.wor(
        # frog speedway
        sm.wand(sm.canPassFrogSpeedwayLeftToRight(),
                sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Norfair Entrance -> Croc via Frog w/Wave']),
                sm.haveItem('Wave')),
        # below ice
        sm.wand(sm.traverse('BusinessCenterTopLeft'),
                sm.haveItem('SpeedBooster'),
                sm.canUsePowerBombs(),
                sm.canHellRun(**Settings.hellRunsTable['Ice']['Norfair Entrance -> Croc via Ice'])))
    )
)
accessPointsDict['Kronic Boost Room Bottom Left'].connectInternal(
    'Crocomire Speedway Bottom',
    Cache.ldeco(lambda sm: sm.wand(
        sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
        sm.haveItem('Wave'))
    )
)
accessPointsDict['Bubble Mountain Bottom'].connectInternal(
    'Crocomire Speedway Bottom',
    Cache.ldeco(lambda sm: sm.wand(
        sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Croc']),
        sm.haveItem('Wave'))
    )
)
accessPointsDict['Noob Bridge Right'].connectInternal(
    'Green Hill Zone Top Right',
    Cache.ldeco(lambda sm: sm.wor(sm.haveItem('Wave'),
                                  RomPatches.has(RomPatches.GreenHillsGateRemoved))
    )
)
# can no longer ggg
accessPointsDict['LN Entrance'].disconnectInternal('Screw Attack Bottom')
accessPointsDict['Firefleas'].disconnectInternal('Screw Attack Bottom')
accessPointsDict['Crab Hole Bottom Left'].connectInternal(
    'Main Street Bottom',
    Cache.ldeco(lambda sm: sm.wand(
        sm.canExitCrabHole(),
        RomPatches.has(RomPatches.GreenHillsGateRemoved))
    )
)
accessPointsDict['West Sand Hall Left'].connectInternal(
    'Main Street Bottom',
    Cache.ldeco(lambda sm: sm.wand(
        sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
        RomPatches.has(RomPatches.AreaRandoGatesOther))
    )
)

# directions:
# no door closes behind Samus:
#    00 = right, 01 = left, 02 = down, 03 = up.
# door closes behind Samus:
#    04 = right, 05 = left, 06 = down, 07 = up.

# exit infos (from tools/gen_ap_exit.py)
accessPointsDict['Lower Mushrooms Left'].ExitInfo.update({
    'DoorPtr': 0x8C22,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Green Pirates Shaft Bottom Right'].ExitInfo.update({
    'DoorPtr': 0x8C52,
    'direction': 0x05,
    'cap': (0x4E, 0x06),
    'bitFlag': 0x00,
    'screen': (0x04, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Moat Right'].ExitInfo.update({
    'DoorPtr': 0x8AEA,
    'direction': 0x05,
    'cap': (0x7E, 0x46),
    'bitFlag': 0x00,
    'screen': (0x07, 0x04),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Keyhunter Room Bottom'].ExitInfo.update({
    'DoorPtr': 0x8A42,
    'direction': 0x06,
    'cap': (0x06, 0x02),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Morph Ball Room Left'].ExitInfo.update({
    'DoorPtr': 0x8E9E,
    'direction': 0x04,
    'cap': (0x61, 0x06),
    'bitFlag': 0x00,
    'screen': (0x06, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Climb Bottom Left'].ExitInfo.update({
    'DoorPtr': 0x8B6E,
    'direction': 0x04,
    'cap': (0x01, 0x16),
    'bitFlag': 0x00,
    'screen': (0x00, 0x01),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Flyway Right'].ExitInfo.update({
    'DoorPtr': 0x8BC2,
    'direction': 0x05,
    'cap': (0x0E, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Bomb Torizo Room Left'].ExitInfo.update({
    'DoorPtr': 0x8BAA,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Green Brinstar Elevator'].ExitInfo.update({
    'DoorPtr': 0x8BFE,
    'direction': 0x05,
    'cap': (0x3E, 0x06),
    'bitFlag': 0x00,
    'screen': (0x03, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Green Hill Zone Top Right'].ExitInfo.update({
    'DoorPtr': 0x8E86,
    'direction': 0x05,
    'cap': (0x7E, 0x26),
    'bitFlag': 0x00,
    'screen': (0x07, 0x02),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Noob Bridge Right'].ExitInfo.update({
    'DoorPtr': 0x8F0A,
    'direction': 0x05,
    'cap': (0x0E, 0x46),
    'bitFlag': 0x00,
    'screen': (0x00, 0x04),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Green Brinstar Main Shaft Top Left'].ExitInfo.update({
    'DoorPtr': 0x8CB2,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Brinstar Pre-Map Room Right'].ExitInfo.update({
    'DoorPtr': 0x8D42,
    'direction': 0x05,
    'cap': (0x3E, 0x46),
    'bitFlag': 0x00,
    'screen': (0x03, 0x04),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['West Ocean Left'].ExitInfo.update({
    'DoorPtr': 0x89CA,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Crab Maze Left'].ExitInfo.update({
    'DoorPtr': 0x8AAE,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['PhantoonRoomOut'].ExitInfo.update({
    'DoorPtr': 0xA2AC,
    'direction': 0x05,
    'cap': (0x0E, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['PhantoonRoomIn'].ExitInfo.update({
    'DoorPtr': 0xA2C4,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': "bank_8f_PhantoonRoomOut_DoorAsmPtr"
})
accessPointsDict['Basement Left'].ExitInfo.update({
    'DoorPtr': 0xA2A0,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Wrecked Ship Map Room'].ExitInfo.update({
    'DoorPtr': 0xA2B8,
    'direction': 0x05,
    'cap': (0x4E, 0x06),
    'bitFlag': 0x00,
    'screen': (0x04, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Lava Dive Right'].ExitInfo.update({
    'DoorPtr': 0x96D2,
    'direction': 0x05,
    'cap': (0x0E, 0x26),
    'bitFlag': 0x00,
    'screen': (0x00, 0x02),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Three Muskateers Room Left'].ExitInfo.update({
    'DoorPtr': 0x9A4A,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['RidleyRoomOut'].ExitInfo.update({
    'DoorPtr': 0x98CA,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['RidleyRoomIn'].ExitInfo.update({
    'DoorPtr': 0x98BE,
    'direction': 0x05,
    'cap': (0x2E, 0x06),
    'bitFlag': 0x00,
    'screen': (0x02, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Warehouse Zeela Room Left'].ExitInfo.update({
    'DoorPtr': 0x913E,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['KraidRoomOut'].ExitInfo.update({
    'DoorPtr': 0x91B6,
    'direction': 0x05,
    'cap': (0x1E, 0x16),
    'bitFlag': 0x00,
    'screen': (0x01, 0x01),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['KraidRoomIn'].ExitInfo.update({
    'DoorPtr': 0x91CE,
    'direction': 0x04,
    'cap': (0x01, 0x16),
    'bitFlag': 0x00,
    'screen': (0x00, 0x01),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Warehouse Entrance Left'].ExitInfo.update({
    'DoorPtr': 0x922E,
    'direction': 0x04,
    'cap': (0x31, 0x16),
    'bitFlag': 0x40,
    'screen': (0x03, 0x01),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0xBDD1
})
accessPointsDict['Warehouse Entrance Right'].ExitInfo.update({
    'DoorPtr': 0x923A,
    'direction': 0x05,
    'cap': (0x1E, 0x06),
    'bitFlag': 0x00,
    'screen': (0x01, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Single Chamber Top Right'].ExitInfo.update({
    'DoorPtr': 0x95FA,
    'direction': 0x05,
    'cap': (0x2E, 0x06),
    'bitFlag': 0x00,
    'screen': (0x02, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Kronic Boost Room Bottom Left'].ExitInfo.update({
    'DoorPtr': 0x967E,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Crocomire Speedway Bottom'].ExitInfo.update({
    'DoorPtr': 0x93D2,
    'direction': 0x06,
    'cap': (0x36, 0x02),
    'bitFlag': 0x00,
    'screen': (0x04, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Business Center Mid Left'].ExitInfo.update({
    'DoorPtr': 0x9306,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Norfair Map Room'].ExitInfo.update({
    'DoorPtr': 0x97C2,
    'direction': 0x05,
    'cap': (0x0E, 0x46),
    'bitFlag': 0x00,
    'screen': (0x00, 0x04),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Crocomire Room Top'].ExitInfo.update({
    'DoorPtr': 0x93EA,
    'direction': 0x07,
    'cap': (0x06, 0x2D),
    'bitFlag': 0x00,
    'screen': (0x00, 0x02),
    'distanceToSpawn': 0x01C0,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Main Street Bottom'].ExitInfo.update({
    'DoorPtr': 0xA39C,
    'direction': 0x06,
    'cap': (0x06, 0x02),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x0170,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Crab Hole Bottom Left'].ExitInfo.update({
    'DoorPtr': 0xA510,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Red Fish Room Left'].ExitInfo.update({
    'DoorPtr': 0xA480,
    'direction': 0x04,
    'cap': (0x01, 0x36),
    'bitFlag': 0x40,
    'screen': (0x00, 0x03),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Crab Shaft Right'].ExitInfo.update({
    'DoorPtr': 0xA4C8,
    'direction': 0x05,
    'cap': (0x5E, 0x16),
    'bitFlag': 0x00,
    'screen': (0x05, 0x01),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Crab Hole Bottom Right'].ExitInfo.update({
    'DoorPtr': 0xA51C,
    'direction': 0x05,
    'cap': (0x0E, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Maridia Map Room'].ExitInfo.update({
    'DoorPtr': 0xA5E8,
    'direction': 0x04,
    'cap': (0x01, 0x16),
    'bitFlag': 0x00,
    'screen': (0x00, 0x01),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0xE356
})
accessPointsDict['Aqueduct Top Left'].ExitInfo.update({
    'DoorPtr': 0xA708,
    'direction': 0x04,
    'cap': (0x01, 0x36),
    'bitFlag': 0x00,
    'screen': (0x00, 0x03),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0xE398
})
accessPointsDict['Le Coude Right'].ExitInfo.update({
    'DoorPtr': 0x8AA2,
    'direction': 0x05,
    'cap': (0x3E, 0x16),
    'bitFlag': 0x00,
    'screen': (0x03, 0x01),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['DraygonRoomOut'].ExitInfo.update({
    'DoorPtr': 0xA840,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['DraygonRoomIn'].ExitInfo.update({
    'DoorPtr': 0xA96C,
    'direction': 0x05,
    'cap': (0x1E, 0x26),
    'bitFlag': 0x00,
    'screen': (0x01, 0x02),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Red Tower Top Left'].ExitInfo.update({
    'DoorPtr': 0x902A,
    'direction': 0x04,
    'cap': (0x01, 0x06),
    'bitFlag': 0x00,
    'screen': (0x00, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Caterpillar Room Top Right'].ExitInfo.update({
    'DoorPtr': 0x90C6,
    'direction': 0x05,
    'cap': (0x2E, 0x06),
    'bitFlag': 0x40,
    'screen': (0x02, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0xBDAF
})
accessPointsDict['Red Brinstar Elevator'].ExitInfo.update({
    'DoorPtr': 0x8AF6,
    'direction': 0x07,
    'cap': (0x16, 0x2D),
    'bitFlag': 0x00,
    'screen': (0x01, 0x02),
    'distanceToSpawn': 0x01C0,
    'doorAsmPtr': 0xB9F1
})
accessPointsDict['East Tunnel Right'].ExitInfo.update({
    'DoorPtr': 0xA384,
    'direction': 0x05,
    'cap': (0x2E, 0x06),
    'bitFlag': 0x40,
    'screen': (0x02, 0x00),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['East Tunnel Top Right'].ExitInfo.update({
    'DoorPtr': 0xA390,
    'direction': 0x05,
    'cap': (0x0E, 0x16),
    'bitFlag': 0x00,
    'screen': (0x00, 0x01),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0xE356
})
accessPointsDict['Glass Tunnel Top'].ExitInfo.update({
    'DoorPtr': 0xA330,
    'direction': 0x07,
    'cap': (0x16, 0x7D),
    'bitFlag': 0x00,
    'screen': (0x01, 0x07),
    'distanceToSpawn': 0x0200,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Golden Four'].ExitInfo.update({
    'DoorPtr': 0x91E6,
    'direction': 0x04,
    'cap': (0x01, 0x66),
    'bitFlag': 0x00,
    'screen': (0x00, 0x06),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})
accessPointsDict['Tourian Escape Room 4 Top Right'].ExitInfo.update({
    'DoorPtr': 0xAB34,
    'direction': 0x05,
    'cap': (0x2E, 0x86),
    'bitFlag': 0x40,
    'screen': (0x02, 0x08),
    'distanceToSpawn': 0x8000,
    'doorAsmPtr': 0x0000
})


accessPointsDict['Lower Mushrooms Left'].EntryInfo.update({
    'SamusX': 0x3c9,
    'SamusY': 0x88
})
accessPointsDict['Green Pirates Shaft Bottom Right'].EntryInfo.update({
    'SamusX': 0x33,
    'SamusY': 0x688
})
accessPointsDict['Moat Right'].EntryInfo.update({
    'SamusX': 0x30,
    'SamusY': 0x88
})
accessPointsDict['Keyhunter Room Bottom'].EntryInfo.update({
    'SamusX': 0x1b3,
    'SamusY': 0x2b8
})
accessPointsDict['Morph Ball Room Left'].EntryInfo.update({
    'SamusX': 0x7cb,
    'SamusY': 0x288
})
accessPointsDict['Climb Bottom Left'].EntryInfo.update({
    'SamusX': 0x2d3,
    'SamusY': 0x888
})
accessPointsDict['Flyway Right'].EntryInfo.update({
    'SamusX': 0xffff,
    'SamusY': 0xffff
})
accessPointsDict['Bomb Torizo Room Left'].EntryInfo.update({
    'SamusX': 0xcb,
    'SamusY': 0xb8
})
accessPointsDict['Green Brinstar Elevator'].EntryInfo.update({
    'SamusX': 0x33,
    'SamusY': 0x88
})
accessPointsDict['Green Hill Zone Top Right'].EntryInfo.update({
    'SamusX': 0x638,
    'SamusY': 0x88
})
accessPointsDict['Noob Bridge Right'].EntryInfo.update({
    'SamusX': 0x31,
    'SamusY': 0x88
})
accessPointsDict['Green Brinstar Main Shaft Top Left'].EntryInfo.update({
    'SamusX': 0x3cb,
    'SamusY': 0x488
})
accessPointsDict['Brinstar Pre-Map Room Right'].EntryInfo.update({
    'SamusX': 0xffff,
    'SamusY': 0xffff
})
accessPointsDict['West Ocean Left'].EntryInfo.update({
    'SamusX': 0x7cb,
    'SamusY': 0x488
})
accessPointsDict['Crab Maze Left'].EntryInfo.update({
    'SamusX': 0x3cb,
    'SamusY': 0x188
})
accessPointsDict['PhantoonRoomOut'].EntryInfo.update({
    'SamusX': 0x60,
    'SamusY': 0xb8
})
accessPointsDict['PhantoonRoomIn'].EntryInfo.update({
    'SamusX': 0xd1,
    'SamusY': 0xb8
})
accessPointsDict['Basement Left'].EntryInfo.update({
    'SamusX': 0x4d1,
    'SamusY': 0x88
})
accessPointsDict['Wrecked Ship Map Room'].EntryInfo.update({
    'SamusX': 0xffff,
    'SamusY': 0xffff
})
accessPointsDict['Lava Dive Right'].EntryInfo.update({
    'SamusX': 0x2f,
    'SamusY': 0x88
})
accessPointsDict['Three Muskateers Room Left'].EntryInfo.update({
    'SamusX': 0x2cb,
    'SamusY': 0x88
})
accessPointsDict['RidleyRoomOut'].EntryInfo.update({
    'SamusX': 0x2d1,
    'SamusY': 0x98
})
accessPointsDict['RidleyRoomIn'].EntryInfo.update({
    'SamusX': 0x50,
    'SamusY': 0x198
})
accessPointsDict['Warehouse Zeela Room Left'].EntryInfo.update({
    'SamusX': 0x1cb,
    'SamusY': 0x88
})
accessPointsDict['KraidRoomOut'].EntryInfo.update({
    'SamusX': 0x32,
    'SamusY': 0x188
})
accessPointsDict['KraidRoomIn'].EntryInfo.update({
    'SamusX': 0x1cb,
    'SamusY': 0x188
})
accessPointsDict['Warehouse Entrance Left'].EntryInfo.update({
    'SamusX': 0x2cb,
    'SamusY': 0x88
})
accessPointsDict['Warehouse Entrance Right'].EntryInfo.update({
    # spawns Samus closer to the door to activate the scroll PLM
    'SamusX': 0x2e,
    'SamusY': 0x98
})
accessPointsDict['Single Chamber Top Right'].EntryInfo.update({
    'SamusX': 0x30,
    'SamusY': 0x88
})
accessPointsDict['Kronic Boost Room Bottom Left'].EntryInfo.update({
    'SamusX': 0xcb,
    'SamusY': 0x288
})
accessPointsDict['Crocomire Speedway Bottom'].EntryInfo.update({
    'SamusX': 0xa8,
    'SamusY': 0x2b8
})
accessPointsDict['Business Center Mid Left'].EntryInfo.update({
    'SamusX': 0xcb,
    'SamusY': 0x488
})
accessPointsDict['Norfair Map Room'].EntryInfo.update({
    'SamusX': 0xffff,
    'SamusY': 0xffff
})
accessPointsDict['Crocomire Room Top'].EntryInfo.update({
    'SamusX': 0x47d,
    'SamusY': 0x98
})
accessPointsDict['Main Street Bottom'].EntryInfo.update({
    'SamusX': 0x1b5,
    'SamusY': 0x7a8
})
accessPointsDict['Crab Hole Bottom Left'].EntryInfo.update({
    'SamusX': 0xd7,
    'SamusY': 0x188
})
accessPointsDict['Red Fish Room Left'].EntryInfo.update({
    'SamusX': 0x2cb,
    'SamusY': 0x88
})
accessPointsDict['Crab Shaft Right'].EntryInfo.update({
    'SamusX': 0x2a,
    'SamusY': 0x388
})
accessPointsDict['Crab Hole Bottom Right'].EntryInfo.update({
    'SamusX': 0x28,
    'SamusY': 0x188
})
accessPointsDict['Maridia Map Room'].EntryInfo.update({
    'SamusX': 0xffff,
    'SamusY': 0xffff
})
accessPointsDict['Aqueduct Top Left'].EntryInfo.update({
    'SamusX': 0x5cb,
    'SamusY': 0x188
})
accessPointsDict['Le Coude Right'].EntryInfo.update({
    'SamusX': 0x2e,
    'SamusY': 0x88
})
accessPointsDict['DraygonRoomOut'].EntryInfo.update({
    'SamusX': 0x1d1,
    'SamusY': 0x288
})
accessPointsDict['DraygonRoomIn'].EntryInfo.update({
    'SamusX': 0x37,
    'SamusY': 0x88
})
accessPointsDict['Red Tower Top Left'].EntryInfo.update({
    'SamusX': 0xd0,
    'SamusY': 0x488
})
accessPointsDict['Caterpillar Room Top Right'].EntryInfo.update({
    'SamusX': 0x2e,
    'SamusY': 0x388
})
accessPointsDict['Red Brinstar Elevator'].EntryInfo.update({
    'SamusX': 0x7f,
    'SamusY': 0x58
})
accessPointsDict['East Tunnel Right'].EntryInfo.update({
    'SamusX': 0x331,
    'SamusY': 0x188
})
accessPointsDict['East Tunnel Top Right'].EntryInfo.update({
    'SamusX': 0x39,
    'SamusY': 0x88
})
accessPointsDict['Glass Tunnel Top'].EntryInfo.update({
    'SamusX': 0x7e,
    'SamusY': 0x78
})
accessPointsDict['Golden Four'].EntryInfo.update({
    'SamusX': 0x4cb,
    'SamusY': 0x88
})
accessPointsDict['Tourian Escape Room 4 Top Right'].EntryInfo.update({
    'SamusX': 0xffff,
    'SamusY': 0xffff
})

accessPoints = [ap for ap in accessPointsDict.values()]


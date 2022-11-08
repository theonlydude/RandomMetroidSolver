from graph.vanilla.graph_access import accessPointsDict
from logic.cache import Cache
from rom.rom_patches import RomPatches
from utils.parameters import Settings

# can now ggg
accessPointsDict['Business Center'].connectInternal(
    'Grapple Escape',
    Cache.ldeco(lambda sm: sm.wor(
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
        sm.wand(sm.haveItem('SpeedBooster'),
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
                                  RomPatches.has(RomPatches.AreaRandoGatesOther))
    )
)
# can no longer ggg
accessPointsDict['LN Entrance'].disconnectInternal('Screw Attack Bottom')
accessPointsDict['Firefleas'].disconnectInternal('Screw Attack Bottom')
accessPointsDict['Crab Hole Bottom Left'].connectInternal(
    'Main Street Bottom',
    Cache.ldeco(lambda sm: sm.wand(
        sm.canExitCrabHole(),
        RomPatches.has(RomPatches.AreaRandoGatesOther))
    )
)
accessPointsDict['West Sand Hall Left'].connectInternal(
    'Main Street Bottom',
    Cache.ldeco(lambda sm: sm.wand(
        sm.wnot(RomPatches.has(RomPatches.MaridiaSandWarp)),
        RomPatches.has(RomPatches.AreaRandoGatesOther))
    )
)

accessPoints = [ap for ap in accessPointsDict.values()]

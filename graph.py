#!/usr/bin/python

from parameters import Knows
from rom import RomPatches
from smbool import SMBool

class AccessPoint(object):
    # name : AccessPoint name
    # graphArea : graph area the node is located in
    # transitions : intra-area transitions
    # traverse: traverse function, will be wand to the added transitions
    # exitInfo : dict carrying vanilla door information. 'RoomPtr': Room address, 'DoorPtr': door address
    # entryInfo : dict carrying forced samus X/Y position with keys 'SamusX' and 'SamusY'.
    #             (to be updated after reading vanillaTransitions and gather entry info from matching exit door)
    # shortName : short name for the credits
    def __init__(self, name, graphArea, transitions, traverse=lambda sm: sm.setSMBool(True), exitInfo=None, entryInfo=None, shortName=None):
        self.Name = name
        self.GraphArea = graphArea
        self.ExitInfo = exitInfo
        self.EntryInfo = entryInfo
        self.transitions = transitions
        self.traverse = traverse
        if shortName is not None:
            self.ShortName = shortName
        else:
            self.ShortName = str(self)

    def __str__(self):
        return "[" + self.GraphArea + "] " + self.Name

    # for additions after construction (inter-area transitions)
    def addTransition(self, destName):
        self.transitions[destName] = lambda sm: self.traverse(sm)


class AccessGraph(object):
    def __init__(self, transitions, bidir=True, dotFile=None):
        self.accessPoints = {}
        self.InterAreaTransitions = []
        for ap in accessPoints:
            self.accessPoints[ap.Name] = ap
        for srcName, dstName in transitions:
            self.addTransition(srcName, dstName, bidir)
        if dotFile is not None:
            self.toDot(dotFile)

    def getCreditsLines(self):
        # TODO arrange transitions shortnames to have the least amount of lines to represent them
        pass

    def toDot(self, dotFile):
        with open(dotFile, "w") as f:
            f.write("digraph {\n")
            for name,ap in self.accessPoints.iteritems():
                for t in ap.transitions:
                    f.write('"' + str(ap) + '" -> "' + str(self.accessPoints[t]) + '"\n')
            f.write("}\n")

    def addTransition(self, srcName, dstName, both=True):
        src = self.accessPoints[srcName]
        dst = self.accessPoints[dstName]
        src.addTransition(dstName)
        self.InterAreaTransitions.append((src, dst))
        if both is True:
            self.addTransition(dstName, srcName, False)

    # availNodes: all already available nodes
    # nodesToCheck: nodes we have to check transitions for
    # items: collected items
    # maxDiff: difficulty limit
    # return newly opened access points
    def getNewAvailNodes(self, availNodes, nodesToCheck, smbm, maxDiff):
        newAvailNodes = {}
        for node in nodesToCheck:
            for dstName, tFunc in node.transitions.iteritems():
                dst = self.accessPoints[dstName]
                if dst in newAvailNodes or dst in availNodes:
                    continue
                # diff = tFunc(smbm)
                diff = smbm.eval(tFunc)
                if diff.bool == True and diff.difficulty <= maxDiff:
                    newAvailNodes[dst] = diff.difficulty
        return newAvailNodes

    # rootNode: starting AccessPoint instance
    # items: collected items
    # maxDiff: difficulty limit
    # return available AccessPoint list
    def getAvailableAccessPoints(self, rootNode, smbm, maxDiff):
        availNodes = { rootNode : 0 }
        newAvailNodes = availNodes
        while len(newAvailNodes) > 0:
            newAvailNodes = self.getNewAvailNodes(availNodes, newAvailNodes, smbm, maxDiff)
            availNodes.update(newAvailNodes)
        return availNodes

    # locations: locations to check
    # items: collected items
    # maxDiff: difficulty limit
    # rootNode: starting AccessPoint
    # return available locations list, also stores difficulty in locations
    def getAvailableLocations(self, locations, smbm, maxDiff, rootNode='Landing Site'):
        availAcessPoints = self.getAvailableAccessPoints(self.accessPoints[rootNode], smbm, maxDiff)
        availAreas = set([ap.GraphArea for ap in availAcessPoints.keys()])
        availLocs = []
        for loc in locations:
            if not loc['GraphArea'] in availAreas:
                continue
            for apName,tFunc in loc['AccessFrom'].iteritems():
                ap = self.accessPoints[apName]
                if not ap in availAcessPoints:
                    continue
                apDiff = availAcessPoints[ap]
                tdiff = smbm.eval(tFunc)
                if tdiff.bool == True and tdiff.difficulty <= maxDiff:
                    diff = smbm.eval(loc['Available'])
                    loc['difficulty'] = SMBool(diff.bool, max(tdiff.difficulty, diff.difficulty, apDiff))
                    if diff.bool == True and diff.difficulty <= maxDiff:
                        availLocs.append(loc)
                        break
                else:
                    loc['difficulty'] = tdiff
            if not 'difficulty' in loc:
                loc['difficulty'] = SMBool(False, 0)
        return availLocs
    

# all access points and traverse functions
accessPoints = [
    # Crateria and Blue Brinstar
    AccessPoint('Landing Site', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: sm.canPassTerminatorBombWall(),
        'Keyhunter Room Bottom': lambda sm: sm.canOpenGreenDoors(),
        'Morph Ball Room Left': lambda sm: sm.canUsePowerBombs()
    }, shortName="C\\Landing"),
    AccessPoint('Lower Mushrooms Left', 'Crateria', {
        'Landing Site': lambda sm: sm.canPassTerminatorBombWall(False)
    }, exitInfo = {'RoomPtr':0x79969, 'DoorPtr':0x8c22, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x0},
                entryInfo = {'SamusX':0x36, 'SamusY':0x88}, shortName="C\\Mushrooms"),
    AccessPoint('Moat Right', 'Crateria', {
        'Keyhunter Room Bottom': lambda sm: sm.canPassMoatReverse()
    }, exitInfo = {'RoomPtr':0x795ff, 'DoorPtr':0x8aea, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x0},
                entryInfo = {'SamusX':0x1cf, 'SamusY':0x88}, shortName="C\\Moat"),
    AccessPoint('Keyhunter Room Bottom', 'Crateria', {
        'Moat Right': lambda sm: sm.wand(sm.canOpenYellowDoors(),
                                         sm.canPassMoat()),
        'Landing Site': lambda sm: sm.setSMBool(True)
    }, lambda sm: sm.canOpenYellowDoors(),
                exitInfo = {'RoomPtr':0x7948c, 'DoorPtr':0x8a42, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                            "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x0},
                entryInfo = {'SamusX':0x14c, 'SamusY':0x2b8}, shortName="C\\Keyhunters"),
    AccessPoint('Morph Ball Room Left', 'Crateria', {
        'Landing Site': lambda sm: sm.canUsePowerBombs()
    }, exitInfo = {'RoomPtr':0x799e9f, 'DoorPtr':0x8e9e, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x1},
                entryInfo = {'SamusX':0x34, 'SamusY':0x279}, shortName="C\\Morph"),
    # Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                                               sm.canDestroyBombWalls()), # pink
                                                        sm.haveItem('Morph'), # big pink
                                                        sm.canOpenGreenDoors()) # also implies first red door
    }, exitInfo = {'RoomPtr':0x79938, 'DoorPtr':0x8bfe, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x0},
                entryInfo = {'SamusX':0xcc, 'SamusY':0x88}, shortName="B\\Green Elev."),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', {
        'Noob Bridge Right': lambda sm: sm.setSMBool(True),
        'Green Brinstar Elevator Right': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                                                   sm.canDestroyBombWalls()), # pink
                                                            sm.haveItem('Morph')) # big pink
    }, lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
                exitInfo = {'RoomPtr':0x79e52, 'DoorPtr':0x8e86, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                            "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x1},
                entryInfo = {'SamusX':0x1c7, 'SamusY':0x88},  shortName="B\\Green Hill"),
    AccessPoint('Noob Bridge Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wor(sm.haveItem('Wave'),
                                                       sm.wand(sm.canOpenRedDoors(), # can do the glitch with either missile or supers
                                                               sm.knowsGreenGateGlitch()))
    }, lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenGreenDoors()),
                exitInfo = {'RoomPtr':0x79fba, 'DoorPtr':0x8f0a, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                            "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x1},
                entryInfo = {'SamusX':0x5ce, 'SamusY':0x88}, shortName="B\\Noob Bridge"),
    # Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', {
        'Crab Maze Left': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                             sm.canPassSpongeBath(), # implies dead phantoon and pass bomb passages
                                             sm.canPassForgottenHighway(True))
    }, exitInfo = {'RoomPtr':0x793fe, 'DoorPtr':0x89ca, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x0},
                entryInfo = {'SamusX':0x34, 'SamusY':0x488}, shortName="W\\West Ocean"),
    AccessPoint('Crab Maze Left', 'WreckedShip', {
        'West Ocean Left': lambda sm: sm.canPassForgottenHighway(False)
    }, exitInfo = {'RoomPtr':0x7957d, 'DoorPtr':0x8aae, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x0},
                entryInfo = {'SamusX':0x34, 'SamusY':0x188}, shortName="W\\Crab Maze"),
    # Lower Norfair
    AccessPoint('Lava Dive Right', 'LowerNorfair', {
        'Three Muskateers Room Left': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'),
                                                         sm.canPassLavaPit(),
                                                         sm.canPassWorstRoom())
    }, exitInfo = {'RoomPtr':0x7af14, 'DoorPtr':0x96d2, 'direction': 0x4, "cap": (0x11, 0x26), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x2},
                entryInfo = {'SamusX':0x3d0, 'SamusY':0x88}, shortName="LN\\Lava Dive"),
    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', {
        'Lava Dive Right': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'),
                                              sm.canPassAmphitheaterReverse()) # if this is OK, reverse lava pit will be too...
    }, exitInfo = {'RoomPtr':0x7b656, 'DoorPtr':0x9a4a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x2},
                entryInfo = {'SamusX':0x134, 'SamusY':0x88}, shortName="LN\\Three Musk."),
    # Norfair
    AccessPoint('Warehouse Entrance Left', 'Norfair', {
        'Single Chamber Top Right': lambda sm: sm.canAccessHeatedNorfairFromEntrance(),
        'Kronic Boost Room Bottom Left': lambda sm: sm.canAccessHeatedNorfairFromEntrance()
    }, exitInfo = {'RoomPtr':0x7a6a1, 'DoorPtr':0x922e, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x40,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdd1, "area": 0x1},
                entryInfo = {'SamusX':0x34, 'SamusY':0x88}, shortName="N\\Warehouse"),
    AccessPoint('Single Chamber Top Right', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                      sm.haveItem('Morph'),
                                                      sm.canHellRun('MainUpperNorfair')),
        'Kronic Boost Room Bottom Left': lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                            sm.haveItem('Morph'),
                                                            sm.canHellRun('MainUpperNorfair'))
    }, lambda sm: sm.wand(sm.canDestroyBombWalls(),
                          sm.haveItem('Morph'),
                          RomPatches.has(RomPatches.SingleChamberNoCrumble)),
                exitInfo = {'RoomPtr':0x7ad5e, 'DoorPtr':0x95fa, 'direction': 0x4, "cap": (0x11, 0x6), "bitFlag": 0x0,
                            "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x2},
                entryInfo = {'SamusX':0x5cf, 'SamusY':0x88}, shortName="N\\Single Chamber"),
    AccessPoint('Kronic Boost Room Bottom Left', 'Norfair', {
        'Single Chamber Top Right': lambda sm: sm.canHellRun('MainUpperNorfair'),
        'Warehouse Entrance Left': lambda sm: sm.canHellRun('MainUpperNorfair')
    }, lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
                exitInfo = {'RoomPtr':0x7ae74, 'DoorPtr':0x968a, 'direction': 0x5, "cap": (0x3e, 0x6), "bitFlag": 0x0,
                            "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x2},
                entryInfo = {'SamusX':0x134, 'SamusY':0x288}, shortName="N\\Kronic Boost"),
    # Maridia
    AccessPoint('Main Street Bottom', 'Maridia', {
        'Red Fish Room Left': lambda sm: sm.canGoUpMtEverest(),
        'Crab Hole Bottom Left': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                    sm.canOpenGreenDoors()), # red door+green gate
        'Le Coude Right': lambda sm: sm.wand(sm.canOpenGreenDoors(), # gate+door
                                             sm.wor(sm.haveItem('Gravity'),
                                                    sm.wand(sm.knowsGravLessLevel3(),
                                                            sm.haveItem('HiJump')))) # for the sand pits
    }, exitInfo = {'RoomPtr':0x7cfc9, 'DoorPtr':0xa39c, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x170, "doorAsmPtr": 0x0000, "area": 0x4},
                entryInfo = {'SamusX':0x14a, 'SamusY':0x7a8}, shortName="M\\Main Street"),
    AccessPoint('Crab Hole Bottom Left', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.wand(sm.canExitCrabHole(),
                                                 sm.wand(sm.haveItem('Super'),
                                                         sm.knowsGreenGateGlitch())),
        'Le Coude Right': lambda sm: sm.wand(sm.canExitCrabHole(),
                                             sm.canOpenGreenDoors(), # toilet door
                                             sm.wor(sm.haveItem('Gravity'),
                                                    sm.wand(sm.knowsGravLessLevel3(),
                                                            sm.haveItem('HiJump')))) # for the sand pits
    }, lambda sm: sm.haveItem('Morph'), exitInfo = {'RoomPtr':0x7d21c, 'DoorPtr':0xa510, 'direction': 0x5,
                                                    "cap": (0x3e, 0x6), "screen": (0x3, 0x0), "bitFlag": 0x0,
                                                    "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x4},
                entryInfo = {'SamusX':0x28, 'SamusY':0x188}, shortName="M\\Crab Hole"),
    AccessPoint('Le Coude Right', 'Maridia', {
        'Crab Hole Bottom Left': lambda sm: sm.wand(sm.canOpenYellowDoors(),
                                                    sm.wor(sm.haveItem('Gravity'),
                                                           sm.wand(sm.knowsGravLessLevel3(),
                                                                   sm.haveItem('HiJump'))), # for the sand pits
                                                    sm.canOpenGreenDoors()), # toilet door
        'Main Street Bottom': lambda sm: sm.wand(sm.canOpenYellowDoors(),
                                                 sm.wand(sm.wor(sm.haveItem('Gravity'),
                                                                sm.wand(sm.knowsGravLessLevel3(),
                                                                        sm.haveItem('HiJump'))), # for the sand pits
                                                         sm.canOpenGreenDoors(), # toilet door
                                                         sm.knowsGreenGateGlitch())),
    }, exitInfo = {'RoomPtr':0x795a8, 'DoorPtr':0x8aa2, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x0},
                entryInfo = {'SamusX':0xd1, 'SamusY':0x88}, shortName="M\\Coude"),
    AccessPoint('Red Fish Room Left', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.haveItem('Morph') # just go down
    }, lambda sm: sm.haveItem('Morph'),
                exitInfo = {'RoomPtr':0x7d104, 'DoorPtr':0xa480, 'direction': 0x5, "cap": (0x2e, 0x36), "bitFlag": 0x40,
                            "screen": (0x2, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe367, "area": 0x4},
                entryInfo = {'SamusX':0x34, 'SamusY':0x88}, shortName="M\\Red Fish"),
    # Red Brinstar. Main nodes: Red Tower Top Left, East Tunnel Right
    AccessPoint('Red Tower Top Left', 'RedBrinstar', {
        # go up
        'Red Brinstar Elevator': lambda sm: sm.wand(sm.canClimbRedTower(),
                                                    sm.wor(sm.canOpenYellowDoors(),
                                                           RomPatches.has(RomPatches.RedTowerBlueDoors))),
        'Caterpillar Room Top Right': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                         RomPatches.has(RomPatches.NoMaridiaGreenGates),
                                                         sm.canClimbRedTower()),
        # go down
        'East Tunnel Right': lambda sm: sm.setSMBool(True)
    }, exitInfo = {'RoomPtr':0x7a253, 'DoorPtr':0x902a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x1},
                entryInfo = {'SamusX':0x2f, 'SamusY':0x488}, shortName="B\\Red Tower"),
    AccessPoint('Caterpillar Room Top Right', 'RedBrinstar', {
        'Red Brinstar Elevator': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                    sm.wor(RomPatches.has(RomPatches.NoMaridiaGreenGates),
                                                           sm.canOpenGreenDoors()),
                                                    sm.wor(sm.canUsePowerBombs(),
                                                           RomPatches.has(RomPatches.RedTowerBlueDoors))),
        'Red Tower Top Left': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                 sm.wor(RomPatches.has(RomPatches.NoMaridiaGreenGates),
                                                        sm.canOpenGreenDoors()),
                                                 sm.canOpenYellowDoors())
    }, lambda sm: sm.wand(sm.haveItem('Morph'), RomPatches.has(RomPatches.NoMaridiaGreenGates)),
                exitInfo = {'RoomPtr':0x7a322, 'DoorPtr':0x90c6, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                            "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdaf, "area": 0x1},
                entryInfo = {'SamusX':0x2cd, 'SamusY':0x388}, shortName="B\\Top Red Tower"),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', {
        'Caterpillar Room Top Right': lambda sm: sm.setSMBool(True), # handled by room traverse function
        'Red Tower Top Left': lambda sm: sm.canOpenYellowDoors()
    }, exitInfo = {'RoomPtr':0x7962a, 'DoorPtr':0x8af6, 'direction': 0x7, "cap": (0x16, 0x2d), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0xb9f1, "area": 0x0},
                entryInfo = {'SamusX':0x80, 'SamusY':0x58}, shortName="B\\Red Elev."),
    AccessPoint('East Tunnel Right', 'RedBrinstar', {
        'East Tunnel Top Right': lambda sm: sm.setSMBool(True), # handled by room traverse function
        'Glass Tunnel Top': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                               sm.wor(sm.haveItem('Gravity'),
                                                      sm.haveItem('HiJump'))),
        'Red Tower Top Left': lambda sm: sm.canClimbBottomRedTower()
    }, exitInfo = {'RoomPtr':0x7cf80, 'DoorPtr':0xa384, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000, "area": 0x4},
                entryInfo = {'SamusX':0xce, 'SamusY':0x188}, shortName="B\\East Tunnel"),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.wor(RomPatches.has(RomPatches.NoMaridiaGreenGates),
                                               sm.canOpenGreenDoors())
    }, lambda sm: RomPatches.has(RomPatches.NoMaridiaGreenGates),
                exitInfo = {'RoomPtr':0x7cf80, 'DoorPtr':0xa390, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                            "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356, "area": 0x4},
                entryInfo = {'SamusX':0x3c6, 'SamusY':0x88}, shortName="B\\Top East Tunnel"),
    AccessPoint('Glass Tunnel Top', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.canUsePowerBombs()
    }, lambda sm: sm.canUsePowerBombs(),
                exitInfo = {'RoomPtr':0x7cefb, 'DoorPtr':0xa330, 'direction': 0x7, "cap": (0x16, 0x7d), "bitFlag": 0x0,
                            "screen": (0x1, 0x7), "distanceToSpawn": 0x200, "doorAsmPtr": 0x0000, "area": 0x4},
                entryInfo = {'SamusX':0x81, 'SamusY':0x78}, shortName="B\\Glass Tunnel")
]

vanillaTransitions = [
    ('Lower Mushrooms Left', 'Green Brinstar Elevator Right'),
    ('Morph Ball Room Left', 'Green Hill Zone Top Right'),
    ('Moat Right', 'West Ocean Left'),
    ('Keyhunter Room Bottom', 'Red Brinstar Elevator'),
    ('Noob Bridge Right', 'Red Tower Top Left'),
    ('Crab Maze Left', 'Le Coude Right'),
    ('Kronic Boost Room Bottom Left', 'Lava Dive Right'),
    ('Three Muskateers Room Left', 'Single Chamber Top Right'),
    ('Warehouse Entrance Left', 'East Tunnel Right'),
    ('East Tunnel Top Right', 'Crab Hole Bottom Left'),
    ('Caterpillar Room Top Right', 'Red Fish Room Left'),
    ('Glass Tunnel Top', 'Main Street Bottom')
]

    # up: 0x3, 0x7
    # down: 0x2, 0x6
    # left: 0x1, 0x5
    # right: 0x0, 0x4

def isHorizontal(dir):
    return dir in [0x1, 0x5, 0x0, 0x4]

def reverseDir(dir):
    if dir in [0x1, 0x5] or dir in [0x3, 0x7]:
        return dir - 1
    else:
        return dir + 1

def removeCap(dir):
    if dir < 4:
        return dir
    return dir - 4

def getDirection(src, dst):
    exitDir = src.ExitInfo['direction']
    entryDir = dst.EntryInfo['direction']
    # compatible transition
    if exitDir == entryDir:
        return exitDir
    # if incompatible but horizontal we just reverse
    if isHorizontal(exitDir) and isHorizontal(entryDir):
        return reverseDir(entryDir)
    # otherwise keep exit direction and remove cap XXX maybe keep horizontal transition in case of V>H? (untested yet)
    return removeCap(exitDir)

def getBitFlag(srcArea, dstArea, origFlag):
    flags = origFlag
    if srcArea == dstArea:
        flags &= 0xBF
    else:
        flags |= 0x40
    return flags

def getDoorConnections(graph):
    for srcName, dstName in vanillaTransitions:
        src = graph.accessPoints[srcName]
        dst = graph.accessPoints[dstName]
        dst.EntryInfo.update(src.ExitInfo)
        src.EntryInfo.update(dst.ExitInfo)
    connections = []
    for src, dst in graph.InterAreaTransitions:
        conn = {}
        # where to write
        conn['DoorPtr'] = src.ExitInfo['DoorPtr']
        conn['DoorRoomPtr'] = src.ExitInfo['RoomPtr'] # FIXME is this necessary?
        # door properties
        conn['RoomPtr'] = dst.ExitInfo['RoomPtr'] # room info is not exit info...
        conn['doorAsmPtr'] = dst.EntryInfo['doorAsmPtr']
        conn['direction'] = getDirection(src, dst)
        conn['bitFlag'] = getBitFlag(src.ExitInfo['area'], dst.ExitInfo['area'], # ...neither is area. FIXME move these in a RoomInfo dict in access points
                                     dst.EntryInfo['bitFlag'])
        conn['cap'] = dst.EntryInfo['cap']
        conn['screen'] = dst.EntryInfo['screen']
        if conn['direction'] != src.ExitInfo['direction']: # incompatible transition
            conn['distanceToSpawn'] = 0
            conn['SamusX'] = dst.EntryInfo['SamusX']
            conn['SamusY'] = dst.EntryInfo['SamusY']
        else:
            conn['distanceToSpawn'] = dst.EntryInfo['distanceToSpawn']
        connections.append(conn)
    return connections

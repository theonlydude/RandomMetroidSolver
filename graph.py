#!/usr/bin/python

import copy
from parameters import Knows
from rom import RomPatches
from smbool import SMBool

class AccessPoint(object):
    # name : AccessPoint name
    # graphArea : graph area the node is located in
    # transitions : intra-area transitions
    # traverse: traverse function, will be wand to the added transitions
    # exitInfo : dict carrying vanilla door information : 'DoorPtr': door address, 'direction', 'cap', 'screen', 'bitFlag', 'distanceToSpawn', 'doorAsmPtr' : door properties
    # entryInfo : dict carrying forced samus X/Y position with keys 'SamusX' and 'SamusY'.
    #             (to be updated after reading vanillaTransitions and gather entry info from matching exit door)
    # roomInfo : dict with 'RoomPtr' : room address, ''
    # shortName : short name for the credits
    def __init__(self, name, graphArea, transitions,
                 traverse=lambda sm: sm.setSMBool(True),
                 exitInfo=None, entryInfo=None, roomInfo=None, shortName=None):
        self.Name = name
        self.GraphArea = graphArea
        self.ExitInfo = exitInfo
        self.EntryInfo = entryInfo
        self.RoomInfo = roomInfo
        self.transitions = transitions
        self.traverse = traverse
        if shortName is not None:
            self.ShortName = shortName
        else:
            self.ShortName = str(self)
        self.distance = 0

    def __str__(self):
        return "[" + self.GraphArea + "] " + self.Name

    # for additions after construction (inter-area transitions)
    def addTransition(self, destName):
        self.transitions[destName] = lambda sm: self.traverse(sm)


class AccessGraph(object):
    def __init__(self, transitions, bidir=True, dotFile=None):
        self.accessPoints = {}
        self.InterAreaTransitions = []
        self.bidir = bidir
        for ap in accessPoints:
            ap.distance = 0
            self.accessPoints[ap.Name] = ap
        for srcName, dstName in transitions:
            self.addTransition(srcName, dstName, bidir)
        if dotFile is not None:
            self.toDot(dotFile)

    def getCreditsTransitions(self):
        transitionsDict = {}
        for (src, dest) in self.InterAreaTransitions:
            transitionsDict[src] = dest

        # remove duplicate (src, dest) - (dest, src)
        transitionsCopy = copy.copy(transitionsDict)
        for src in transitionsCopy:
            if src in transitionsDict:
                dest = transitionsDict[src]
                if dest in transitionsDict:
                    if transitionsDict[dest] == src:
                        del transitionsDict[dest]

        transitions = [(t, transitionsDict[t]) for t in transitionsDict]

        return transitions

    def toDot(self, dotFile):
        orientations = {
            'Lava Dive Right': 'w',
            'Noob Bridge Right': 'se',
            'Main Street Bottom': 's',
            'Red Tower Top Left': 'w',
            'Red Brinstar Elevator': 'n',
            'Moat Right': 'ne',
            'Le Coude Right': 'ne',
            'Warehouse Entrance Left': 'w',
            'Green Brinstar Elevator Right': 'ne',
            'Crab Hole Bottom Left': 'se',
            'Lower Mushrooms Left': 'nw',
            'East Tunnel Right': 'se',
            'Glass Tunnel Top': 's',
            'Green Hill Zone Top Right': 'e',
            'East Tunnel Top Right': 'e',
            'Crab Maze Left': 'e',
            'Caterpillar Room Top Right': 'ne',
            'Three Muskateers Room Left': 'n',
            'Morph Ball Room Left': 'sw',
            'Kronic Boost Room Bottom Left': 'se',
            'West Ocean Left': 'w',
            'Red Fish Room Left': 'w',
            'Single Chamber Top Right': 'ne',
            'Keyhunter Room Bottom': 'se'
        }
        colors = ['red', 'blue', 'green', 'yellow', 'skyblue', 'violet', 'orange',
                  'lawngreen', 'crimson', 'chocolate', 'turquoise', 'tomato']
        with open(dotFile, "w") as f:
            f.write("digraph {\n")
            f.write('size="30,30!";\n')
            f.write('rankdir=LR;\n')
            f.write('ranksep=2.2;\n')
            f.write('overlap=scale;\n')
            f.write('edge [dir="both",arrowhead="box",arrowtail="box",arrowsize=0.5,fontsize=7,style=dotted];\n')
            f.write('node [shape="box",fontsize=10];\n')
            for area in set([ap.GraphArea for ap in self.accessPoints.values()]):
                f.write(area + ";\n") # TODO area long name and color
            drawn = []
            i = 0
            for src, dst in self.InterAreaTransitions:
                if self.bidir is True and src.Name in drawn:
                    continue
                f.write('%s:%s -> %s:%s [taillabel="%s",headlabel="%s",color=%s];\n' % (src.GraphArea, orientations[src.Name], dst.GraphArea, orientations[dst.Name], src.Name, dst.Name, colors[i]))
                drawn += [src.Name,dst.Name]
                i += 1
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
    def getNewAvailNodes(self, availNodes, nodesToCheck, smbm, maxDiff, distance):
        newAvailNodes = {}
        for node in nodesToCheck:
            for dstName, tFunc in node.transitions.iteritems():
                dst = self.accessPoints[dstName]
                if dst in newAvailNodes or dst in availNodes:
                    continue
                # diff = tFunc(smbm)
                diff = smbm.eval(tFunc)
                if diff.bool == True and diff.difficulty <= maxDiff:
                    dst.distance = distance
                    newAvailNodes[dst] = diff
        return newAvailNodes

    # rootNode: starting AccessPoint instance
    # items: collected items
    # maxDiff: difficulty limit
    # return available AccessPoint list
    def getAvailableAccessPoints(self, rootNode, smbm, maxDiff):
        availNodes = { rootNode : SMBool(True, 0) }
        newAvailNodes = availNodes
        distance = 1
        while len(newAvailNodes) > 0:
            newAvailNodes = self.getNewAvailNodes(availNodes, newAvailNodes, smbm, maxDiff, distance)
            availNodes.update(newAvailNodes)
            distance += 1
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
                    loc['difficulty'] = SMBool(diff.bool,
                                               difficulty=max(tdiff.difficulty, diff.difficulty, apDiff.difficulty),
                                               knows=list(set(tdiff.knows + diff.knows + apDiff.knows)),
                                               items=list(set(tdiff.items + diff.items + apDiff.items)))
                    if diff.bool == True and diff.difficulty <= maxDiff:
                        loc['distance'] = ap.distance + 1
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
    }, shortName="C\\LANDING"),
    AccessPoint('Lower Mushrooms Left', 'Crateria', {
        'Landing Site': lambda sm: sm.canPassTerminatorBombWall(False)
    }, roomInfo = {'RoomPtr':0x9969, "area": 0x0},
       exitInfo = {'DoorPtr':0x8c22, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x36, 'SamusY':0x88},
       shortName="C\\MUSHROOMS"),
    AccessPoint('Moat Right', 'Crateria', {
        'Keyhunter Room Bottom': lambda sm: sm.canPassMoatReverse()
    }, roomInfo = {'RoomPtr':0x95ff, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aea, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1cf, 'SamusY':0x88},
       shortName="C\\MOAT"),
    AccessPoint('Keyhunter Room Bottom', 'Crateria', {
        'Moat Right': lambda sm: sm.wand(sm.canOpenYellowDoors(),
                                         sm.canPassMoat()),
        'Landing Site': lambda sm: sm.setSMBool(True)
    }, traverse = lambda sm: sm.canOpenYellowDoors(),
       roomInfo = { 'RoomPtr':0x948c, "area": 0x0 },
       exitInfo = {'DoorPtr':0x8a42, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14c, 'SamusY':0x2b8},
       shortName="C\\KEYHUNTERS"),
    AccessPoint('Morph Ball Room Left', 'Crateria', {
        'Landing Site': lambda sm: sm.canUsePowerBombs()
    }, roomInfo = { 'RoomPtr':0x9e9f, "area": 0x1},
       exitInfo = {'DoorPtr':0x8e9e, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x288},
       shortName="C\\MORPH"),
    # Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                                               sm.canDestroyBombWalls()), # pink
                                                        sm.haveItem('Morph'), # big pink
                                                        sm.canOpenGreenDoors()) # also implies first red door
    }, roomInfo = {'RoomPtr':0x9938, "area": 0x0},
       exitInfo = {'DoorPtr':0x8bfe, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xcc, 'SamusY':0x88},
       shortName="B\\GREEN ELEV."),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', {
        'Noob Bridge Right': lambda sm: sm.setSMBool(True),
        'Green Brinstar Elevator Right': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'),
                                                                   sm.canDestroyBombWalls()), # pink
                                                            sm.haveItem('Morph')) # big pink
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
       roomInfo = {'RoomPtr':0x9e52, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8e86, 'direction': 0x4, "cap": (0x1, 0x26), "bitFlag": 0x0,
                   "screen": (0x0, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x1c7, 'SamusY':0x88},
       shortName="B\\GREEN HILL"),
    AccessPoint('Noob Bridge Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wor(sm.haveItem('Wave'),
                                                       sm.wand(sm.canOpenRedDoors(), # can do the glitch with either missile or supers
                                                               sm.knowsGreenGateGlitch()))
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenGreenDoors()),
       roomInfo = {'RoomPtr':0x9fba, "area": 0x1 },
       exitInfo = {'DoorPtr':0x8f0a, 'direction': 0x4, "cap": (0x1, 0x46), "bitFlag": 0x0,
                   "screen": (0x0, 0x4), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x5ce, 'SamusY':0x88},
       shortName="B\\NOOB BRIDGE"),
    # Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', {
        'Crab Maze Left': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                             sm.canPassSpongeBath(), # implies dead phantoon and pass bomb passages
                                             sm.canPassForgottenHighway(True))
    }, roomInfo = {'RoomPtr':0x93fe, "area": 0x0},
       exitInfo = {'DoorPtr':0x89ca, 'direction': 0x5, "cap": (0x1e, 0x6), "bitFlag": 0x0,
                   "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x488},
       shortName="W\\WEST OCEAN"),
    AccessPoint('Crab Maze Left', 'WreckedShip', {
        'West Ocean Left': lambda sm: sm.canPassForgottenHighway(False)
    }, roomInfo = {'RoomPtr':0x957d, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aae, 'direction': 0x5, "cap": (0xe, 0x6), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x34, 'SamusY':0x188},
       shortName="W\\CRAB MAZE"),
    # Lower Norfair
    AccessPoint('Lava Dive Right', 'LowerNorfair', {
        'Three Muskateers Room Left': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'),
                                                         sm.canPassLavaPit(),
                                                         sm.canPassWorstRoom())
    }, roomInfo = {'RoomPtr':0xaf14, "area": 0x2},
       exitInfo = {'DoorPtr':0x96d2, 'direction': 0x4, "cap": (0x11, 0x26), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x3d0, 'SamusY':0x88},
       shortName="LN\\LAVA DIVE"),
    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', {
        'Lava Dive Right': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'),
                                              sm.canPassAmphitheaterReverse()) # if this is OK, reverse lava pit will be too...
    }, roomInfo = {'RoomPtr':0xb656, "area": 0x2},
       exitInfo = {'DoorPtr':0x9a4a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x88},
       shortName="LN\\THREE MUSK."),
    # Norfair
    AccessPoint('Warehouse Entrance Left', 'Norfair', {
        'Single Chamber Top Right': lambda sm: sm.canAccessHeatedNorfairFromEntrance(),
        'Kronic Boost Room Bottom Left': lambda sm: sm.canAccessHeatedNorfairFromEntrance()
    }, roomInfo = {'RoomPtr':0xa6a1, "area": 0x1},
       exitInfo = {'DoorPtr':0x922e, 'direction': 0x5, "cap": (0xe, 0x16), "bitFlag": 0x40,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdd1},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       shortName="N\\WAREHOUSE"),
    AccessPoint('Single Chamber Top Right', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                      sm.haveItem('Morph'),
                                                      sm.canHellRun('MainUpperNorfair')),
        'Kronic Boost Room Bottom Left': lambda sm: sm.wand(sm.canDestroyBombWalls(),
                                                            sm.haveItem('Morph'),
                                                            sm.canHellRun('MainUpperNorfair'))
    }, traverse=lambda sm: sm.wand(sm.canDestroyBombWalls(),
                           sm.haveItem('Morph'),
                           RomPatches.has(RomPatches.SingleChamberNoCrumble)),
        roomInfo = {'RoomPtr':0xad5e, "area": 0x2},
        exitInfo = {'DoorPtr':0x95fa, 'direction': 0x4, "cap": (0x11, 0x6), "bitFlag": 0x0,
                    "screen": (0x1, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
        entryInfo = {'SamusX':0x5cf, 'SamusY':0x88},
        shortName="N\\SINGLE CHAMBER"),
    AccessPoint('Kronic Boost Room Bottom Left', 'Norfair', {
        'Single Chamber Top Right': lambda sm: sm.canHellRun('MainUpperNorfair'),
        'Warehouse Entrance Left': lambda sm: sm.canHellRun('MainUpperNorfair')
    }, traverse=lambda sm: sm.wor(RomPatches.has(RomPatches.AreaRandoBlueDoors), sm.canOpenYellowDoors()),
       roomInfo = {'RoomPtr':0xae74, "area": 0x2},
       exitInfo = {'DoorPtr':0x967e, 'direction': 0x5, "cap": (0x3e, 0x6), "bitFlag": 0x0,
                   "screen": (0x3, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x134, 'SamusY':0x288},
       shortName="N\\KRONIC BOOST"),
    # Maridia
    AccessPoint('Main Street Bottom', 'Maridia', {
        'Red Fish Room Left': lambda sm: sm.canGoUpMtEverest(),
        'Crab Hole Bottom Left': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                    sm.canOpenGreenDoors()), # red door+green gate
        'Le Coude Right': lambda sm: sm.wand(sm.canOpenGreenDoors(), # gate+door
                                             sm.wor(sm.haveItem('Gravity'),
                                                    sm.wand(sm.knowsGravLessLevel3(),
                                                            sm.haveItem('HiJump')))) # for the sand pits
    }, roomInfo = {'RoomPtr':0xcfc9, "area": 0x4},
       exitInfo = {'DoorPtr':0xa39c, 'direction': 0x6, "cap": (0x6, 0x2), "bitFlag": 0x0,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x170, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x14a, 'SamusY':0x7a8},
       shortName="M\\MAIN STREET"),
    AccessPoint('Crab Hole Bottom Left', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.wand(sm.canExitCrabHole(),
                                                 sm.wand(sm.haveItem('Super'),
                                                         sm.knowsGreenGateGlitch())),
        'Le Coude Right': lambda sm: sm.wand(sm.canExitCrabHole(),
                                             sm.canOpenGreenDoors(), # toilet door
                                             sm.wor(sm.haveItem('Gravity'),
                                                    sm.wand(sm.knowsGravLessLevel3(),
                                                            sm.haveItem('HiJump')))) # for the sand pits
    }, traverse = lambda sm: sm.haveItem('Morph'),
       roomInfo = {'RoomPtr':0xd21c, "area": 0x4},
       exitInfo = {'DoorPtr':0xa510, 'direction': 0x5,
                   "cap": (0x3e, 0x6), "screen": (0x3, 0x0), "bitFlag": 0x0,
                   "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x28, 'SamusY':0x188},
       shortName="M\\CRAB HOLE"),
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
    }, roomInfo = {'RoomPtr':0x95a8, "area": 0x0},
       exitInfo = {'DoorPtr':0x8aa2, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xd1, 'SamusY':0x88},
       shortName="M\\COUDE"),
    AccessPoint('Red Fish Room Left', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.haveItem('Morph') # just go down
    }, traverse=lambda sm: sm.haveItem('Morph'),
       roomInfo = {'RoomPtr':0xd104, "area": 0x4},
       exitInfo = {'DoorPtr':0xa480, 'direction': 0x5, "cap": (0x2e, 0x36), "bitFlag": 0x40,
                   "screen": (0x2, 0x3), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe367},
       entryInfo = {'SamusX':0x34, 'SamusY':0x88},
       shortName="M\\RED FISH"),
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
    }, roomInfo = {'RoomPtr':0xa253, "area": 0x1},
       exitInfo = {'DoorPtr':0x902a, 'direction': 0x5, "cap": (0x5e, 0x6), "bitFlag": 0x0,
                   "screen": (0x5, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x2f, 'SamusY':0x488},
       shortName="B\\RED TOWER"),
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
    }, traverse=lambda sm: sm.wand(sm.haveItem('Morph'), RomPatches.has(RomPatches.NoMaridiaGreenGates)),
       roomInfo = {'RoomPtr':0xa322, "area": 0x1},
       exitInfo = {'DoorPtr':0x90c6, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xbdaf},
       entryInfo = {'SamusX':0x2cd, 'SamusY':0x388},
       shortName="B\\TOP RED TOWER"),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', {
        'Caterpillar Room Top Right': lambda sm: sm.setSMBool(True), # handled by room traverse function
        'Red Tower Top Left': lambda sm: sm.canOpenYellowDoors()
    }, roomInfo = {'RoomPtr':0x962a, "area": 0x0},
       exitInfo = {'DoorPtr':0x8af6, 'direction': 0x7, "cap": (0x16, 0x2d), "bitFlag": 0x0,
                   "screen": (0x1, 0x2), "distanceToSpawn": 0x1c0, "doorAsmPtr": 0xb9f1},
       entryInfo = {'SamusX':0x80, 'SamusY':0x58},
       shortName="B\\RED ELEV."),
    AccessPoint('East Tunnel Right', 'RedBrinstar', {
        'East Tunnel Top Right': lambda sm: sm.setSMBool(True), # handled by room traverse function
        'Glass Tunnel Top': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                               sm.wor(sm.haveItem('Gravity'),
                                                      sm.haveItem('HiJump'))),
        'Red Tower Top Left': lambda sm: sm.canClimbBottomRedTower()
    }, roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa384, 'direction': 0x4, "cap": (0x1, 0x6), "bitFlag": 0x40,
                   "screen": (0x0, 0x0), "distanceToSpawn": 0x8000, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0xce, 'SamusY':0x188},
       shortName="B\\EAST TUNNEL"),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.wor(RomPatches.has(RomPatches.NoMaridiaGreenGates),
                                               sm.canOpenGreenDoors())
    }, traverse=lambda sm: RomPatches.has(RomPatches.NoMaridiaGreenGates),
       roomInfo = {'RoomPtr':0xcf80, "area": 0x4},
       exitInfo = {'DoorPtr':0xa390, 'direction': 0x4, "cap": (0x1, 0x16), "bitFlag": 0x0,
                   "screen": (0x0, 0x1), "distanceToSpawn": 0x8000, "doorAsmPtr": 0xe356},
       entryInfo = {'SamusX':0x3c6, 'SamusY':0x88},
       shortName="B\\TOP EAST TUNNEL"),
    AccessPoint('Glass Tunnel Top', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.canUsePowerBombs()
    }, traverse=lambda sm: sm.wand(sm.wor(sm.haveItem('Gravity'),
                                          sm.haveItem('HiJump')),
                                   sm.canUsePowerBombs()),
       roomInfo = {'RoomPtr':0xcefb, "area": 0x4},
       exitInfo = {'DoorPtr':0xa330, 'direction': 0x7, "cap": (0x16, 0x7d), "bitFlag": 0x0,
                   "screen": (0x1, 0x7), "distanceToSpawn": 0x200, "doorAsmPtr": 0x0000},
       entryInfo = {'SamusX':0x81, 'SamusY':0x78},
       shortName="B\\GLASS TUNNEL")
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

def isVanillaTransitions(transitions):
    for src, dest in transitions:
        found = False
        for vsrc, vdest in vanillaTransitions:
            if (src == vsrc and dest == vdest) or (src == vdest and dest == vsrc):
                found = True
                break
        if found == False:
            return False
    return True

    # up: 0x3, 0x7
    # down: 0x2, 0x6
    # left: 0x1, 0x5
    # right: 0x0, 0x4

def isHorizontal(dir):
    return dir in [0x1, 0x5, 0x0, 0x4]

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
    # if incompatible but horizontal we keep entry dir (looks more natural)
    if isHorizontal(exitDir) and isHorizontal(entryDir):
        return entryDir
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
        conn['ID'] = str(src) + ' -> ' + str(dst)
        # where to write
        conn['DoorPtr'] = src.ExitInfo['DoorPtr']
        # door properties
        conn['RoomPtr'] = dst.RoomInfo['RoomPtr']
        conn['doorAsmPtr'] = dst.EntryInfo['doorAsmPtr']
        conn['direction'] = getDirection(src, dst)
        conn['bitFlag'] = getBitFlag(src.RoomInfo['area'], dst.RoomInfo['area'],
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

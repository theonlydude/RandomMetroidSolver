#!/usr/bin/python

from parameters import Knows
from rom import RomPatches
from smbool import SMBool

class AccessPoint(object):
    # name : AccessPoint name
    # graphArea : graph area the node is located in
    # transitions : intra-area transitions
    # traverse: traverse function, will be wand to the added transitions
    # TODO add SNES door attributes (or some kind of Tag property to carry it)
    def __init__(self, name, graphArea, transitions, traverse=lambda sm: sm.setSMBool(True)):
        self.Name = name
        self.GraphArea = graphArea
        self.transitions = transitions
        self.traverse = traverse

    def __str__(self):
        return "[" + self.GraphArea + "] " + self.Name

    # for additions after construction (inter-area transitions)
    def addTransition(self, destName):
        self.transitions[destName] = lambda sm: self.traverse(sm)

# all access points and traverse functions
accessPoints = [
    # Crateria and Blue Brinstar
    AccessPoint('Landing Site', 'Crateria', {
        'Lower Mushrooms Left': lambda sm: sm.canPassTerminatorBombWall(),
        'Keyhunter Room Bottom': lambda sm: sm.canOpenGreenDoors(),
        'Morph Ball Room Left': lambda sm: sm.canUsePowerBombs()
    }),
    AccessPoint('Lower Mushrooms Left', 'Crateria', {
        'Landing Site': lambda sm: sm.canPassTerminatorBombWall()
    }),
    AccessPoint('Moat Right', 'Crateria', {
        'Keyhunter Room Bottom': lambda sm: sm.canPassMoatReverse()
    }),
    AccessPoint('Keyhunter Room Bottom', 'Crateria', {
        'Moat Right': lambda sm: sm.wand(sm.canOpenYellowDoors(),
                                         sm.canPassMoat()),
        'Landing Site': lambda sm: sm.setSMBool(True)
    }, lambda sm: sm.canOpenYellowDoors()),
    AccessPoint('Morph Ball Room Left', 'Crateria', {
        'Landing Site': lambda sm: sm.canUsePowerBombs()
    }),
    # Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'), sm.canDestroyBombWalls()), # pink
                                                        sm.haveItem('Morph'), # big pink
                                                        sm.canOpenGreenDoors()) # also implies first red door
    }),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', {
        'Noob Bridge Right': lambda sm: sm.setSMBool(True),
        'Green Brinstar Elevator Right': lambda sm: sm.wand(sm.wor(sm.haveItem('SpeedBooster'), sm.canDestroyBombWalls()), # pink
                                                            sm.haveItem('Morph')) # big pink
    }, lambda sm: sm.canOpenYellowDoors()),
    AccessPoint('Noob Bridge Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda sm: sm.wor(sm.haveItem('Wave'),
                                                       sm.wand(sm.canOpenRedDoors(), # can do the glitch with either missile or supers
                                                               sm.knowsGreenGateGlitch()))
    }, lambda sm: sm.canOpenGreenDoors()),
    # Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', {
        'Crab Maze Left': lambda sm: sm.wand(sm.canOpenGreenDoors(),
                                             sm.canPassSpongeBath(), # implies dead phantoon and pass bomb passages
                                             sm.canPassForgottenHighway(True))
    }),
    AccessPoint('Crab Maze Left', 'WreckedShip', {
        'West Ocean Left': lambda sm: sm.canPassForgottenHighway(False)
    }),
    # Lower Norfair
    AccessPoint('Lava Dive Right', 'LowerNorfair', {
        'Three Muskateers Room Left': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'),
                                                         sm.canPassLavaPit(),
                                                         sm.canPassWorstRoom())
    }),
    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', {
        'Lava Dive Right': lambda sm: sm.wand(sm.canHellRun('LowerNorfair'),
                                              sm.canPassAmphitheaterReverse()) # if this is OK, reverse lava pit will be too...
    }),
    # Norfair   
    AccessPoint('Warehouse Entrance Left', 'Norfair', {
        'Single Chamber Top Right': lambda sm: sm.canAccessHeatedNorfairFromEntrance(),
        'Kronic Boost Room Bottom Left': lambda sm: sm.canAccessHeatedNorfairFromEntrance()
    }),
    AccessPoint('Single Chamber Top Right', 'Norfair', {
        'Warehouse Entrance Left': lambda sm: sm.wand(sm.canDestroyBombWalls(), sm.haveItem('Morph'), sm.canHellRun('MainUpperNorfair')),
        'Kronic Boost Room Bottom Left': lambda sm: sm.wand(sm.canDestroyBombWalls(), sm.haveItem('Morph'), sm.canHellRun('MainUpperNorfair'))
    }, lambda sm: sm.wand(sm.canDestroyBombWalls(), sm.haveItem('Morph'), RomPatches.has(RomPatches.SingleChamberNoCrumble))),
    AccessPoint('Kronic Boost Room Bottom Left', 'Norfair', {
        'Single Chamber Top Right': lambda sm: sm.canHellRun('MainUpperNorfair'),
        'Warehouse Entrance Left': lambda sm: sm.canHellRun('MainUpperNorfair')
    }, lambda sm: sm.canOpenYellowDoors()),
    # Maridia
    AccessPoint('Main Street Bottom', 'Maridia', {
        'Red Fish Room Left': lambda sm: sm.canGoUpMtEverest(),
        'Crab Hole Bottom Left': lambda sm: sm.wand(sm.haveItem('Morph'), sm.canOpenGreenDoors()), # red door+green gate
        'Le Coude Right': lambda sm: sm.wand(sm.canOpenGreenDoors(), # gate+door
                                             sm.wor(sm.haveItem('Gravity'), sm.wand(sm.knowsGravLessLevel3(), sm.haveItem('HiJump')))) # for the sand pits
    }),
    AccessPoint('Crab Hole Bottom Left', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.wand(sm.canExitCrabHole(),
                                                 sm.wand(sm.haveItem('Super'), sm.knowsGreenGateGlitch())),
        'Le Coude Right': lambda sm: sm.wand(sm.canExitCrabHole(),
                                             sm.canOpenGreenDoors(), # toilet door
                                             sm.wor(sm.haveItem('Gravity'), sm.wand(sm.knowsGravLessLevel3(), sm.haveItem('HiJump')))) # for the sand pits
    }, lambda sm: sm.haveItem('Morph')),
    AccessPoint('Le Coude Right', 'Maridia', {
        'Crab Hole Bottom Left': lambda sm: sm.wand(sm.canOpenYellowDoors(),
                                                    sm.wor(sm.haveItem('Gravity'), sm.wand(sm.knowsGravLessLevel3(), sm.haveItem('HiJump'))), # for the sand pits
                                                    sm.canOpenGreenDoors()), # toilet door
        'Main Street Bottom': lambda sm: sm.wand(sm.canOpenYellowDoors(),
                                                 sm.wand(sm.wor(sm.haveItem('Gravity'), sm.wand(sm.knowsGravLessLevel3(), sm.haveItem('HiJump'))), # for the sand pits
                                                         sm.canOpenGreenDoors(), # toilet door
                                                         sm.knowsGreenGateGlitch())),
    }),
    AccessPoint('Red Fish Room Left', 'Maridia', {
        'Main Street Bottom': lambda sm: sm.setSMBool(True) # just go down
    }),
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
    }),
    AccessPoint('Caterpillar Room Top Right', 'RedBrinstar', {
        'Red Brinstar Elevator': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                    sm.wor(RomPatches.has(RomPatches.NoMaridiaGreenGates), sm.canOpenGreenDoors()),
                                                    sm.wor(sm.canUsePowerBombs(),
                                                           RomPatches.has(RomPatches.RedTowerBlueDoors))),
        'Red Tower Top Left': lambda sm: sm.wand(sm.haveItem('Morph'),
                                                 sm.wor(RomPatches.has(RomPatches.NoMaridiaGreenGates), sm.canOpenGreenDoors()),
                                                 sm.canOpenYellowDoors())
    }, lambda sm: sm.wand(sm.haveItem('Morph'), RomPatches.has(RomPatches.NoMaridiaGreenGates))),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', {
        'Caterpillar Room Top Right': lambda sm: sm.setSMBool(True), # handled by room traverse function
        'Red Tower Top Left': lambda sm: sm.canOpenYellowDoors()
    }),
    AccessPoint('East Tunnel Right', 'RedBrinstar', {
        'East Tunnel Top Right': lambda sm: sm.setSMBool(True), # handled by room traverse function
        'Glass Tunnel Top': lambda sm: sm.wand(sm.canUsePowerBombs(),
                                               sm.wor(sm.haveItem('Gravity'),
                                                      sm.haveItem('HiJump'))),
        'Red Tower Top Left': lambda sm: sm.canClimbBottomRedTower()
    }),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.wor(RomPatches.has(RomPatches.NoMaridiaGreenGates),
                                               sm.canOpenGreenDoors())
    }, lambda sm: RomPatches.has(RomPatches.NoMaridiaGreenGates)),
    AccessPoint('Glass Tunnel Top', 'RedBrinstar', {
        'East Tunnel Right': lambda sm: sm.canUsePowerBombs()
    }, lambda sm: sm.canUsePowerBombs())
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

class AccessGraph(object):
    def __init__(self, transitions, bidir=True, dotFile=None):
        self.accessPoints = {}
        for ap in accessPoints:
            self.accessPoints[ap.Name] = ap
        for srcName, dstName in transitions:
            self.addTransition(srcName, dstName, bidir)
        if dotFile is not None:
            self.toDot(dotFile)

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
        if both is True:
            self.addTransition(dstName, srcName, False)

    # availNodes: all already available nodes
    # nodesToCheck: nodes we have to check transitions for
    # items: collected items
    # maxDiff: difficulty limit
    # return newly opened access points 
    def getNewAvailNodes(self, availNodes, nodesToCheck, smbm, maxDiff):
        newAvailNodes = []
        for node in nodesToCheck:
            for dstName, tFunc in node.transitions.iteritems():
                dst = self.accessPoints[dstName]
                if dst in newAvailNodes or dst in availNodes:
                    continue
                # diff = tFunc(smbm)
                diff = smbm.eval(tFunc)
                if diff.bool == True and diff.difficulty <= maxDiff:
                    newAvailNodes.append(dst)
        return newAvailNodes

    # rootNode: starting AccessPoint instance
    # items: collected items
    # maxDiff: difficulty limit
    # return available AccessPoint list
    def getAvailableAccessPoints(self, rootNode, smbm, maxDiff):
        availNodes = [ rootNode ]
        newAvailNodes = availNodes
        while len(newAvailNodes) > 0:
            newAvailNodes = self.getNewAvailNodes(availNodes, newAvailNodes, smbm, maxDiff)
            availNodes += newAvailNodes
        return availNodes
    
    # locations: locations to check
    # items: collected items
    # maxDiff: difficulty limit
    # return available locations list, also stores difficulty in locations
    def getAvailableLocations(self, locations, smbm, maxDiff):
        availAcessPoints = self.getAvailableAccessPoints(self.accessPoints['Landing Site'], smbm, maxDiff)
        availAreas = set([ap.GraphArea for ap in availAcessPoints])
        availLocs = []
        for loc in locations:
            if not loc['GraphArea'] in availAreas:
                continue
            for apName,tFunc in loc['AccessFrom'].iteritems():
                ap = self.accessPoints[apName]
                if not ap in availAcessPoints:
                    continue
                tdiff = smbm.eval(tFunc)
                if tdiff.bool == True and tdiff.difficulty <= maxDiff:
                    diff = smbm.eval(loc['Available'])
                    # TODO::after the jm tests, put it back
                    loc['difficulty'] = SMBool(diff.bool, max(tdiff.difficulty, diff.difficulty))
                    #loc['difficulty'] = SMBool(diff.bool, tdiff.difficulty + diff.difficulty)
                    if diff.bool == True and diff.difficulty <= maxDiff:
                        availLocs.append(loc)
                        break
                else:
                    loc['difficulty'] = tdiff
        return availLocs


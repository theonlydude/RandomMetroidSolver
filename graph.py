#!/usr/bin/python

from graph_helpers import wand, wor, haveItem, canPassMoat, canPassMoatReverse, canOpenGreenDoors, canPassTerminatorBombWall, canOpenYellowDoors, canDestroyBombWalls, canOpenRedDoors, canPassSpongeBath, canPassForgottenHighway, canHellRun, canPassLavaPit, canPassWorstRoom, canPassAmphitheaterReverse, canGoUpMtEverest, canClimbRedTower, canClimbBottomRedTower, canUsePowerBombs, canAccessHeatedNorfairFromEntrance, canDoSuitlessOuterMaridia
from parameters import Knows
from rom import RomPatches
from smbool import SMBool

class AccessPoint(object):
    # name : AccessPoint name
    # graphArea : graph area the node is located in
    # transitions : intra-area transitions
    # traverse: traverse function, will be wand to the added transitions
    # TODO add SNES door attributes (or some kind of Tag property to carry it)
    def __init__(self, name, graphArea, transitions, traverse=lambda items: SMBool(True, 0)):
        self.Name = name
        self.GraphArea = graphArea
        self.transitions = transitions
        self.traverse = traverse

    def __str__(self):
        return "[" + self.GraphArea + "] " + self.name

    # for additions after construction (inter-area transitions)
    def addTransition(self, destName):
        self.transitions[destName] = lambda items: self.traverse(items)
    
    def getTransition(self, destName, items):
        if not destName in self.transitions:
            return (False, 0)
        return self.transitions[destName](items)


# all access points and traverse functions
accessPoints = [
    # Crateria and Blue Brinstar
    AccessPoint('Landing Site', 'Crateria', {
        'Lower Mushrooms Left': lambda items: canPassTerminatorBombWall(items),
        'Keyhunter Room Bottom': lambda items: canOpenGreenDoors(items),
        'Morph Ball Room Left': lambda items: canUsePowerBombs(items)
    }),
    AccessPoint('Lower Mushrooms Left', 'Crateria', {
        'Landing Site': lambda items: canPassTerminatorBombWall(items)
    }),
    AccessPoint('Moat Right', 'Crateria', {
        'Keyhunter Room Bottom': lambda items: canPassMoatReverse(items)
    }),
    AccessPoint('Keyhunter Room Bottom', 'Crateria', {
        'Moat Right': lambda items: canPassMoat(items),
        'Landing Site': lambda items: SMBool(True, 0)
    }, lambda items: canOpenYellowDoors(items)),
    AccessPoint('Morph Ball Room Left', 'Crateria', {
         'Landing Site': lambda items: canUsePowerBombs(items)
    }),
    # Green and Pink Brinstar
    AccessPoint('Green Brinstar Elevator Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda items: wand(canDestroyBombWalls(items), # pink
                                                        haveItem(items, 'Morph'), # big pink
                                                        canOpenGreenDoors(items)) # also implies first red door
    }),
    AccessPoint('Green Hill Zone Top Right', 'GreenPinkBrinstar', {
        'Noob Bridge Right': lambda items: SMBool(True, 0),
        'Green Brinstar Elevator Right': lambda items: wand(canDestroyBombWalls(items), # pink
                                                            haveItem(items, 'Morph')) # big pink
    }, lambda items: canOpenYellowDoors(items)),
    AccessPoint('Noob Bridge Right', 'GreenPinkBrinstar', {
        'Green Hill Zone Top Right': lambda items: wor(haveItem(items, 'Wave'),
                                                       wand(canOpenRedDoors(items), # can do the glitch with either missile or supers
                                                            Knows.GreenGateGlitch))
    }),
    # Wrecked Ship
    AccessPoint('West Ocean Left', 'WreckedShip', {
        'Crab Maze Left': lambda items: wand(canOpenGreenDoors(items),
                                             canPassSpongeBath(items), # implies dead phantoon
                                             canPassForgottenHighway(items, True))
    }),
    AccessPoint('Crab Maze Left', 'WreckedShip', {
        'West Ocean Left': lambda items: canPassForgottenHighway(items, False)
    }),
    # Lower Norfair
    AccessPoint('Lava Dive Right', 'LowerNorfair', {
        'Three Muskateers Room Left': lambda items: wand(canHellRun(items, 'LowerNorfair'),
                                                         canPassLavaPit(items),
                                                         canPassWorstRoom(items))
    }),
    AccessPoint('Three Muskateers Room Left', 'LowerNorfair', {
        'Lava Dive Right': lambda items: wand(canHellRun(items, 'LowerNorfair'),
                                              canPassAmphitheaterReverse(items)) # if this is OK, reverse lava pit will be too...
    }),
    # Norfair   
    AccessPoint('Warehouse Entrance Left', 'Norfair', {
        'Single Chamber Top Right': lambda items: wand(canAccessHeatedNorfairFromEntrance(items),
                                                       RomPatches.has(RomPatches.SingleChamberNoCrumble)),
        'Kronic Boost Room Bottom Right': lambda items: canAccessHeatedNorfairFromEntrance(items)
    }),
    AccessPoint('Single Chamber Top Right', 'Norfair', {
        'Warehouse Entrance Left': lambda items: canHellRun(items, 'MainUpperNorfair'),
        'Kronic Boost Room Bottom Right': lambda items: canHellRun(items, 'MainUpperNorfair')
    }),
    AccessPoint('Kronic Boost Room Bottom Right', 'Norfair', {
        'Single Chamber Top Right': lambda items: wand(canHellRun(items, 'MainUpperNorfair'),
                                                       RomPatches.has(RomPatches.SingleChamberNoCrumble)),
        'Warehouse Entrance Left': lambda items: canHellRun(items, 'MainUpperNorfair')
    }, lambda items: canOpenYellowDoors(items)),
    # Maridia
    AccessPoint('Main Street Bottom', 'Maridia', {
        'Red Fish Room Left': lambda items: canGoUpMtEverest(items),
        'Crab Hole Bottom Left': lambda items: canOpenGreenDoors(items), # red door+green gate
    }),
    AccessPoint('Crab Hole Bottom Left', 'Maridia', {
        'Main Street Bottom': lambda items: wand(wor(haveItem(items, 'Gravity'), 
                                                     canDoSuitlessOuterMaridia(items)),
                                                 wand(haveItem(items, 'Super'), Knows.GreenGateGlitch)),
        'Le Coude Right': lambda items: wand(wor(haveItem(items, 'Gravity'), 
                                                     canDoSuitlessOuterMaridia(items)),
                                             canOpenGreenDoors(items)) # toilet door
    }),
    AccessPoint('Le Coude Right', 'Maridia', {
        'Crab Hole Bottom Left': lambda items: wand(canOpenYellowDoors(items),
                                                    wand(wor(haveItem(items, 'Gravity'),
                                                             haveItem(items, 'HiJump')), # the sand pit to go through is possible with no gravity or particular knowledge. FIXME is HiJump necessary?
                                                         canOpenGreenDoors(items))), # toilet door
        'Main Street Bottom': lambda items: wand(canOpenYellowDoors(items),
                                                 wand(wor(haveItem(items, 'Gravity'),
                                                          haveItem(items, 'HiJump')), # the sand pit to go through is possible with no gravity or particular knowledge. FIXME is HiJump necessary?
                                                      canOpenGreenDoors(items), # toilet door
                                                      Knows.GreenGateGlitch)),
    }),
    AccessPoint('Red Fish Room Left', 'Maridia', {
        'Main Street Bottom': lambda items: SMBool(True, 0) # just go down
    }),
    # Red Brinstar. Main nodes: Red Tower Top Left, East Tunnel Right
    AccessPoint('Red Tower Top Left', 'RedBrinstar', {
        # go up
        'Red Brinstar Elevator': lambda items: wand(canClimbRedTower(items),
                                                    wor(canOpenYellowDoors(items),
                                                        RomPatches.has(RomPatches.RedTowerBlueDoors))),
        'Caterpillar Room Top Right': lambda items: wand(haveItem(items, 'Morph'),
                                                         RomPatches.has(RomPatches.NoMaridiaGreenGates),
                                                         canClimbRedTower(items)),
        # go down
        'East Tunnel Right': lambda items: SMBool(True, 0)
    }),
    AccessPoint('Caterpillar Room Top Right', 'RedBrinstar', {
        'Red Brinstar Elevator': lambda items: wand(wor(RomPatches.has(RomPatches.NoMaridiaGreenGates), canOpenGreenDoors(items)),
                                                    wor(canUsePowerBombs(items),
                                                        RomPatches.has(RomPatches.RedTowerBlueDoors))),
        'Red Tower Top Left': lambda items: wand(wor(RomPatches.has(RomPatches.NoMaridiaGreenGates), canOpenGreenDoors(items)),
                                                 canOpenYellowDoors(items))
    }, lambda items: haveItem(items, 'Morph')),
    AccessPoint('Red Brinstar Elevator', 'RedBrinstar', {
        'Caterpillar Room Top Right': lambda items: wand(haveItem(items, 'Morph'), RomPatches.has(RomPatches.NoMaridiaGreenGates)),
        'Red Tower Top Left': lambda items: canOpenYellowDoors(items)
    }),
    AccessPoint('East Tunnel Right', 'RedBrinstar', {
        'East Tunnel Top Right': lambda items: RomPatches.has(RomPatches.NoMaridiaGreenGates),
        'Glass Tunnel Top': lambda items: wand(canUsePowerBombs(items),
                                               wor(haveItem(items, 'Gravity'),
                                                   haveItem(items, 'HiJump'))),
        'Red Tower Top Left': lambda items: canClimbBottomRedTower(items)
    }),
    AccessPoint('East Tunnel Top Right', 'RedBrinstar', {
        'East Tunnel Right': lambda items: wor(RomPatches.has(RomPatches.NoMaridiaGreenGates),
                                               canOpenGreenDoors(items))
    }),
    AccessPoint('Glass Tunnel Top', 'RedBrinstar', {
        'East Tunnel Right': lambda items: canUsePowerBombs(items)
    }, lambda items: canUsePowerBombs(items))
]

vanillaTransitions = [
    ('Lower Mushrooms Left', 'Green Brinstar Elevator Right'),
    ('Morph Ball Room Left', 'Green Hill Zone Top Right'),
    ('Moat Right', 'West Ocean Left'),
    ('Keyhunter Room Bottom', 'Red Brinstar Elevator'),
    ('Noob Bridge Right', 'Red Tower Top Left'),
    ('Crab Maze Left', 'Le Coude Right'),
    ('Kronic Boost Room Bottom Right', 'Lava Dive Right'),
    ('Three Muskateers Room Left', 'Single Chamber Top Right'),
    ('Warehouse Entrance Left', 'East Tunnel Right'),
    ('East Tunnel Top Right', 'Crab Hole Bottom Left'),
    ('Caterpillar Room Top Right', 'Red Fish Room Left'),
    ('Glass Tunnel Top', 'Main Street Bottom')
]

class AccessGraph(object):
    def __init__(self, transitions, bidir=True):
        self.accessPoints = {}
        for ap in accessPoints:
            self.accessPoints[ap.Name] = ap
        for t in transitions:
            self.addTransition(t[0], t[1], bidir)

    def addTransition(self, srcName, dstName, both=True):
        src = self.accessPoints[srcName]
        dst = self.accessPoints[dstName]
        if src.GraphArea == dst.GraphArea:
            raise ValuError('Invalid transition : "' + srcName + '" and "' + dstName + '" are both in "' + src.GraphArea + '"')
        src.addTransition(dstName)
        if both is True:
            self.addTransition(dstName, srcName, False)

    # availNodes: all already available nodes
    # nodesToCheck: nodes we have to check transitions for
    # items: collected items
    # maxDiff: difficulty limit
    # return newly opened access points 
    def getNewAvailNodes(self, availNodes, nodesToCheck, items, maxDiff):
        newAvailNodes = []
        for node in nodesToCheck:
            for dstName, tFunc in node.transitions.iteritems():
                dst = self.accessPoints[dstName]
                if dst in newAvailNodes or dst in availNodes:
                    continue
                diff = tFunc(items)
                if diff.bool == True and diff.difficulty <= maxDiff:
                    newAvailNodes.append(dst)
        return newAvailNodes

    # rootNode: starting AccessPoint instance
    # items: collected items
    # maxDiff: difficulty limit
    # return available AccessPoint list
    def getAvailableAccessPoints(self, rootNode, items, maxDiff):
        availNodes = [ rootNode ]
        newAvailNodes = availNodes
        while len(newAvailNodes) > 0:
            newAvailNodes = self.getNewAvailNodes(availNodes, newAvailNodes, items, maxDiff)
            availNodes += newAvailNodes
        return availNodes

    # locations: locations to check
    # items: collected items
    # maxDiff: difficulty limit
    # return available locations list
    def getAvailableLocations(self, locations, items, maxDiff):
        availAcessPoints = self.getAvailableAccessPoints(self.accessPoints['Landing Site'], items, maxDiff)
        availAreas = set([ap.GraphArea for ap in availAcessPoints])
        availLocs = []
        for loc in locations:
            if not loc['GraphArea'] in availAreas:
                continue
            for apName,tFunc in loc['AccessPoints'].iteritems():
                ap = self.accessPoints[apName]
                if not ap in availAcessPoints:
                    continue
                diff = tFunc(items)
                if diff.bool == True and diff.difficulty <= maxDiff:
                    diff = loc['Available'](items)
                    if diff.bool == True and diff.difficulty <= maxDiff:
                        availLocs.append(loc)
                        break
        return availLocs

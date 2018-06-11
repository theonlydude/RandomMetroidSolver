#!/usr/bin/python

import copy
from smbool import SMBool

class AccessPoint(object):
    # name : AccessPoint name
    # graphArea : graph area the node is located in
    # transitions : intra-area transitions
    # traverse: traverse function, will be wand to the added transitions
    # exitInfo : dict carrying vanilla door information : 'DoorPtr': door address, 'direction', 'cap', 'screen', 'bitFlag', 'distanceToSpawn', 'doorAsmPtr' : door properties
    # entryInfo : dict carrying forced samus X/Y position with keys 'SamusX' and 'SamusY'.
    #             (to be updated after reading vanillaTransitions and gather entry info from matching exit door)
    # roomInfo : dict with 'RoomPtr' : room address, 'area'
    # shortName : short name for the credits
    # internal : if true, shall not be used for connecting areas
    def __init__(self, name, graphArea, transitions,
                 traverse=lambda sm: sm.setSMBool(True),
                 exitInfo=None, entryInfo=None, roomInfo=None, shortName=None, internal=False):
        self.Name = name
        self.GraphArea = graphArea
        self.ExitInfo = exitInfo
        self.EntryInfo = entryInfo
        self.RoomInfo = roomInfo
        self.Internal = internal
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
        if self.Internal is False:
            self.transitions[destName] = lambda sm: self.traverse(sm)
        else:
            raise "Nope"

class AccessGraph(object):
    def __init__(self, accessPointList, transitions, bidir=True, dotFile=None):
        self.accessPoints = {}
        self.InterAreaTransitions = []
        self.bidir = bidir
        for ap in accessPointList:
            ap.distance = 0
            self.accessPoints[ap.Name] = ap
        for srcName, dstName in transitions:
            self.addTransition(srcName, dstName, bidir)
        if dotFile is not None:
            self.toDot(dotFile)

    def getCreditsTransitions(self):
        transitionsDict = {}
        for (src, dest) in self.InterAreaTransitions:
            transitionsDict[src.ShortName] = dest.ShortName

        transitions = []
        for accessPoint in ['C\\MUSHROOMS', 'C\\PIRATES', 'C\\MOAT', 'C\\KEYHUNTERS', 'C\\MORPH', 'B\\GREEN ELEV.',
                            'B\\GREEN HILL', 'B\\NOOB BRIDGE', 'W\\WEST OCEAN', 'W\\CRAB MAZE', 'N\\WAREHOUSE',
                            'N\\SINGLE CHAMBER', 'N\\KRONIC BOOST', 'LN\\LAVA DIVE', 'LN\\THREE MUSK.',
                            'M\\MAIN STREET', 'M\\CRAB HOLE', 'M\\COUDE', 'M\\RED FISH', 'B\\RED TOWER',
                            'B\\TOP RED TOWER', 'B\\RED ELEV.', 'B\\EAST TUNNEL', 'B\\TOP EAST TUNNEL',
                            'B\\GLASS TUNNEL', 'T\\STATUES']:
            if accessPoint in transitionsDict:
                src = accessPoint
                dst = transitionsDict[accessPoint]
                transitions.append((src, dst))
                del transitionsDict[src]
                del transitionsDict[dst]

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
            'Keyhunter Room Bottom': 'se',
            'Green Pirates Shaft Bottom Right': 'e',
            'Statues Hallway Left': 'w'
        }
        colors = ['red', 'blue', 'green', 'yellow', 'skyblue', 'violet', 'orange',
                  'lawngreen', 'crimson', 'chocolate', 'turquoise', 'tomato', 'navyblue', 'darkturquoise']
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
        availAccessPoints = self.getAvailableAccessPoints(self.accessPoints[rootNode], smbm, maxDiff)
        availAreas = set([ap.GraphArea for ap in availAccessPoints.keys()])
        availLocs = []
        for loc in locations:
            if not loc['GraphArea'] in availAreas:
                loc['distance'] = 10000
                loc['difficulty'] = SMBool(False, 0)
                continue
            for apName,tFunc in loc['AccessFrom'].iteritems():
                ap = self.accessPoints[apName]
                if not ap in availAccessPoints:
                    continue
                apDiff = availAccessPoints[ap]
                tdiff = smbm.eval(tFunc)
                if tdiff.bool == True and tdiff.difficulty <= maxDiff:
                    diff = smbm.eval(loc['Available'])
                    loc['difficulty'] = SMBool(diff.bool,
                                               difficulty=max(tdiff.difficulty, diff.difficulty, apDiff.difficulty),
                                               knows=list(set(tdiff.knows + diff.knows + apDiff.knows)),
                                               items=list(set(tdiff.items + diff.items + apDiff.items)))
                    if diff.bool == True and diff.difficulty <= maxDiff:
                        loc['distance'] = ap.distance + 1
                        loc['accessPoint'] = apName
                        availLocs.append(loc)
                        break
                else:
                    loc['distance'] = 1000 + tdiff.difficulty
                    loc['difficulty'] = SMBool(False, 0)
            if not 'difficulty' in loc:
                loc['distance'] = 10000
                loc['difficulty'] = SMBool(False, 0)

        return availLocs

    # test access from an access point to another, given an optional item
    def canAccess(self, smbm, srcAccessPointName, destAccessPointName, maxDiff, item=None):
        if item is not None:
            smbm.addItem(item)
        destAccessPoint = self.accessPoints[destAccessPointName]
        srcAccessPoint = self.accessPoints[srcAccessPointName]
        availAccessPoints = self.getAvailableAccessPoints(srcAccessPoint, smbm, maxDiff)
        can = destAccessPoint in availAccessPoints
#        print("canAccess: avail = " + str([ap.Name for ap in availAccessPoints.keys()]))
        if item is not None:
            smbm.removeItem(item)
        return can


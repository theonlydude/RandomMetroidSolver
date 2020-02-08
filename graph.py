import copy
from smbool import SMBool
from rom_patches import RomPatches
from parameters import infinity
import log

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
                 traverse=lambda sm: SMBool(True),
                 exitInfo=None, entryInfo=None, roomInfo=None,
                 internal=False, boss=False, escape=False,
                 start=None,
                 dotOrientation='w'):
        self.Name = name
        self.GraphArea = graphArea
        self.ExitInfo = exitInfo
        self.EntryInfo = entryInfo
        self.RoomInfo = roomInfo
        self.Internal = internal
        self.Boss = boss
        self.Escape = escape
        self.Start = start
        self.DotOrientation = dotOrientation
        self.transitions = transitions
        self.traverse = traverse
        self.distance = 0
        # inter-area connection
        self.ConnectedTo = None

    def __str__(self):
        return "[" + self.GraphArea + "] " + self.Name

    # connect to inter-area access point
    def connect(self, destName):
        if self.ConnectedTo is not None:
            del self.transitions[self.ConnectedTo]
        if self.Internal is False:
            self.transitions[destName] = lambda sm: self.traverse(sm)
            self.ConnectedTo = destName
        else:
            raise RuntimeError("Cannot add an internal access point as inter-are transition")

    # tells if this node is to connect areas together
    def isArea(self):
        return not self.Internal and not self.Boss and not self.Escape

    # used by the solver to get area and boss APs
    def isInternal(self):
        return self.Internal or self.Escape

class AccessGraph(object):
    def __init__(self, accessPointList, transitions, bidir=True, dotFile=None):
        self.log = log.get('Graph')

        self.accessPoints = {}
        self.InterAreaTransitions = []
        self.EscapeTimer = None
        self.bidir = bidir
        for ap in accessPointList:
            ap.distance = 0
            self.accessPoints[ap.Name] = ap
        for srcName, dstName in transitions:
            self.addTransition(srcName, dstName, bidir)
        if dotFile is not None:
            self.toDot(dotFile)

    def toDot(self, dotFile):
        colors = ['red', 'blue', 'green', 'yellow', 'skyblue', 'violet', 'orange',
                  'lawngreen', 'crimson', 'chocolate', 'turquoise', 'tomato',
                  'navyblue', 'darkturquoise', 'green', 'blue', 'maroon', 'magenta',
                  'bisque', 'coral', 'chartreuse', 'chocolate', 'cyan']
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
                f.write('%s:%s -> %s:%s [taillabel="%s",headlabel="%s",color=%s];\n' % (src.GraphArea, src.DotOrientation, dst.GraphArea, dst.DotOrientation, src.Name, dst.Name, colors[i]))
                drawn += [src.Name,dst.Name]
                i += 1
            f.write("}\n")

    def addTransition(self, srcName, dstName, both=True):
        src = self.accessPoints[srcName]
        dst = self.accessPoints[dstName]
        src.connect(dstName)
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
        for src in sorted(nodesToCheck, key=lambda x: x.Name):
            for dstName in sorted(src.transitions.keys()):
                tFunc = src.transitions[dstName]
                dst = self.accessPoints[dstName]
                if dst in newAvailNodes or dst in availNodes:
                    continue
                diff = smbm.eval(tFunc)
                if diff.bool == True and diff.difficulty <= maxDiff:
                    if src.GraphArea == dst.GraphArea:
                        dst.distance = src.distance + 0.01
                    else:
                        dst.distance = src.distance + 1
                    newAvailNodes[dst] = { 'difficulty' : diff, 'from' : src }

                #self.log.debug("{} -> {}: {}".format(src.Name, dstName, diff))
        return newAvailNodes

    # rootNode: starting AccessPoint instance
    # items: collected items
    # maxDiff: difficulty limit
    # return available AccessPoint list
    def getAvailableAccessPoints(self, rootNode, smbm, maxDiff):
        availNodes = { rootNode : { 'difficulty' : SMBool(True, 0), 'from' : None } }
        newAvailNodes = availNodes
        rootNode.distance = 0
        while len(newAvailNodes) > 0:
            newAvailNodes = self.getNewAvailNodes(availNodes, newAvailNodes, smbm, maxDiff)
            availNodes.update(newAvailNodes)

        return availNodes

    # gets path from the root AP used to compute availAps
    def getPath(self, dstAp, availAps):
        path = []
        root = dstAp
        while root != None:
            path = [root] + path
            root = availAps[root]['from']

        return path

    def getPathDifficulty(self, path, availAps):
        pdiff = SMBool(True, 0)
        for ap in path:
            diff = availAps[ap]['difficulty']
            pdiff = SMBool(True,
                           difficulty=max(pdiff.difficulty, diff.difficulty),
                           knows=list(set(pdiff.knows + diff.knows)),
                           items=pdiff.items + diff.items)

        return pdiff

    def getAvailAPPaths(self, availAccessPoints, locsAPs):
        paths = {}
        for ap in availAccessPoints:
            if ap.Name in locsAPs:
                path = self.getPath(ap, availAccessPoints)
                pdiff = self.getPathDifficulty(path, availAccessPoints)
                paths[ap.Name] = {"path": path, "pdiff": pdiff, "distance": len(path)}
        return paths

    def getSortedAPs(self, paths, locAccessFrom):
        ret = []

        for apName in locAccessFrom:
            if apName not in paths:
                continue
            difficulty = paths[apName]["pdiff"].difficulty
            ret.append((difficulty if difficulty != -1 else infinity, paths[apName]["distance"], apName))
        # sort by difficulty first, then distance
        ret.sort(key=lambda x: (x[0], x[1], x[2]))
        return [apName for (diff, dist, apName) in ret]

    # locations: locations to check
    # items: collected items
    # maxDiff: difficulty limit
    # rootNode: starting AccessPoint
    # return available locations list, also stores difficulty in locations
    def getAvailableLocations(self, locations, smbm, maxDiff, rootNode='Landing Site'):
        rootAp = self.accessPoints[rootNode]
        availAccessPoints = self.getAvailableAccessPoints(rootAp, smbm, maxDiff)
        availAreas = set([ap.GraphArea for ap in availAccessPoints.keys()])
        availLocs = []

        # get all the current locations APs first to only compute these paths
        locsAPs = set()
        for loc in locations:
            for ap in loc["AccessFrom"]:
                locsAPs.add(ap)

        # sort availAccessPoints based on difficulty to take easier paths first
        availAPPaths = self.getAvailAPPaths(availAccessPoints, locsAPs)

        for loc in locations:
            if loc['GraphArea'] not in availAreas:
                loc['distance'] = 30000
                loc['difficulty'] = SMBool(False)
                #if loc['Name'] == "Kraid":
                #    print("loc: {} locDiff is area nok".format(loc["Name"]))
                continue

            locAPs = self.getSortedAPs(availAPPaths, loc['AccessFrom'])
            if len(locAPs) == 0:
                loc['distance'] = 40000
                loc['difficulty'] = SMBool(False)
                #if loc['Name'] == "Kraid":
                #    print("loc: {} no aps".format(loc["Name"]))
                continue

            for apName in locAPs:
                if apName == None:
                    loc['distance'] = 20000
                    loc['difficulty'] = SMBool(False)
                    #if loc['Name'] == "Kraid":
                    #    print("loc: {} ap is none".format(loc["Name"]))
                    break

                tFunc = loc['AccessFrom'][apName]
                ap = self.accessPoints[apName]
                tdiff = smbm.eval(tFunc)
                #if loc['Name'] == "Kraid":
                #    print("{} root: {} ap: {}".format(loc['Name'], rootNode, apName))
                if tdiff.bool == True and tdiff.difficulty <= maxDiff:
                    diff = smbm.eval(loc['Available'])
                    path = availAPPaths[apName]["path"]
                    #if loc['Name'] == "Kraid":
                    #    print("{} path: {}".format(loc['Name'], [a.Name for a in path]))
                    pdiff = availAPPaths[apName]["pdiff"]
                    locDiff = SMBool(diff.bool,
                                     difficulty=max(tdiff.difficulty, diff.difficulty, pdiff.difficulty),
                                     knows=list(set(tdiff.knows + diff.knows + pdiff.knows)),
                                     items=tdiff.items + diff.items + pdiff.items)
                    if locDiff.bool == True and locDiff.difficulty <= maxDiff:
                        loc['distance'] = ap.distance + 1
                        loc['accessPoint'] = apName
                        loc['difficulty'] = locDiff
                        loc['path'] = path
                        availLocs.append(loc)
                        #if loc['Name'] == "Kraid":
                        #    print("{} diff: {} tdiff: {} pdiff: {}".format(loc['Name'], diff, tdiff, pdiff))
                        break
                    else:
                        loc['distance'] = 1000 + tdiff.difficulty
                        loc['difficulty'] = SMBool(False)
                        #if loc['Name'] == "Kraid":
                        #    print("loc: {} locDiff is false".format(loc["Name"]))
                else:
                    loc['distance'] = 10000 + tdiff.difficulty
                    loc['difficulty'] = SMBool(False)
                    #if loc['Name'] == "Kraid":
                    #    print("loc: {} tdiff is false".format(loc["Name"]))

            if 'difficulty' not in loc:
                #if loc['Name'] == "Kraid":
                #    print("loc: {} no difficulty in loc".format(loc["Name"]))
                loc['distance'] = 100000
                loc['difficulty'] = SMBool(False)

            #if loc['Name'] == "Kraid":
            #    print("loc: {}: {}".format(loc['Name'], loc))

        #print("availableLocs: {}".format([loc["Name"] for loc in availLocs]))
        return availLocs

    # test access from an access point to another, given an optional item
    def canAccess(self, smbm, srcAccessPointName, destAccessPointName, maxDiff, item=None):
        if item is not None:
            smbm.addItem(item)
        #print("canAccess: item: {}, src: {}, dest: {}".format(item, srcAccessPointName, destAccessPointName))
        destAccessPoint = self.accessPoints[destAccessPointName]
        srcAccessPoint = self.accessPoints[srcAccessPointName]
        availAccessPoints = self.getAvailableAccessPoints(srcAccessPoint, smbm, maxDiff)
        can = destAccessPoint in availAccessPoints
        #self.log.debug("canAccess: avail = {}".format([ap.Name for ap in availAccessPoints.keys()]))
        if item is not None:
            smbm.removeItem(item)
        #print("canAccess: {}".format(can))
        return can

    # returns a list of AccessPoint instances from srcAccessPointName to destAccessPointName
    # (not including source ap)
    # or None if no possible path
    def accessPath(self, smbm, srcAccessPointName, destAccessPointName, maxDiff):
        destAccessPoint = self.accessPoints[destAccessPointName]
        srcAccessPoint = self.accessPoints[srcAccessPointName]
        availAccessPoints = self.getAvailableAccessPoints(srcAccessPoint, smbm, maxDiff)
        if destAccessPoint not in availAccessPoints:
            return None
        return self.getPath(destAccessPoint, availAccessPoints)

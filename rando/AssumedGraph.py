import logging, utils
from collections import defaultdict
from utils.utils import removeChars

class Node(object):
    def __init__(self, data, attributes, type):
        self.data = data
        self.attributes = attributes
        self.neighbours = defaultdict(list)
        # item or location
        self.type = type

    def isItem(self):
        return self.type == 'item'

    def isLocation(self):
        return self.type == 'location'

    def addEdge(self, type, neighbour):
        self.neighbours[type].append(neighbour)

    def removeEdge(self, type, neighbour):
        self.neighbours[type].remove(neighbour)

    # need to remove edge in neighbours too
    #def resetEdges(self, type):
    #    self.neighbour[type] = []

    # need to remove edge in neighbours too
    #def replaceEdges(self, type, neighbours):
    #    self.neighbours[type] = neighbours

    def hasEdge(self, type):
        return len(self.neighbours[type]) > 0

    def getNeighbours(self, type):
        return self.neighbours[type]

    def hasNeighbour(self, type, neighbourNode):
        return neighbourNode in self.neighbours[type]

class AssumedGraph(object):
    def __init__(self, validItems):
        self.items = {}
        self.locations = {}
        self.validItems = validItems
        # we have different kind of edges between items and locs:
        # pv: valid item can be place at loc
        # pi: invalid item can be place at loc
        # u: loc unavailable without item
        # b: nolongeravaillocswoitem locs of item where all its possible locations are unavailable without both items (bv the associated valid item)
        # ov: one loc valid item unavailable without both items (o for the other item)
        # c: loc unavailable without two count items
        # n: loc post unavailable without item
        self.priorities = {'u': 1, 'c': 1, 'n': 1, 'ov': 25, 'o': 0, 'pv': 0, 'pi': 0, 'b': 25, 'bv': 0}
        self.log = utils.log.get('AssumedGraph')

    def toDot(self, step):
        colors = {'u': "red", 'c': "yellow", 'n': "cyan", 'b': "green", 'bv': "gold", 'pv': "pink", 'pi': "orange", 'o': "darkgreen", 'ov': "khaki"}

        with open("step{:02d}.dot".format(step), 'w') as f:
            f.write("digraph D {\n")
            f.write("splines=\"line\"\n")

            # add locations
            for loc, locNode in self.locations.items():
                locNode.graphName = removeChars(loc.Name, ' ,()-')+"loc"
                f.write("{} [shape=circle label=\"{} ({})\"]\n".format(locNode.graphName, locNode.data.Name, locNode.attributes['priority']))
                for type, neighbours in locNode.neighbours.items():
                    #if type in ['pv', 'pi']:
                    if type in ['pi']:
                        continue
                    if type in ['u', 'pv', 'pi']:
                        f.write("{} -> {{{}}} [color=\"{}\"]\n".format(locNode.graphName, ', '.join([itemNode.data.Type for itemNode in neighbours]), colors[type]))
                    else:
                        f.write("{} -> {{{}}} [color=\"{}\" label=\"{}\"]\n".format(locNode.graphName, ', '.join([itemNode.data.Type for itemNode in neighbours]), colors[type], type))

            # add items
            for item, itemNode in self.items.items():
                f.write("{} [shape=box color=\"{}\"]\n".format(item.Type, "green" if item in self.validItems else "black"))
                for type, neighbours in itemNode.neighbours.items():
                    #if type in ['pv', 'pi']:
                    if type in ['pi']:
                        continue
                    if type in ['u', 'pv', 'pi']:
                        f.write("{} -> {{{}}} [color=\"{}\"]\n".format(item.Type, ', '.join([locNode.graphName for locNode in neighbours]), colors[type]))
                    else:
                        f.write("{} -> {{{}}} [color=\"{}\" label=\"{}\"]\n".format(item.Type, ', '.join([locNode.graphName for locNode in neighbours]), colors[type], type))

            # add ranks
            f.write("{{ rank=same {} }}\n".format(" ".join([locNode.graphName for locNode in self.locations.values()])))
            f.write("{{ rank=same {} }}\n".format(" ".join([item.Type for item in self.items.keys()])))

            f.write("}")

    def getLocNeighbours(self, loc, type):
        return [itemNode.data for itemNode in self.locations[loc].getNeighbours(type)]

    def getItemNeighbours(self, item, type):
        return [locNode.data for locNode in self.items[item].getNeighbours(type)]

    def addItem(self, item, isValid):
        node = Node(item, {'isValid': isValid}, 'item')
        self.items[item] = node

    def addLocation(self, location):
        node = Node(location, {'priority': 0}, 'location')
        self.locations[location] = node

    def addEdge(self, item, location, type):
        itemNode = self.items[item]
        locationNode =  self.locations[location]

        self.addEdgeNode(itemNode, locationNode, type)

    def addEdgeNode(self, itemNode, locationNode, type):
        itemNode.addEdge(type, locationNode)
        locationNode.addEdge(type, itemNode)

        # update priority as we add edges
        locationNode.attributes['priority'] += self.priorities[type]

    def removeEdge(self, item, location, type):
        itemNode = self.items[item]
        locationNode =  self.locations[location]

        self.removeEdgeNode(itemNode, locationNode, type)

    def removeEdgeNode(self, node1, node2, type):
        node1.removeEdge(type, node2)
        node2.removeEdge(type, node1)

        # update priority
        if node1.isLocation():
            node1.attributes['priority'] -= self.priorities[type]
        elif node2.isLocation():
            node2.attributes['priority'] -= self.priorities[type]

    def removeNodeEdges(self, node, type):
        neighbours = node.getNeighbours(type)[:]
        for neighbour in neighbours:
            self.removeEdgeNode(node, neighbour, type)

    def build(self, itemLocDict, container):
        # add items and locs to the graph
        for it in itemLocDict.keys():
            self.addItem(it, isValid=it in self.validItems)
        for loc in container.unusedLocations:
            self.addLocation(loc)

        for it, data in itemLocDict.items():
            for loc in data['noLongerAvailLocsWoItem']:
                self.addEdge(it, loc, type='u')
            for loc in data['locsNokWoDoubleItem']:
                self.addEdge(it, loc, type='c')
            for loc in data['locsPostNokWoItem']:
                self.addEdge(it, loc, type='n')
            if it in self.validItems:
                for loc in data['possibleLocs']:
                    self.addEdge(it, loc, type='pv')
            else:
                for loc in data['possibleLocs']:
                    self.addEdge(it, loc, type='pi')
            oneLocItem = it
            for item, locations in data['oneLocNokWoBothItems'].items():
                for loc in locations:
                    # one loc valid item
                    self.addEdge(oneLocItem, loc, type='ov')
                    # the associated item making the one loc non valid for oneLocItem
                    self.addEdge(item, loc, type='o')
#            for validItem, locations in data['locsNokWoBothItems'].items():
#                # priorize it nolongeravaillocswoitem locs
#                for loc in locations:
#                    # 'it' those possible locs will become unavailable without 'it' and associated validItem.
#                    # the locations are the nolongeravaillocswoitem of 'it'
#                    self.addEdge(it, loc, type='b')
#                    self.log.debug("b {} -> {}".format(it.Type, loc.Name))
#                    # the associated valid item
#                    self.addEdge(validItem, loc, type='bv')
#                    self.log.debug("bv {} -> {}".format(validItem.Type, loc.Name))

        self.handleItemsWithOnePossibleLoc()
        self.preventLostLoc('n')
        self.preventLostLoc('c')

    def getLocNodesWithEdge(self, type):
        ret = []
        for loc, locNode in self.locations.items():
            if locNode.hasEdge(type):
                ret.append(locNode)
        return ret

    def preventLostLoc(self, type):
        # instead of increasing the priority of type locations, prevent associated items to be placed in other locs.
        locsAtRisk = self.getLocNodesWithEdge(type)
        for locNode in locsAtRisk:
            itemsNodes = locNode.getNeighbours(type)
            for itemNode in itemsNodes:
                if itemNode.attributes['isValid']:
                    if itemNode.hasNeighbour('pv', locNode):
                        self.log.debug("preventLostLoc loc {} allow item {} in it".format(locNode.data.Name, itemNode.data.Type))
                        self.removeNodeEdges(itemNode, 'pv')
                        self.addEdgeNode(itemNode, locNode, 'pv')
                    else:
                        self.log.debug("preventLostLoc loc {} disable item {}".format(locNode.data.Name, itemNode.data.Type))
                        self.removeNodeEdges(itemNode, 'pv')

    def getLocationsItems(self):
        locationsPriorities = defaultdict(list)
        for loc, locNode in self.locations.items():
            locationsPriorities[locNode.attributes['priority']].append(loc)
        priorities = set(list(locationsPriorities.keys()))

        while priorities:
            maxPriority = max(priorities)
            priorityLocations = locationsPriorities[maxPriority]
            self.log.debug("max priority: {} unfiltered locs: {}".format(maxPriority, [loc.Name for loc in priorityLocations]))
            # keep only locs with at least one valid item
            locItemDict = {loc: set(self.getLocNeighbours(loc, 'pv')) for loc in priorityLocations}
            removedLocs = [loc for loc, items in locItemDict.items() if not items]
            locItemDict = {loc: items for loc, items in locItemDict.items() if items}

            # if some locs have been filtered replace with the noLongerAvailLocsWoItem of the items
            # linked to these locs (it means that they are of higher priority).
            if removedLocs:
                newPrioLocs = self.getMorePriorityLocs(removedLocs)
                if newPrioLocs:
                    self.log.debug("new priority locs from filtered locs: {}".format([loc.Name for loc in newPrioLocs]))
                    locItemDict = newPrioLocs

            if not locItemDict:
                priorities.remove(maxPriority)
            else:
                # check in the locs if some have only one possible item, if so keep only these locs
                filteredLocItemDict = {loc: items for loc, items in locItemDict.items() if len(items) == 1}
                if filteredLocItemDict:
                    self.log.debug("filter to keep only locs with one possible item")
                    return filteredLocItemDict
                else:
                    return locItemDict
        return {}

    def getMorePriorityLocs(self, removedLocs):
        newPrioLocs = {}
        self.log.debug("removed locs: {}".format([loc.Name for loc in removedLocs]))
        for rloc in removedLocs:
            # possible invalid items for the removed loc
            ritems = self.getLocNeighbours(rloc, 'pi')
            self.log.debug("invalid items of rloc {}: {}".format(rloc.Name, [it.Type for it in ritems]))
            for ritem in ritems:
                # no longer avail locs wo invalid item
                noLongerAvailLocsWoItem = self.getItemNeighbours(ritem, 'u')
                self.log.debug("item: {} nolongeravaillocswoitem: {}".format(ritem.Type, [loc.Name for loc in noLongerAvailLocsWoItem]))
                for loc in noLongerAvailLocsWoItem:
                    # valid items for the loc
                    items = set(self.getLocNeighbours(loc, 'pv'))
                    if items:
                        newPrioLocs[loc] = items
        return newPrioLocs

    def handleItemsWithOnePossibleLoc(self):
        # if an item has only one possible loc, remove other 'pv' edges to that loc to prevent
        # having an item with no possible loc.
        # also do that for pi edges to avoid filing a loc which will be the only possible one for
        # an item when its dependent locs get filled.
        for item, itemNode in self.items.items():
            pvLocsNodes = itemNode.getNeighbours('pv')
            piLocsNodes = itemNode.getNeighbours('pi')
            if len(pvLocsNodes) == 1:
                locNode = pvLocsNodes[0]
                self.removeNodeEdges(locNode, 'pv')
                self.addEdgeNode(itemNode, locNode, 'pv')
                self.log.debug("one loc valid item {}, set it as only possible items for loc {}".format(item.Type, locNode.data.Name))
            if len(piLocsNodes) == 1:
                locNode = piLocsNodes[0]
                self.removeNodeEdges(locNode, 'pv')
                self.log.debug("one loc invalid item {}, remove all possible items for loc {}".format(item.Type, locNode.data.Name))

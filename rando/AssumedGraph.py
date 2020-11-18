import logging, utils
from collections import defaultdict
from utils.utils import removeChars

class Node(object):
    def __init__(self, data, attributes):
        self.data = data
        self.attributes = attributes
        self.neighbours = defaultdict(list)

    def addEdge(self, type, neighbour):
        self.neighbours[type].append(neighbour)

class AssumedGraph(object):
    def __init__(self, validItems):
        self.items = {}
        self.locations = {}
        self.validItems = validItems
        # we have different kind of edges between items and locs:
        # pv: valid item can be place at loc
        # pi: invalid item can be place at loc
        # u: loc unavailable without item
        # b: loc unavailable without both items
        # c: loc unavailable without two count items
        # n: loc post unavailable without item
        self.priorities = {'u': 1, 'c': 50, 'n': 100, 'b': 75, 'pv': 0, 'pi': 0}
        self.log = utils.log.get('AssumedGraph')

    def toDot(self, step):
        colors = {'u': "red", 'c': "yellow", 'n': "cyan", 'b': "green", 'pv': "pink", 'pi': "orange"}

        with open("step{:02d}.dot".format(step), 'w') as f:
            f.write("digraph D {\n")
            f.write("splines=\"line\"\n")

            # add locations
            for loc, locNode in self.locations.items():
                locNode.graphName = removeChars(loc.Name, ' ,()-')+"loc"
                f.write("{} [shape=circle label=\"{} ({})\"]\n".format(locNode.graphName, locNode.data.Name, locNode.attributes['priority']))
                for type, neighbours in locNode.neighbours.items():
                    if type in ['pv', 'pi']:
                        continue
                    f.write("{} -> {{{}}} [color=\"{}\"]\n".format(locNode.graphName, ', '.join([itemNode.data.Type for itemNode in neighbours]), colors[type]))

            # add items
            for item, itemNode in self.items.items():
                f.write("{} [shape=box color=\"{}\"]\n".format(item.Type, "green" if item in self.validItems else "black"))
                for type, neighbours in itemNode.neighbours.items():
                    if type in ['pv', 'pi']:
                        continue
                    f.write("{} -> {{{}}} [color=\"{}\"]\n".format(item.Type, ', '.join([locNode.graphName for locNode in neighbours]), colors[type]))

            # add ranks
            f.write("{{ rank=same {} }}\n".format(" ".join([locNode.graphName for locNode in self.locations.values()])))
            f.write("{{ rank=same {} }}\n".format(" ".join([item.Type for item in self.items.keys()])))

            f.write("}")

    def getLocNeighbours(self, loc, type):
        return [itemNode.data for itemNode in self.locations[loc].neighbours[type]]

    def getItemNeighbours(self, item, type):
        return [locNode.data for locNode in self.items[item].neighbours[type]]

    def addItem(self, item, isValid):
        node = Node(item, {'isValid': isValid})
        self.items[item] = node

    def addLocation(self, location):
        node = Node(location, {'priority': 0})
        self.locations[location] = node

    def addEdge(self, item, location, type):
        itemNode = self.items[item]
        locationNode =  self.locations[location]

        itemNode.addEdge(type, locationNode)
        locationNode.addEdge(type, itemNode)

        # update priority as we add edges
        locationNode.attributes['priority'] += self.priorities[type]

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
            if 'locsNokWoBothItems' in data:
                for loc in data['locsNokWoBothItems']:
                    self.addEdge(it, loc, type='b')

        self.handleItemsWithOnePossibleLoc()

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
            pvLocsNodes = itemNode.neighbours['pv']
            piLocsNodes = itemNode.neighbours['pi']
            if len(pvLocsNodes) == 1:
                locNode = pvLocsNodes[0]
                locNode.neighbours['pv'] = [itemNode]
                self.log.debug("one loc valid item {}, set it as only possible items for loc {}".format(item.Type, locNode.data.Name))
            if len(piLocsNodes) == 1:
                locNode = piLocsNodes[0]
                locNode.neighbours['pv'] = []
                self.log.debug("one loc invalid item {}, remove all possible items for loc {}".format(item.Type, locNode.data.Name))

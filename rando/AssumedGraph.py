import logging, utils
from collections import defaultdict

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
        # p: item can be place at loc
        # u: loc unavailable without item
        # b: loc unavailable without both items
        # c: loc unavailable without two count items
        # n: loc post unavailable without item
        self.priorities = {'u': 1, 'c': 100, 'n': 100, 'b': 100, 'p': 0}
        self.log = utils.log.get('AssumedGraph')

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
                    self.addEdge(it, loc, type='p')
            if 'locsNokWoBothItems' in data:
                for loc in data['locsNokWoBothItems']:
                    self.addEdge(it, loc, type='b')

        self.handleItemsWithOnePossibleLoc()

    def getLocationsItems(self):
        locationsPriorities = defaultdict(list)
        for loc, locNode in self.locations.items():
            locationsPriorities[locNode.attributes['priority']].append(loc)
        maxPriority = -1
        for priority in locationsPriorities:
            if priority > maxPriority:
                maxPriority = priority
        priorityLocations = locationsPriorities[maxPriority]
        self.log.debug("max priority: {} locs: {}".format(maxPriority, [loc.Name for loc in priorityLocations]))
        # keep only locs with at least one valid item
        locItemDict = {loc: set([itemNode.data for itemNode in self.locations[loc].neighbours['p']]).intersection(self.validItems) for loc in priorityLocations}
        return {loc: items for loc, items in locItemDict.items() if len(items) > 0}

    def handleItemsWithOnePossibleLoc(self):
        # if an item has only one possible loc, remove other 'p' edges to that loc to prevent
        # having an item with no possible loc.
        for item, itemNode in self.items.items():
            if len(itemNode.neighbours['p']) == 1:
                locNode = itemNode.neighbours['p'][0]
                locNode.neighbours['p'] = [itemNode]
                self.log.debug("one loc item {}, remove other possible items for loc {}".format(item.Type, locNode.data.Name))

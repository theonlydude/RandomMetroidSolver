import copy, random, utils.log

from graph.graph_access import getAccessPoint
from rando.ItemLocContainer import getLocListStr

# Holds settings related to item placement restrictions.
# canPlaceAtLocation is the main entry point here
class Restrictions(object):
    def __init__(self, settings):
        self.log = utils.log.get('Restrictions')
        self.settings = settings
        # Item split : Major, Chozo or Full
        self.split = settings.restrictions['MajorMinor']
        self.suitsRestrictions = settings.restrictions['Suits']
        # checker function chain used by canPlaceAtLocation
        self.checkers = self.getCheckers()
        self.static = {}
        self.dynamic = {}

    def disable(self):
        self.split = "Full"
        self.suitsRestrictions = False
        self.checkers = []

    def isEarlyMorph(self):
        return self.settings.restrictions['Morph'] == 'early'

    def isLateMorph(self):
        return self.settings.restrictions['Morph'] == 'late'

    def isLateAmmo(self):
        return self.settings.restrictions['ammo'] == 'late'

    def isChozo(self):
        return self.split == 'Chozo'

    def lateMorphInit(self, ap, emptyContainer, services):
        assert self.isLateMorph()
        morph = emptyContainer.getNextItemInPool('Morph')
        assert morph is not None
        locs = services.possibleLocations(morph, ap, emptyContainer, bossesKilled=False)
        self.lateMorphLimit = len(locs)
        self.log.debug('lateMorphInit. {} locs: {}'.format(self.lateMorphLimit, getLocListStr(locs)))
        areas = {}
        for loc in locs:
            areas[loc.GraphArea] = areas.get(loc.GraphArea, 0) + 1
        self.log.debug('lateMorphLimit. areas: {}'.format(areas))
        if len(areas) > 1:
            self.lateMorphForbiddenArea = getAccessPoint(ap).GraphArea
            self.log.debug('lateMorphLimit. forbid start area: {}'.format(self.lateMorphForbiddenArea))
        else:
            self.lateMorphForbiddenArea = None

    NoCheckCat = set(['Energy', 'Nothing', 'Boss'])

    def addPlacementRestrictions(self, restrictionDict):
        self.log.debug("add speedrun placement restrictions")
#        self.log.debug(restrictionDict)
        self.checkers.append(lambda item, loc, cont:
                             item.Category in Restrictions.NoCheckCat
                             or item.Type == 'Missile'
                             or (item.Category == 'Ammo' and cont.hasUnrestrictedLocWithItemType(item.Type))
                             or loc.GraphArea not in restrictionDict
                             or item.Type not in restrictionDict[loc.GraphArea]
                             or loc.Name in restrictionDict[loc.GraphArea][item.Type])

    def isLocMajor(self, loc):
        return not loc.isBoss() and (self.split == "Full" or loc.isClass(self.split))

    def isLocMinor(self, loc):
        return not loc.isBoss() and (self.split == "Full" or not loc.isClass(self.split))

    def isItemMajor(self, item):
        if self.split == "Full":
            return True
        else:
            return item.Class == self.split

    def isItemMinor(self, item):
        if self.split == "Full":
            return True
        else:
            return item.Class == "Minor"

    def isItemLocMatching(self, item, loc):
        if self.split == "Full":
            return True
        if loc.isClass(self.split):
            return item.Class == self.split
        else:
            return item.Class == "Minor"

    # return True if we can keep morph as a possibility
    def lateMorphCheck(self, container, possibleLocs):
        # the closer we get to the limit the higher the chances of allowing morph
        proba = random.randint(0, self.lateMorphLimit)
        if self.split == 'Full':
            nbItems = len(container.currentItems)
        else:
            nbItems = len([item for item in container.currentItems if self.split == item.Class])
        if proba > nbItems:
            return None
        if self.lateMorphForbiddenArea is not None:
            morphLocs = [loc for loc in possibleLocs if loc.GraphArea != self.lateMorphForbiddenArea]
            forbidden = len(morphLocs) == 0
            possibleLocs = morphLocs if not forbidden else None
        return possibleLocs

    def isSuit(self, item):
        return item.Type == 'Varia' or item.Type == 'Gravity'
    
    def getCheckers(self):
        checkers = []
        self.log.debug("add bosses restriction")
        checkers.append(lambda item, loc, cont: (item.Category != 'Boss' and not loc.isBoss()) or (item.Category == 'Boss' and item.Name == loc.Name))
        if self.split != 'Full':
            self.log.debug("add majorsSplit restriction")
            checkers.append(lambda item, loc, cont: self.isItemLocMatching(item, loc))
        if self.suitsRestrictions:
            self.log.debug("add suits restriction")
            checkers.append(lambda item, loc, cont: not self.isSuit(item) or loc.GraphArea != 'Crateria')
        return checkers

    # return bool telling whether we can place a given item at a given location
    def canPlaceAtLocation(self, item, location, container):
        ret = True
        for chk in self.checkers:
            ret = ret and chk(item, location, container)
            if not ret:
                break

        return ret

    ### Below : faster implementation tailored for random fill

    def precomputeRestrictions(self, container):
        # precompute the values for canPlaceAtLocation. only for random filler.
        # dict (loc name, item type) -> bool
        items = container.getDistinctItems()
        for item in items:
            for location in container.unusedLocations:
                self.static[(location.Name, item.Type)] = self.canPlaceAtLocation(item, location, container)

        container.unrestrictedItems = set(['Super', 'PowerBomb'])
        for item in items:
            if item.Type not in ['Super', 'PowerBomb']:
                continue
            for location in container.unusedLocations:
                self.dynamic[(location.Name, item.Type)] = self.canPlaceAtLocation(item, location, container)
        container.unrestrictedItems = set()

    def canPlaceAtLocationFast(self, itemType, locName, container):
        if itemType in ['Super', 'PowerBomb'] and container.hasUnrestrictedLocWithItemType(itemType):
            return self.dynamic.get((locName, itemType))
        else:
            return self.static.get((locName, itemType))

import copy, random, log

from graph_access import getAccessPoint
from rando.ItemLocContainer import getLocListStr

class Restrictions(object):
    def __init__(self, settings):
        self.settings = settings
        self.split = settings.restrictions['MajorMinor']
        self.suitsRestrictions = settings.restrictions['Suits']
        self.checkers = self.getCheckers()
        self.log = log.get("Restrictions")

    def isEarlyMorph(self):
        return self.settings.restrictions['Morph'] == 'early'

    def isLateMorph(self):
        return self.settings.restrictions['Morph'] == 'late'

    def lateMorphInit(self, ap, emptyContainer, services):
        assert self.isLateMorph()
        locs = services.possibleLocations('Morph', ap, emptyContainer)
        if self.split != 'Full':
            locs = [loc for loc in locs if self.split in loc['Class']]
        self.log.debug('lateMorphInit. locs='+getLocListStr(locs))
        self.lateMorphLimit = len(locs)
        if len(set([loc['GraphArea'] for loc in locs])) > 1:
            self.lateMorphForbiddenArea = getAccessPoint(ap).GraphArea
        else:
            self.lateMorphForbiddenArea = None

    def addPlacementeRestrictions(self, restrictionDict):
        self.checkers.append(lambda item, loc, cont: item['Type'] not in restrictionDict or (item['Category'] == 'Ammo' and cont.hasUnrestrictedLocWithItemType(item['Type'])) or any(l['Name'] == loc['Name'] for l in restrictionDict[item['Type']]))

    def isLocMajor(self, loc):
        return 'Boss' not in loc['Class'] and (self.split == "Full" or self.split in loc['Class'])

    def isLocMinor(self, loc):
        return 'Boss' not in loc['Class'] and (self.split == "Full" or self.split not in loc['Class'])

    def isItemMajor(self, item):
        if self.split == "Full":
            return True
        else:
            return item['Class'] == self.split

    def isItemMinor(self, item):
        if self.split == "Full":
            return True
        else:
            return item['Class'] == "Minor"

    def isItemLocMatching(self, item, loc):
        if self.split == "Full":
            return True
        if self.split in loc['Class']:
            return item['Class'] == self.split
        else:
            return item['Class'] == "Minor"

    # return True if we can keep morph as a possibility
    def lateMorphCheck(self, container):
        # the closer we get to the limit the higher the chances of allowing morph
        proba = random.randint(0, self.lateMorphLimit)
        if self.split == 'Full':
            nbItems = len(container.currentItems)
        else:
            nbItems = len([item for item in container.currentItems if self.split == item['Class']])
        return proba <= nbItems

    def isSuit(self, item):
        return item['Type'] == 'Varia' or item['Type'] == 'Gravity'
    
    def getCheckers(self):
        checkers = []
        checkers.append(lambda item, loc, cont: (item['Category'] != 'Boss' and 'Boss' not in loc['Class']) or (item['Category'] == 'Boss' and item['Name'] == loc['Name']))
        if self.split != 'Full':
            checkers.append(lambda item, loc, cont: self.isItemLocMatching(item, loc))
        if self.suitsRestrictions:
            checkers.append(lambda item, loc, cont: not self.isSuit(item) or loc['GraphArea'] != 'Crateroa')
        return checkers

    def canPlaceAtLocation(self, item, location, container):
        ret = True
        for chk in self.checkers:
            ret = ret and chk(item, location, container)
            if not ret:
                break
        return ret

        # # plando locs are not available
        # if 'itemName' in location:
        #     return False

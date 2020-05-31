
import sys
from rando.Items import ItemManager

class RandoSettings(object):
    def __init__(self, maxDiff, progSpeed, progDiff, qty, restrictions,
                 superFun, runtimeLimit_s, plandoRandoItemLocs):
        self.progSpeed = progSpeed
        self.progDiff = progDiff.lower()
        self.maxDiff = maxDiff
        self.qty = qty
        self.restrictions = restrictions
        self.superFun = superFun
        self.runtimeLimit_s = runtimeLimit_s
        if self.runtimeLimit_s <= 0:
            self.runtimeLimit_s = sys.maxsize
        self.plandoRandoItemLocs = plandoRandoItemLocs

    def getItemManager(self, smbm):
        if self.plandoRandoItemLocs is None:
            return ItemManager(self.restrictions['MajorMinor'], self.qty, smbm)
        else:
            return ItemManager('Plando', self.qty, self.smbm)

    def getExcludeItems(self, locations):
        if self.plandoRandoItemLocs is None:
            return None
        exclude = {'total':0}
        # plandoRando is a dict {'loc name': 'item type'}
        for locName,itemType in self.plandoRandoItemLocs.items():
            if not any(loc['Name'] == locName for loc in locations):
                continue
            if itemType not in exclude:
                exclude[itemType] = 0
            exclude[itemType] += 1
            exclude['total'] += 1

        return exclude

    def collectAlreadyPlacedItemLocations(self, container):
        if self.plandoRandoItemLocs is None:
            return
        for locName,itemType in self.plandoRandoItemLocs.items():
            if not any(loc['Name'] == locName for loc in container.unusedLocations):
                continue
            item = container.getNextItemInPool(itemType)
            assert item is not None, "Invalid plando item pool"
            location = container.getLocs(lambda loc: loc['Name'] == locName)[0]
            itemLoc = {'Item':item, 'Location':location}
            container.collect(itemLoc, pickup=False)

class GraphSettings(object):
    def __init__(self, startAP, areaRando, bossRando, escapeRando, dotFile, plandoRandoTransitions):
        self.bidir = True
        self.startAP = startAP
        self.areaRando = areaRando
        self.bossRando = bossRando
        self.escapeRando = escapeRando
        self.dotFile = dotFile
        self.plandoRandoTransitions = plandoRandoTransitions

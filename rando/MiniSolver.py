
import log, random

from smboolmanager import SMBoolManager
from parameters import infinity

class MiniSolver(object):
    def __init__(self, startAP, areaGraph, restrictions):
        self.startAP = startAP
        self.areaGraph = areaGraph
        self.restrictions = restrictions
        self.settings = restrictions.settings
        self.smbm = SMBoolManager()
        self.log = log.get('MiniSolver')

    # if True, does not mean it is actually beatable, unless you're sure of it from another source of information
    # if False, it is certain it is not beatable
    def isBeatable(self, itemLocations, maxDiff=None):
        if maxDiff is None:
            maxDiff = self.settings.maxDiff
        locations = []
        for il in itemLocations:
            loc = il['Location']
            if loc.get('restricted') == True:
                continue
            loc['itemType'] = il['Item']['Type']
            loc['difficulty'] = None
            locations.append(loc)
        self.smbm.resetItems()
        ap = self.startAP
        onlyBossesLeft = -1
        while True:
            if not locations:
                return True
            # only two loops to collect all remaining locations in only bosses left mode
            if onlyBossesLeft > 0:
                onlyBossesLeft += 1
                if onlyBossesLeft > 2:
                    return False
            self.areaGraph.getAvailableLocations(locations, self.smbm, maxDiff, ap)
            post = [loc for loc in locations if 'PostAvailable' in loc and loc['difficulty'].bool == True]
            for loc in post:
                self.smbm.addItem(loc['itemType'])
                postAvailable = loc['PostAvailable'](self.smbm)
                self.smbm.removeItem(loc['itemType'])
                loc['difficulty'] = self.smbm.wand(loc['difficulty'], postAvailable)
            toCollect = [loc for loc in locations if loc['difficulty'].bool == True and loc['difficulty'].difficulty <= maxDiff]
            if not toCollect:
                # mini onlyBossesLeft
                if maxDiff < infinity:
                    maxDiff = infinity
                    onlyBossesLeft = 0
                    continue
                return False
            self.smbm.addItems([loc['itemType'] for loc in toCollect])
            for loc in toCollect:
                locations.remove(loc)
            # if len(locations) > 0:
            #     ap = random.choice([loc['accessPoint'] for loc in locations])

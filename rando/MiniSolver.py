
import log, random

from smboolmanager import SMBoolManager

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
            if 'restricted' in loc and loc['restricted'] == True:
                continue
            loc['itemType'] = il['Item']['Type']
            loc['difficulty'] = None
            locations.append(loc)
        self.smbm.resetItems()
        ap = self.startAP
        while True:
            if not locations:
                return True
            self.areaGraph.getAvailableLocations(locations, self.smbm, maxDiff, ap)
            toCollect = [loc for loc in locations if loc['difficulty'].bool == True and loc['difficulty'].difficulty <= maxDiff]
            if not toCollect:
                return False
            self.smbm.addItems([loc['itemType'] for loc in toCollect])
            for loc in toCollect:
                locations.remove(loc)
            # if len(locations) > 0:
            #     ap = random.choice([loc['accessPoint'] for loc in locations])

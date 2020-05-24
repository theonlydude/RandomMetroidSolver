
import log

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
            loc['itemType'] = il['Item']['Type']
            loc['difficulty'] = None
            locations.append(loc)
        self.smbm.resetItems()
        while True:
            if len(locations) == 0:
                return True
            self.areaGraph.getAvailableLocations(locations, self.smbm, maxDiff, self.startAP)
            for loc in locations:
                if loc['difficulty'].bool == True:
                    if 'PostAvailable' in loc:
                        self.smbm.addItem(loc['itemType'])
                        postAvailable = loc['PostAvailable'](self.smbm)
                        self.smbm.removeItem(loc['itemType'])
                        loc['difficulty'] = self.smbm.wand(loc['difficulty'], postAvailable)
            toCollect = [loc for loc in locations if loc['difficulty'].bool == True and loc['difficulty'].difficulty <= maxDiff]
            if len(toCollect) == 0:
                return False
            for loc in toCollect:
                self.smbm.addItem(loc['itemType'])
            locations = [loc for loc in locations if loc['difficulty'].bool == False or loc['difficulty'].difficulty > maxDiff]

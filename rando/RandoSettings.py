
import sys, random
from rando.Items import ItemManager
from utils import getRangeDict, chooseFromRange

# Holder for settings and a few utility functions related to them
# (especially for plando/rando).
# Holds settings not related to graph layout.
class RandoSettings(object):
    def __init__(self, maxDiff, progSpeed, progDiff, qty, restrictions,
                 superFun, runtimeLimit_s, plandoRandoItemLocs):
        self.progSpeed = progSpeed.lower()
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
            return ItemManager('Plando', self.qty, smbm)

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

# Holds settings and utiliy functions related to graph layout
class GraphSettings(object):
    def __init__(self, startAP, areaRando, bossRando, escapeRando, dotFile, plandoRandoTransitions):
        self.bidir = True
        self.startAP = startAP
        self.areaRando = areaRando
        self.bossRando = bossRando
        self.escapeRando = escapeRando
        self.dotFile = dotFile
        self.plandoRandoTransitions = plandoRandoTransitions

    # used by FillerRandom to know how many front fill steps it must perform
    def getRandomFillHelp(self):
        helpByAp = {
            "Firefleas Top": 3,
            "Aqueduct": 1,
            "Mama Turtle": 1,
            "Watering Hole": 2,
            "Etecoons Supers": 2,
            "Gauntlet Top":1,
            "Bubble Mountain":1
        }
        return helpByAp[self.startAP] if self.startAP in helpByAp else 0

# algo settings depending on prog speed (slowest to fastest+variable,
# other "speeds" are actually different algorithms)
class ProgSpeedParameters(object):
    def __init__(self, restrictions):
        self.restrictions = restrictions

    def getVariableSpeed(self):
        ranges = getRangeDict({
            'slowest':5,
            'slow':20,
            'medium':35,
            'fast':25,
            'fastest':15
        })
        return chooseFromRange(ranges)

    def getMinorHelpProb(self, progSpeed):
        if self.restrictions.split != 'Major':
            return 0
        if progSpeed == 'slowest':
            return 0.16
        elif progSpeed == 'slow':
            return 0.33
        elif progSpeed == 'medium':
            return 0.5
        return 1

    def getItemLimit(self, progSpeed):
        itemLimit = 105
        if progSpeed == 'slow':
            itemLimit = 21
        elif progSpeed == 'medium':
            itemLimit = 9
        elif progSpeed == 'fast':
            itemLimit = 6
        elif progSpeed == 'fastest':
            itemLimit = 1
        if self.restrictions.split == 'Chozo':
            itemLimit = int(itemLimit / 4)
        minLimit = itemLimit - int(itemLimit/5)
        maxLimit = itemLimit + int(itemLimit/5)
        if minLimit == maxLimit:
            itemLimit = minLimit
        else:
            itemLimit = random.randint(minLimit, maxLimit)
        return itemLimit

    def getLocLimit(self, progSpeed):
        locLimit = -1
        if progSpeed == 'slow':
            locLimit = 1
        elif progSpeed == 'medium':
            locLimit = 2
        elif progSpeed == 'fast':
            locLimit = 3
        elif progSpeed == 'fastest':
            locLimit = 4
        return locLimit

    def getProgressionItemTypes(self, progSpeed):
        progTypes = ItemManager.getProgTypes()
        progTypes.append('Charge')
        if progSpeed == 'slowest':
            return progTypes
        else:
            progTypes.remove('HiJump')
            progTypes.remove('Charge')
        if progSpeed == 'slow':
            return progTypes
        else:
            progTypes.remove('Bomb')
            progTypes.remove('Grapple')
        if progSpeed == 'medium':
            return progTypes
        else:
            progTypes.remove('Ice')
            progTypes.remove('SpaceJump')
        if progSpeed == 'fast':
            return progTypes
        else:
            progTypes.remove('SpeedBooster')
        if progSpeed == 'fastest':
            return progTypes # only morph, varia, gravity
        raise RuntimeError("Unknown prog speed " + progSpeed)

    def getPossibleSoftlockProb(self, progSpeed):
        if progSpeed == 'slowest':
            return 1
        if progSpeed == 'slow':
            return 0.66
        if progSpeed == 'medium':
            return 0.33
        if progSpeed == 'fast':
            return 0.1
        if progSpeed == 'fastest':
            return 0
        raise RuntimeError("Unknown prog speed " + progSpeed)

    def getChooseLocDict(self, progDiff):
        if progDiff == 'normal':
            return {
                'Random' : 1,
                'MinDiff' : 0,
                'MaxDiff' : 0
            }
        elif progDiff == 'easier':
            return {
                'Random' : 2,
                'MinDiff' : 1,
                'MaxDiff' : 0
            }
        elif progDiff == 'harder':
            return {
                'Random' : 2,
                'MinDiff' : 0,
                'MaxDiff' : 1
            }

    def getChooseItemDict(self, progSpeed):
        if progSpeed == 'slowest':
            return {
                'MinProgression' : 1,
                'Random' : 2,
                'MaxProgression' : 0
            }
        elif progSpeed == 'slow':
            return {
                'MinProgression' : 25,
                'Random' : 75,
                'MaxProgression' : 0
            }
        elif progSpeed == 'medium':
            return {
                'MinProgression' : 0,
                'Random' : 1,
                'MaxProgression' : 0
            }
        elif progSpeed == 'fast':
            return {
                'MinProgression' : 0,
                'Random' : 85,
                'MaxProgression' : 15
            }
        elif progSpeed == 'fastest':
            return {
                'MinProgression' : 0,
                'Random' : 2,
                'MaxProgression' : 1
            }

    def getSpreadFactor(self, progSpeed):
        if progSpeed == 'slowest':
            return 0.9
        elif progSpeed == 'slow':
            return 0.7
        elif progSpeed == 'medium':
            return 0.4
        elif progSpeed == 'fast':
            return 0.1
        return 0

    def getChozoSecondPhaseRestrictionProb(self, progSpeed):
        if progSpeed == 'slowest':
            return 0
        if progSpeed == 'slow':
            return 0.16
        if progSpeed == 'medium':
            return 0.5
        if progSpeed == 'fast':
            return 0.9
        return 1

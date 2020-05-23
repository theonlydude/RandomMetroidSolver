import log, random
from utils import getRangeDict, chooseFromRange

class Choice(object):
    def __init__(self, restrictions):
        self.restrictions = restrictions
        self.settings = restrictions.settings
        self.log = log.get("Choice")

    # args are return from RandoServices.getPossiblePlacements
    # return itemLoc dict, or None if no possible choice
    def chooseItemLoc(self, itemLocDict, isProg):
        return None

    def getItemList(self, itemLocDict):
        return sorted([wrapper.item for wrapper in itemLocDict.keys()], key=lambda item: item['Type'])
    def getLocList(self, itemLocDict, item):
        return itemLocDict[item['Wrapper']]

# simple random choice (still with early morph check)
class ItemThenLocChoice(Choice):
    def __init__(self, restrictions):
        super(ItemThenLocChoice, self).__init__(restrictions)

    def chooseItemLoc(self, itemLocDict, isProg):
        itemList = self.getItemList(itemLocDict)
        item = self.chooseItem(itemList, isProg)
        if item is None:
            return None
        locList = self.getLocList(itemLocDict, item)
        loc = self.chooseLocation(locList, item, isProg)
        if loc is None:
            return None
        return {
            'Item': item,
            'Location': loc
        }

    def chooseItem(self, itemList, isProg):
        if len(itemList) == 0:
            return None
        if isProg:
            return self.chooseItemProg(itemList)
        else:
            return self.chooseItemRandom(itemList)

    def earlyMorphCheck(self, itemList):
        if not self.restrictions.isEarlyMorph():
            return None
        return next((item for item in itemList if item['Type'] == 'Morph'), None)

    def chooseItemProg(self, itemList):
        ret = self.earlyMorphCheck(itemList)
        if ret is None:
            ret = self.chooseItemRandom(itemList)
        return ret

    def chooseItemRandom(self, itemList):
        return random.choice(itemList)

    def chooseLocation(self, locList, item, isProg):
        if len(locList) == 0:
            return None
        if isProg:
            return self.chooseLocationProg(locList, item)
        else:
            return self.chooseLocationRandom(locList)

    def chooseLocationProg(self, locList, item):
        return self.chooseLocationRandom(locList)

    def chooseLocationRandom(self, locList):
        return random.choice(locList)


class ItemThenLocChoiceProgSpeed(ItemThenLocChoice):
    def __init__(self, restrictions, distanceProp):
        super(ItemThenLocChoiceProgSpeed, self).__init__(restrictions)
        self.distanceProp = distanceProp
        self.chooseItemFuncs = {
            'Random' : self.chooseItemRandom,
            'MinProgression' : self.chooseItemMinProgression,
            'MaxProgression' : self.chooseItemMaxProgression
        }
        self.chooseLocFuncs = {
            'Random' : self.chooseLocationRandom,
            'MinDiff' : self.chooseLocationMinDiff,
            'MaxDiff' : self.chooseLocationMaxDiff
        }

    def chooseItemLoc(self, itemLocDict, isProg, progressionItemLocs):
        self.progressionItemLocs = progressionItemLocs
        return super(ItemThenLocChoiceProgSpeed, self).chooseItemLoc(itemLocDict, isProg)

    def determineParameters(self, progSpeed=None, progDiff=None):
        self.chooseLocRanges = getRangeDict(self.getChooseLocs(progDiff))
        self.chooseItemRanges = getRangeDict(self.getChooseItems(progSpeed))
        self.spreadProb = self.getSpreadFactor(progSpeed)

    def getChooseLocs(self, progDiff=None):
        if progDiff is None:
            progDiff = self.settings.progDiff
        return self.getChooseLocDict(self.settings.progDiff)

    def getChooseItems(self, progSpeed):
        if progSpeed is None:
            progSpeed = self.settings.progSpeed
        return self.getChooseItemDict(progSpeed)

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
                'Random' : 75,
                'MaxProgression' : 25
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

    def chooseItemProg(self, itemList):
        ret = self.earlyMorphCheck(itemList)
        if ret is None:
            ret = self.getChooseFunc(self.chooseItemRanges, self.chooseItemFuncs)(itemList)
        self.log.debug('chooseItemProg. ret='+ret['Type'])
        return ret

    def chooseLocationProg(self, locs, item):
        locs = self.getLocsSpreadProgression(locs)
        random.shuffle(locs)
        ret = self.getChooseFunc(self.chooseLocRanges, self.chooseLocFuncs)(locs)
        self.log.debug('chooseLocationProg. ret='+ret['Name'])
        return ret

    # get choose function from a weighted dict
    def getChooseFunc(self, rangeDict, funcDict):
        v = chooseFromRange(rangeDict)

        return funcDict[v]

    def chooseItemMinProgression(self, items):
        minNewLocs = 1000
        ret = None

        for item in items:
            newLocs = len(self.currentLocations(item))
            if newLocs < minNewLocs:
                minNewLocs = newLocs
                ret = item
        return ret

    def chooseItemMaxProgression(self, items):
        maxNewLocs = 0
        ret = None

        for item in items:
            newLocs = len(self.currentLocations(item))
            if newLocs > maxNewLocs:
                maxNewLocs = newLocs
                ret = item
        return ret

    def getLocDiff(self, loc):
        # avail difficulty already stored by graph algorithm
        return loc['difficulty']

    def fillLocsDiff(self, locs):
        for loc in locs:
            if 'PostAvailable' in loc:
                loc['difficulty'] = self.smbm.wand(self.getLocDiff(loc), self.smbm.eval(loc['PostAvailable']))

    def chooseLocationMaxDiff(self, availableLocations, item):
        self.log.debug("MAX")
        self.fillLocsDiff(availableLocations)
        self.log.debug("chooseLocationMaxDiff: {}".format([(l['Name'], l['difficulty']) for l in availableLocations]))
        return max(availableLocations, key=lambda loc:loc['difficulty'].difficulty)

    def chooseLocationMinDiff(self, availableLocations, item):
        self.log.debug("MIN")
        self.fillLocsDiff(availableLocations)
        self.log.debug("chooseLocationMinDiff: {}".format([(l['Name'], l['difficulty']) for l in availableLocations]))
        return min(availableLocations, key=lambda loc:loc['difficulty'].difficulty)

    def areaDistance(self, loc, otherLocs):
        areas = [l[self.distanceProp] for l in otherLocs]
        cnt = areas.count(loc[self.distanceProp])
        d = None
        if cnt == 0:
            d = 2
        else:
            d = 1.0/cnt
        return d

    def getLocsSpreadProgression(self, availableLocations):
        cond = lambda item: ((self.restriction.split == 'Full' and item['Class'] == 'Major') or self.restriction.split == item['Class']) and item['Category'] != "Energy"
        progLocs = [il['Location'] for il in self.progressionItemLocs if cond(il['Item'])]
        distances = [self.areaDistance(loc, progLocs) for loc in availableLocations]
        maxDist = max(distances)
        locs = []
        for i in range(len(availableLocations)):
            loc = availableLocations[i]
            d = distances[i]
            if d == maxDist or random.random() >= self.spreadProb:
                locs.append(loc)
        return locs

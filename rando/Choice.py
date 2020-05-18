

import log, random

class Choice(object):
    def __init__(self, restrictions):
        self.restrictions = restrictions
        self.loc = log.get("Choice")
    
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
        return next((item for item in items if item['Type'] == 'Morph'), None)

    def chooseItemProg(self, itemList):
        ret = self.earlyMorphCheck(itemList)
        if ret is None:
            ret = self.chooseItemRandom(itemList)
        return ret

    def chooseItemRandom(self, itemList):
        return random.choice(itemList)

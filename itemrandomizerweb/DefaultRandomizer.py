from Randomizer import Randomizer
from stdlib import Map, Array, List, Random
import Items
import random

class DefaultRandomizer(Randomizer):
    def __init__(self, seed, difficultyTarget, locations, sampleSize=1):
        super(DefaultRandomizer, self).__init__(seed, difficultyTarget, locations, sampleSize)

    def getItemToPlace(self, items, itemPool):        
        itemsLen = len(items)
        if itemsLen == 0:
            item = List.item(random.randint(0, len(itemPool)-1), itemPool)
        else:
            item = self.chooseItem(items)
        return item

#     def chooseItem(self, items):
#         # print(len(items))
#         # print([i['Type'] for i in items])
#         minNewLocs = 1000
#         ret = None
        
#         for item in items:
#             if item in self.failItems:
#                 continue
#             newLocs = len(self.currentLocations(self.currentItems + [item]))
#             if newLocs < minNewLocs:
#                 minNewLocs = newLocs
#                 ret = item
# #        print(ret['Type'] + ' ' + str(minNewLocs))
#         return ret
    
    # def chooseLocation(self, availableLocations):
    #     if self.chosenLocation is None:
    #         self.chosenLocation = availableLocations[random.randint(0, len(availableLocations)-1)]
    #     else:
    #         random.shuffle(availableLocations)
    #         chosen = availableLocations[0]
    #         for loc in availableLocations:
    #             if loc['Area'] != self.chosenLocation['Area']:
    #                 chosen = loc
    #                 break
    #         self.chosenLocation = chosen
    #     return self.chosenLocation
    
    def generateItems(self):
        items = []
        itemLocations = []
        self.currentItems = items
        while len(self.itemPool) > 0:
            curLocs = self.currentLocations(items)
            itemLocation = None
            self.failItems = []
            while itemLocation is None:
                posItems = self.possibleItems(curLocs, items, itemLocations, self.itemPool, self.locationPool)
                itemLocation = self.placeItem(posItems, self.itemPool, curLocs)
            print(str(len(self.currentItems) + 1) + ':' + itemLocation['Item']['Type'] + ' at ' + itemLocation['Location']['Name'])
            items.append(itemLocation['Item'])
            itemLocations.append(itemLocation)
            self.itemPool = self.removeItem(itemLocation['Item']['Type'], self.itemPool)

        return itemLocations

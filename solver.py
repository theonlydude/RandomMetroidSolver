#!/usr/bin/python

# https://itemrando.supermetroid.run/randomize

import sys, struct, math, os, json, logging

# the difficulties for each technics
from parameters import *
# the canXXX functions
from helpers import *

class Solver:
    # given a rom and parameters returns the estimated difficulty

    items = {
        '0xeed7': {'name': 'ETank'},
        '0xeedb': {'name': 'Missile'},
        '0xeedf': {'name': 'Super'},
        '0xeee3': {'name': 'PowerBomb'},
        '0xeee7': {'name': 'Bomb'},
        '0xeeeb': {'name': 'Charge'},
        '0xeeef': {'name': 'Ice'},
        '0xeef3': {'name': 'HiJump'},
        '0xeef7': {'name': 'SpeedBooster'},
        '0xeefb': {'name': 'Wave'},
        '0xeeff': {'name': 'Spazer'},
        '0xef03': {'name': 'SpringBall'},
        '0xef07': {'name': 'Varia'},
        '0xef13': {'name': 'Plasma'},
        '0xef17': {'name': 'Grapple'},
        '0xef23': {'name': 'Morph'},
        '0xef27': {'name': 'Reserve'},
        '0xef0b': {'name': 'Gravity'},
        '0xef0f': {'name': 'XRayScope'},
        '0xef1b': {'name': 'SpaceJump'},
        '0xef1f': {'name': 'ScrewAttack'}
    }

    def __init__(self):
        import tournament_locations
        self.locations = tournament_locations.locations

        #logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger('Solver')

    def loadRom(self, romName):
        RomReader(romName).loadItems(self.locations)

        # add item name to location
        self.log.debug("Display items at locations:")
        for location in self.locations:
            location['itemName'] = self.items[location["item"]]['name']
            self.log.debug('{:>50}: {:>16}'.format(location["Name"], location['itemName']))

    def loadParams(self, paramName=None):
        # TODO::load parameters.py vars into an object instead of in global
        if paramName is None:
            return

        # the json file is a dict with the knowsXXX variables
        with open(paramName) as jsonFile:
            params = json.load(jsonFile)

            # load the params into the global vars
            for param in params:
                globals()[param] = params[param]

    def solveRom(self, romName, paramName):
        self.loadParams(paramName)
        self.loadRom(romName)

        difficulty = self.getDifficulty()

        self.displayDifficulty(difficulty)

    def displayDifficulty(self, difficulty):
        if difficulty[0] >= 0:
            DifficultyDisplayer(difficulty[0]).scale()
        else:
            print("Aborted run, can't finish the game with the given prerequisites")

    def getDifficulty(self):
        # loop on the available locations depending on the collected items.
        # before getting a new item, loop on all of them and get their difficulty,
        # the next collected item is the one with the smallest difficulty,
        # if equality between major and minor, take major first.

        majorLocations = [loc for loc in self.locations if loc["Class"] == "Major"]
        minorLocations = [loc for loc in self.locations if loc["Class"] == "Minor"]

        visitedLocations = []
        collectedItems = []

        # with the knowsXXX conditions some roms can be unbeatable, so we have to detect it
        previous = -1
        current = 0

        self.log.debug("{}: available major: {}, available minor: {}, visited: {}".format(itemsPickup, len(majorLocations), len(minorLocations), len(visitedLocations)))

        isEndPossible = False
        endDifficulty = mania
        area = 'Crateria'
        while True:
            # actual while condition
            hasEnoughItems = enoughMajors(collectedItems, majorLocations, visitedLocations) and enoughMinors(collectedItems, minorLocations)
            (isEndPossible, endDifficulty) = canEndGame(collectedItems)
            if isEndPossible and hasEnoughItems:
                break
            self.log.debug(str(collectedItems))

            current = len(collectedItems)
            if current == previous:
                # we're stuck ! abort
                break
            previous = current

            # compute the difficulty of all the locations
            for loc in majorLocations:
                if 'PostAvailable' in loc:
                    loc['difficulty'] = wand(loc['Available'](collectedItems),
                                             loc['PostAvailable'](collectedItems + [loc['itemName']]))
                else:
                    loc['difficulty'] = loc['Available'](collectedItems)
            enough = enoughMinors(collectedItems, minorLocations)
            if not enough:
                for loc in minorLocations:
                    loc['difficulty'] = loc['Available'](collectedItems)

            # keep only the available locations
            majorAvailable = [loc for loc in majorLocations if loc["difficulty"][0] == True]
            if not enough:
                minorAvailable = [loc for loc in minorLocations if loc["difficulty"][0] == True]

            if len(majorAvailable) == 0 and enough is True:
                # stuck
                break

            # sort them on difficulty and proximity
            majorAvailable = getAvailableItemsList(majorAvailable, area, difficulty_target)
            if not enough:
                minorAvailable = getAvailableItemsList(minorAvailable, area, difficulty_target)

            # first take major items in the current area
            majorPicked = False
            while len(majorAvailable) > 0 and majorAvailable[0]['Area'] == area and majorAvailable[0]['difficulty'][0] <= easy:
                loc = majorAvailable.pop(0)
                majorLocations.remove(loc)
                visitedLocations.append(loc)
                self.collectItem(collectedItems, loc)
                majorPicked = True

            # if we take at least one major, recompute the difficulty
            if majorPicked is True:
                continue

            # if enough stuff, take the next available major
            if enough is True:
                # take first major
                loc = majorAvailable.pop(0)
                majorLocations.remove(loc)
                visitedLocations.append(loc)
                area = self.collectItem(collectedItems, loc)
            else:
                if len(majorAvailable) == 0:
                    nextMajorDifficulty = mania * 10
                else:
                    nextMajorDifficulty = majorAvailable[0]["difficulty"][1]

                # take the minors easier than the next major, check if we don't get too much stuff
                minorPicked = False
                while len(minorAvailable) > 0 and minorAvailable[0]["difficulty"][1] < nextMajorDifficulty and not enoughMinors(collectedItems, minorLocations):
                    loc = minorAvailable.pop(0)
                    minorLocations.remove(loc)
                    visitedLocations.append(loc)
                    area = self.collectItem(collectedItems, loc)
                    minorPicked = True

                # if we take at least one minor, recompute the difficulty
                if minorPicked is True:
                    continue

                # take the next available major
                if len(majorAvailable) > 0:
                    loc = majorAvailable.pop(0)
                    majorLocations.remove(loc)
                    visitedLocations.append(loc)
                    area = self.collectItem(collectedItems, loc)

        if isEndPossible:
            visitedLocations.append({
                'item' : 'The End',
                'itemName' : 'The End',
                'Name' : 'The End',
                'Area' : 'The End',
                'difficulty' : (True, endDifficulty)
            })
        # print generated path
        if displayGeneratedPath is True:
            print("Generated path:")
            print('{:>50}: {:>12} {:>16} {}'.format("Location Name", "Area", "Item", "Difficulty"))
            print('-'*92)
            for location in visitedLocations:
                print('{:>50}: {:>12} {:>16} {}'.format(location['Name'],
                                                        location['Area'],
                                                        location['itemName'],
                                                        location['difficulty'][1]))

        if not enoughMajors(collectedItems, majorLocations, visitedLocations) or not enoughMinors(collectedItems, minorLocations) or not canEndGame(collectedItems):
            # we have aborted
            difficulty = (-1, -1)
        else:
            # sum difficulty for all visited locations
            difficulty_sum = 0
            difficulty_max = 0
            for loc in visitedLocations:
                difficulty_sum = difficulty_sum + loc['difficulty'][1]
                difficulty_max = max(difficulty_max, loc['difficulty'][1])
            # we compute the number of '+' that we'll display next to the difficulty to take in
            # account the sum of the difficulties.
            if difficulty_sum > difficulty_max:
                difficulty = (difficulty_max, (difficulty_sum - difficulty_max) / (difficulty_max * 2))
            else:
                difficulty = (difficulty_max, 0)

        self.log.debug("{}: remaining major: {}, remaining minor: {}, visited: {}".format(itemsPickup, len(majorLocations), len(minorLocations), len(visitedLocations)))

        return difficulty

    def collectItem(self, collectedItems, loc):
        collectedItems.append(loc["itemName"])
        if 'Pickup' in loc:
            loc['Pickup']()
        return loc['Area']

class RomReader:
    # read the items in the rom

    def __init__(self, romName):
        self.romName = romName

    def getItem(self, romFile, address, visibility):
        # return the hex code of the object at the given address

        romFile.seek(address, 0)
        # value is in two bytes
        value1 = struct.unpack("B", romFile.read(1))
        value2 = struct.unpack("B", romFile.read(1))

        # match itemVisibility with
        # | Visible -> 0
        # | Chozo -> 0x54 (84)
        # | Hidden -> 0xA8 (168)
        if visibility == 'Visible':
            return hex(value2[0]*256+(value1[0]-0))
        elif visibility == 'Chozo':
            return hex(value2[0]*256+(value1[0]-84))
        elif visibility == 'Hidden':
            return hex(value2[0]*256+(value1[0]-168))
        else:
            # crash !
            manger.du(cul)

    def loadItems(self, locations):
        with open(self.romName, "rb") as romFile:
            for location in locations:
                location["item"] = self.getItem(romFile, location["Address"], location["Visibility"])

class DifficultyDisplayer:
    difficulties = {
        easy : 'easy',
        medium : 'medium',
        hard : 'hard',
        harder : 'very hard',
        hardcore : 'hardcore',
        mania : 'mania'
    }

    def __init__(self, difficulty):
        self.difficulty = difficulty

    def text(self):
        if self.difficulty >= easy and self.difficulty < medium:
            difficultyText = self.difficulties[easy]
        elif self.difficulty >= medium and self.difficulty < hard:
            difficultyText = self.difficulties[medium]
        elif self.difficulty >= hard and self.difficulty < harder:
            difficultyText = self.difficulties[hard]
        elif self.difficulty >= harder and self.difficulty < hardcore:
            difficultyText = self.difficulties[harder]
        elif self.difficulty >= hardcore and self.difficulty < mania:
            difficultyText = self.difficulties[hardcore]
        else:
            difficultyText = self.difficulties[mania]

        print("Estimated difficulty for items pickup {}: {}".format(itemsPickup, difficultyText))
    
    def scale(self):
        if self.difficulty == 0:
            print('FREEEEEE')
            return

        previous = 0
        for d in sorted(self.difficulties):
            if self.difficulty >= d:
                previous = d
            else:
                displayString = self.difficulties[previous]
                displayString += ' '
                scale = d - previous
                pos = int(self.difficulty - previous)
                displayString += '-' * pos
                displayString += '^'
                displayString += '-' * (scale - pos)
                displayString += ' '
                displayString += self.difficulties[d]
                print(displayString)
                break

        if previous == 0:
            print('MAAAANIIIAAAAAAA')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        romName = sys.argv[1]
        paramName = None
    elif len(sys.argv) == 3:
        romName = None
        paramName = None
        for arg in sys.argv[1:]:
            ext = os.path.splitext(arg)
            if ext[1] == '.sfc':
                romName = arg
            elif ext[1] == '.json':
                paramName = arg
            else:
                print("wrong file type given as parameter: {}".format(ext))
                sys.exit(-1)
    else:
        print("missing param: rom file")
        sys.exit(0)

    Solver().solveRom(romName, paramName)

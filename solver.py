#!/usr/bin/python

# https://itemrando.supermetroid.run/randomize

import sys, struct, math, os, json, logging

# the difficulties for each technics
from parameters import Conf, Knows, Settings
from parameters import easy, medium, hard, harder, hardcore, mania

# the helper functions
from helpers import *

class Solver:
    # given a rom and parameters returns the estimated difficulty

    def __init__(self, type='console', rom=None, params=None):
        #logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger('Solver')

        if params is not None:
            self.loadParams(params)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("loaded knows: ")
            for knows in Knows.__dict__:
                if knows[0:len('__')] != '__':
                    self.log.debug("{}: {}".format(knows, Knows.__dict__[knows]))
            self.log.debug("loaded settings:")
            for setting in Settings.__dict__:
                if setting[0:len('__')] != '__':
                    self.log.debug("{}: {}".format(setting, Settings.__dict__[setting]))
            self.log.debug("loaded conf:")
            for conf in Conf.__dict__:
                if conf[0:len('__')] != '__':
                    self.log.debug("{}: {}".format(conf, Conf.__dict__[conf]))

        import tournament_locations
        self.locations = tournament_locations.locations

        self.pickup = Pickup(Conf.itemsPickup)

        # can be called from command line (console) or from web site (web)
        self.type = type

        self.romLoaded = False
        if rom is not None:
            self.loadRom(rom)

    def loadRom(self, rom):
        RomLoader.factory(rom).assignItems(self.locations)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("Display items at locations:")
            for location in self.locations:
                self.log.debug('{:>50}: {:>16}'.format(location["Name"], location['itemName']))

        self.romLoaded = True

    def loadParams(self, params):
        ParamsLoader.factory(params).load()

    def solveRom(self):
        if  self.romLoaded is False:
            self.log.error("rom not loaded")
            return

        difficulty = self.computeDifficulty()

        if self.type == 'console':
            # print generated path
            if Conf.displayGeneratedPath is True:
                self.printPath("Generated path:", self.visitedLocations)
                # if we've aborted, display remaining majors
                if difficulty == -1:
                    self.printPath("Remaining major locations:", self.majorLocations)

            # display difficulty scale
            self.displayDifficulty(difficulty)

        return difficulty

    def displayDifficulty(self, difficulty):
        if difficulty >= 0:
            text = DifficultyDisplayer(difficulty).scale()
            print("Estimated difficulty for items pickup {}: {}".format(Conf.itemsPickup, text))
        else:
            print("Aborted run, can't finish the game with the given prerequisites")

    def computeDifficulty(self):
        # loop on the available locations depending on the collected items.
        # before getting a new item, loop on all of them and get their difficulty,
        # the next collected item is the one with the smallest difficulty,
        # if equality between major and minor, take major first.

        self.majorLocations = [loc for loc in self.locations if loc["Class"] == "Major"]
        self.minorLocations = [loc for loc in self.locations if loc["Class"] == "Minor"]

        self.visitedLocations = []
        self.collectedItems = []

        # with the knowsXXX conditions some roms can be unbeatable, so we have to detect it
        previous = -1
        current = 0

        self.log.debug("{}: available major: {}, available minor: {}, visited: {}".format(Conf.itemsPickup, len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

        isEndPossible = False
        endDifficulty = mania
        area = 'Crateria'
        while True:
            # actual while condition
            hasEnoughItems = (self.pickup.enoughMajors(self.collectedItems, self.majorLocations)
                              and self.pickup.enoughMinors(self.collectedItems, self.minorLocations))
            (isEndPossible, endDifficulty) = self.canEndGame()
            if isEndPossible and hasEnoughItems:
                break

            self.log.debug(str(self.collectedItems))

            # check if we have collected an item in the last loop
            current = len(self.collectedItems)
            if current == previous:
                # we're stuck ! abort
                break
            previous = current

            # compute the difficulty of all the locations
            self.computeLocationsDifficulty(self.majorLocations)
            enough = self.pickup.enoughMinors(self.collectedItems, self.minorLocations)
            if not enough:
                self.computeLocationsDifficulty(self.minorLocations)

            # keep only the available locations
            majorAvailable = [loc for loc in self.majorLocations if loc["difficulty"][0] == True]
            if not enough:
                minorAvailable = [loc for loc in self.minorLocations if loc["difficulty"][0] == True]

            # check if we're stuck
            if len(majorAvailable) == 0 and enough is True:
                break

            # sort them on difficulty and proximity
            majorAvailable = self.getAvailableItemsList(majorAvailable, area, Conf.difficultyTarget)
            if not enough:
                minorAvailable = self.getAvailableItemsList(minorAvailable, area, Conf.difficultyTarget)

            # first take easy major items in the current area
            majorPicked = False
            while (len(majorAvailable) > 0
                   and majorAvailable[0]['Area'] == area
                   and majorAvailable[0]['difficulty'][0] <= easy):
                self.collectMajor(majorAvailable.pop(0))
                majorPicked = True

            # if we take at least one major, recompute the difficulty
            if majorPicked is True:
                continue

            # if enough stuff, take the next available major
            if enough is True:
                # take first major
                area = self.collectMajor(majorAvailable.pop(0))
            else:
                if len(majorAvailable) == 0:
                    nextMajorDifficulty = mania * 10
                else:
                    nextMajorDifficulty = majorAvailable[0]["difficulty"][1]

                # take the minors easier than the next major, check if we don't get too much stuff
                minorPicked = False
                while (len(minorAvailable) > 0
                       and minorAvailable[0]["difficulty"][1] < nextMajorDifficulty
                       and not self.pickup.enoughMinors(self.collectedItems, self.minorLocations)):
                    area = self.collectMinor(minorAvailable.pop(0))
                    minorPicked = True

                # if we take at least one minor, recompute the difficulty
                if minorPicked is True:
                    continue

                # take the next available major
                if len(majorAvailable) > 0:
                    area = self.collectMajor(majorAvailable.pop(0))

        if isEndPossible:
            self.visitedLocations.append({
                'item' : 'The End',
                'itemName' : 'The End',
                'Name' : 'The End',
                'Area' : 'The End',
                'difficulty' : (True, endDifficulty)
            })

        # compute difficulty value
        difficulty = self.computeDifficultyValue()

        self.log.debug("{}: remaining major: {}, remaining minor: {}, visited: {}".format(Conf.itemsPickup, len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

        self.log.debug("remaining majors:")
        for loc in self.majorLocations:
            self.log.debug("{} ({})".format(loc['Name'], loc['itemName']))

        self.log.debug("bosses: {}".format(Bosses.golden4Dead))

        return difficulty

    def computeLocationsDifficulty(self, locations):
        for loc in locations:
            if 'PostAvailable' in loc:
                loc['difficulty'] = wand(loc['Available'](self.collectedItems),
                                         loc['PostAvailable'](self.collectedItems + [loc['itemName']]))
            else:
                loc['difficulty'] = loc['Available'](self.collectedItems)

    def computeDifficultyValue(self):
        if not self.pickup.enoughMajors(self.collectedItems, self.majorLocations) or not self.pickup.enoughMinors(self.collectedItems, self.minorLocations) or not self.canEndGame():
            # we have aborted
            difficulty = -1
        else:
            # sum difficulty for all visited locations
            difficulty_max = 0
            for loc in self.visitedLocations:
                difficulty_max = max(difficulty_max, loc['difficulty'][1])
            difficulty = difficulty_max

        return difficulty

    def printPath(self, message, locations):
        print(message)
        print('{:>50}: {:>12} {:>16} {}'.format("Location Name", "Area", "Item", "Difficulty"))
        print('-'*92)
        for location in locations:
            print('{:>50}: {:>12} {:>16} {}'.format(location['Name'],
                                                    location['Area'],
                                                    location['itemName'],
                                                    location['difficulty'][1]))

    def collectMajor(self, loc):
        self.majorLocations.remove(loc)
        self.visitedLocations.append(loc)
        area = self.collectItem(loc)
        return area

    def collectMinor(self, loc):
        self.minorLocations.remove(loc)
        self.visitedLocations.append(loc)
        area = self.collectItem(loc)
        return area

    def collectItem(self, loc):
        item = loc["itemName"]
        if loc["Class"] == "Minor" or self.pickup.grabItem(self.collectedItems, item):
            self.collectedItems.append(item)
        else:
            self.log.debug("Item not picked up: {}".format(item))
            self.collectedItems.append('Dummy')
        if 'Pickup' in loc:
            loc['Pickup']()

        self.log.debug("collectItem: {} at {}".format(item, loc['Name']))

        return loc['Area']

    def canEndGame(self):
        # to finish the game you must :
        # - beat golden 4 : we force pickup of the 4 items
        #   behind the bosses to ensure that
        # - defeat metroids
        # - destroy/skip the zebetites
        # - beat Mother Brain
        return wand(Bosses.allBossesDead(), enoughStuffTourian(self.collectedItems))

    def getAvailableItemsList(self, locations, area, threshold):
        around = [loc for loc in locations if loc['Area'] == area and loc['difficulty'][1] <= threshold and not Bosses.areaBossDead(area)]
        around.sort(key=lambda loc: loc['difficulty'][1])

        outside = [loc for loc in locations if not loc in around]
        # we want to sort the outside locations by putting the ones is the same area first,
        # then we sort by remaining areas.
        outside.sort(key=lambda loc: (loc['difficulty'][1], 0 if loc['Area'] == area else 1, loc['Area']))

        return around + outside

class RomReader:
    # read the items in the rom
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

    def __init__(self, romFileName):
        self.romFileName = romFileName

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
        with open(self.romFileName, "rb") as romFile:
            for loc in locations:
                item = self.getItem(romFile, loc["Address"], loc["Visibility"])
                loc["itemName"] = self.items[item]["name"]

class RomLoader:
    @staticmethod
    def factory(rom):
        # can be a real rom. can be a json or a dict with the locations - items association
        if type(rom) is str:
            ext = os.path.splitext(rom)
            if ext[1].lower() == '.sfc' or ext[1].lower() == '.smc':
                return RomLoaderSfc(rom)
            elif ext[1].lower() == '.json':
                return RomLoaderJson(rom)
            else:
                print("wrong rom file type: {}".format(ext[1]))
                sys.exit(-1)
        elif type(rom) is dict:
            return RomLoaderDict(rom)

    def assignItems(self, locations):
        # update the itemName of the locations
        for loc in locations:
            loc['itemName'] = self.locsItems[loc['Name']]

    def dump(self, fileName):
        with open(fileName, 'w') as jsonFile:
            json.dump(self.locsItems, jsonFile)

class RomLoaderSfc(RomLoader):
    # standard usage
    def __init__(self, romFileName):
        self.romReader = RomReader(romFileName)

    def assignItems(self, locations):
        # update the itemName of the locations
        self.romReader.loadItems(locations)

        self.locsItems = {}
        for loc in locations:
            self.locsItems[loc['Name']] = loc['itemName']

class RomLoaderJson(RomLoader):
    # when called from the test suite
    def __init__(self, jsonFileName):
        with open(jsonFileName) as jsonFile:
            self.locsItems = json.load(jsonFile)

class RomLoaderDict(RomLoader):
    # when called from the website
    def __init__(self, locsItems):
        self.locsItems = locsItems

class ParamsLoader:
    @staticmethod
    def factory(params):
        # can be a json, a python file or a dict with the parameters
        if type(params) is str:
            ext = os.path.splitext(params)
            if ext[1].lower() == '.json':
                return ParamsLoaderJson(params)
            elif ext[1].lower() == '.py':
                return ParamsLoaderPy(ext[0])
            else:
                print("wrong parameters file type: {}".format(ext[1]))
                sys.exit(-1)
        elif type(params) is dict:
            return ParamsLoaderDict(params)
        elif params is None:
            return ParamsLoaderMem()

    def load(self):
        # update the parameters in the parameters classes: Conf, Knows, Settings
        # Conf
        for param in self.params['Conf']:
            if param[0:len('__')] != '__':
                setattr(Conf, param, self.params['Conf'][param])

        # Knows
        for param in self.params['Knows']:
            if param[0:len('__')] != '__':
                setattr(Knows, param, self.params['Knows'][param])

        # Settings
        for param in self.params['Settings']:
            if param[0:len('__')] != '__':
                setattr(Settings, param, self.params['Settings'][param])

    def dump(self, fileName):
        with open(fileName, 'w') as jsonFile:
            json.dump(self.params, jsonFile)

    def printToScreen(self):
        print("self.params: {}".format(self.params))

        print("loaded knows: ")
        for knows in Knows.__dict__:
            if knows[0:len('__')] != '__':
                print("{}: {}".format(knows, Knows.__dict__[knows]))
        print("loaded settings:")
        for setting in Settings.__dict__:
            if setting[0:len('__')] != '__':
                print("{}: {}".format(setting, Settings.__dict__[setting]))
        print("loaded conf:")
        for conf in Conf.__dict__:
            if conf[0:len('__')] != '__':
                print("{}: {}".format(conf, Conf.__dict__[conf]))


class ParamsLoaderJson(ParamsLoader):
    # when called from the test suite
    def __init__(self, jsonFileName):
        with open(jsonFileName) as jsonFile:
            self.params = json.load(jsonFile)

class ParamsLoaderPy(ParamsLoader):
    # for testing purpose
    def __init__(self, pyFileName):
        import importlib
        mod = importlib.import_module(pyFileName)
        conf = getattr(mod, 'Conf')
        knows = getattr(mod, 'Knows')
        settings = getattr(mod, 'Settings')
        self.params = {'Conf': {k: v for k, v in conf.__dict__.items() if k[0:len('__')] != '__'},
                       'Knows': {k: v for k, v in knows.__dict__.items() if k[0:len('__')] != '__'},
                       'Settings': {k: v for k, v in settings.__dict__.items() if k[0:len('__')] != '__'}}

class ParamsLoaderDict(ParamsLoader):
    # when called from the website
    def __init__(self, params):
        self.params = params

class ParamsLoaderMem(ParamsLoader):
    # to load the current classes from memory
    def __init__(self):
        self.params = {'Conf': {k: v for k, v in Conf.__dict__.items() if k[0:len('__')] != '__'},
                       'Knows': {k: v for k, v in Knows.__dict__.items() if k[0:len('__')] != '__'},
                       'Settings': {k: v for k, v in Settings.__dict__.items() if k[0:len('__')] != '__'}}

class DifficultyDisplayer:
    difficulties = {
        0 : 'baby',
        easy : 'easy',
        medium : 'medium',
        hard : 'hard',
        harder : 'very hard',
        hardcore : 'hardcore',
        mania : 'mania',
        mania*2 : 'god',
        mania*4 : 'samus'
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

        return difficultyText

    def scale(self):
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
                break

        return displayString

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("missing param: rom file [param file]")
        sys.exit(0)

    romFileName = sys.argv[1]
    solver = Solver(rom=romFileName)

    if len(sys.argv) == 3:
        paramsFileName = sys.argv[2]
        solver.loadParams(paramsFileName)

    solver.solveRom()

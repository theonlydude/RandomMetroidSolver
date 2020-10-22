import random, logging, time
from collections import defaultdict

from rando.Filler import Filler
from rando.FillerRandom import FillerRandomItems, FrontFillerKickstart, FrontFillerNoCopy
from utils.parameters import infinity
from rando.Choice import ItemThenLocChoice
from graph.graph_access import GraphUtils
from rando.RandoServices import ComebackCheckType
from rando.ItemLocContainer import ItemLocation, getItemListStr, ContainerSoftBackup
from logic.smbool import SMBool
from logic.helpers import diffValue2txt
from rando.MiniSolver import MiniSolver
from solver.randoSolver import RandoSolver

class AssumedFiller(Filler):
    def __init__(self, startAP, graph, restrictions, container, endDate=infinity):
        super(AssumedFiller, self).__init__(startAP, graph, restrictions, container, endDate)
        self.choice = ItemThenLocChoice(restrictions)
        self.stdStart = GraphUtils.isStandardStart(self.startAP)
        # be more generous with only boss left steps in minisolver
        self.miniSolver = MiniSolver(startAP, graph, restrictions, 10)
        self.can100percent = False
        self.earlyGame = False

    def initFiller(self):
        super(AssumedFiller, self).initFiller()
        
        assert len(self.container.itemPool) == len(self.container.unusedLocations)

        if self.vcr is not None:
            # give all items to vcr, like we do in assumed fill
            self.vcr.setFiller('reverse')
            self.vcr.addInitialItems([it.Type for it in self.container.itemPool])

        # first collect mother brain
        self.ap = 'Golden Four'
        for (boss, bossLocName) in [('MotherBrain', 'Mother Brain')]:
            bossItem = self.container.getItems(lambda it: it.Type == boss)
            bossLoc = self.container.getLocs(lambda loc: loc.Name == bossLocName)
            self.collect(ItemLocation(bossItem[0], bossLoc[0]))

        self.alreadyTriedItems = defaultdict(set)
        self.alreadySwitchedItems = defaultdict(set)

        # get all aps accessible from start ap with no items
        self.firstAPs = [ap.Name for ap in self.graph.getAvailableAccessPoints(self.graph.accessPoints[self.startAP], self.container.sm, self.maxDiff)]

        self.log.debug("first APs: {}".format(self.firstAPs))
        # then all the locations linked to these first APs
        self.firstLocations = []
        for loc in self.container.unusedLocations:
            for ap in loc.AccessFrom.keys():
                if ap in self.firstAPs:
                    if self.isMajor(loc):
                        self.firstLocations.append(loc)
                    continue

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("first locations: {}".format(len(self.firstLocations)))
            for loc in self.firstLocations:
                self.log.debug(loc.Name)

        # TODO::choose morph loc first to forbid other items in it. TODO::handle early/late morph
        #firstItemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.container, assumedItems, alreadyPlacedItems)

    def isMajor(self, obj):
        return (self.settings.restrictions['MajorMinor'] == 'Full'
                or self.settings.restrictions['MajorMinor'] in obj.Class)

    def uncollect(self, loc):
        itemType = self.container.uncollect(loc)
        if self.vcr is not None:
            self.vcr.removeLocation(loc.Name, itemType)

    def getMoreUseless(self, item1, item2):
        # nothing < noenergy < missile < super < powerbomb < reserve < etank
        usefulness = {'Nothing': 0, 'NoEnergy': 1, 'Missile': 2, 'Super': 3, 'PowerBomb': 4, 'Reserve': 5, 'ETank': 6}

        if usefulness.get(item1.Type, infinity) < usefulness.get(item2.Type, infinity):
            return item1
        else:
            return item2

    def validateFill(self):
        self.log.debug("Final mini/real solver check to validate the fill")
        return self.can100percentReverse()

    def can100percentReverse(self):
        if self.can100percent:
            self.log.debug("can100percentReverse: already validated by real solver")
            return True
        # check that mini solver can beat the seed starting from start ap
        self.miniSolver.startAP = self.startAP
        if not self.miniSolver.isBeatable(self.container.itemLocations, self.maxDiff):
            return False
        self.log.debug("can100percentReverse: validated by mini solver")
        # do a full solver check
        graphLocations = self.container.getLocsForSolver()
        solver = RandoSolver(self.restrictions.split, self.startAP, self.graph, graphLocations)
        diff = solver.solveRom()
        self.container.cleanLocsAfterSolver()
        if diff == -1:
            self.log.debug("can100percentReverse: real solver validation failed")
            return False
        self.log.debug("can100percentReverse: validated by real solver")
        # don't do a real solver check each loop
        self.can100percent = True
        return True

    def displayItemLocDict(self, msg, itemLocDict):
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("{}: {}".format(msg, [(it.Type, data['availLocsWoItemLen'], len(data['possibleLocs'])) for (it, data) in itemLocDict.items()]))
            for it, data in itemLocDict.items():
                locs = data['possibleLocs']
                self.log.debug("  {}: {}".format(it.Type, [loc.Name for loc in locs] if len(locs) < 5 else len(locs)))

    def getPriorityLocations(self, itemLocDict):
        # for each item get the locations which become unreachable after placing the item (ie. without the item)
        # then priorize the locations depending on how many items required them, favor item with smallest list,
        # also priorize locs where placing an item invalidate their postAvailable
        # return the list of locations of higher priority
        postNokPriority = 1024 # have to be big, it's top priority to fill it else it will never be filled
        # higher priorities for useful items
        itemsPriorities = {
            'Boss': 10,
            'Progression': 5,
            'Beam': 5,
            'Misc': 5,
            'Ammo': 1,
            'Energy': 1,
            'Nothing': 0
        }

        priorityLocations = defaultdict(float)
        allLocations = set(self.container.unusedLocations)
        for it, data in itemLocDict.items():
            unreachableLocations = allLocations - set(data["availLocsWoItem"])
            self.log.debug("priority locs for {}: {} - {}".format(it.Type, len(unreachableLocations), [loc.Name for loc in unreachableLocations]))

            priority = itemsPriorities[it.Category]
            for loc in unreachableLocations:
                # lower priority if more locs have to be filled
                priorityLocations[loc] += priority / len(unreachableLocations)
            for loc in data["locsPostNokWoItem"]:
                self.log.debug("loc post nok wo {}: {}".format(it.Type, loc.Name))
                priorityLocations[loc] += postNokPriority

        # get list of locations for each priorities
        priorities = defaultdict(list)
        for loc, count in priorityLocations.items():
            priorities[count].append(loc)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            #for count, locs in priorities.items():
                #self.log.debug("priority {}: {}".format(round(count, 2), [loc.Name for loc in locs]))

            self.log.debug("max priority locations: {} - {}".format(round(max(priorities), 2), [loc.Name for loc in priorities[max(priorities) if priorities else 0]]))

        return priorities[max(priorities) if priorities else 0]

    def step(self, onlyBossCheck=False):
        self.log.debug("------------------------------------------------")
        self.log.debug("is earlyGame: {}".format(self.earlyGame))

        if self.can100percentReverse():
            (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
            itemLoc = ItemThenLocChoice.chooseItemLoc(self.choice, itemLocDict, False)
            assert itemLoc is not None
            self.log.debug("can100percent, fill with no logic")
            self.ap = self.services.collect(self.ap, self.container, itemLoc)
            return True

        # check only boss left
        self.onlyBossLeftLocations = self.services.getOnlyBossLeftLocationReverse(self.startAP, self.container)

        assumedItems = self.container.itemPool

        step = len(assumedItems)

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("remaining assumed items: {} - {}".format(step, getItemListStr(assumedItems)))
            self.log.debug("remaining locations: {}".format(len(self.container.unusedLocations) if len(self.container.unusedLocations) > 13 else [loc.Name for loc in self.container.unusedLocations]))
            self.log.debug("start ap: {}".format(self.ap))

        if len(self.onlyBossLeftLocations) > 0:
            self.log.debug("onlyBossLeftLocations not empty: {}, set maxDiff to infinity".format([loc.Name for loc in self.onlyBossLeftLocations]))
            maxDiff = infinity
        else:
            self.log.debug("onlyBossLeftLocations empty, set maxDiff to {}".format(self.services.settings.maxDiff))
            maxDiff = self.maxDiff

        # compute available locs without each item type from start ap
        itemLocDict = self.services.getPossiblePlacementsWithoutItem(self.startAP, self.ap, self.container, assumedItems, maxDiff)

        # debug display
        self.displayItemLocDict("before", itemLocDict)

        # keep only priority locations, locations that need to be filled to allow placement of an item
        # which will make other locations unreachable
        priorityLocations = set(self.getPriorityLocations(itemLocDict))

        if priorityLocations:
            # keep only priority locations
            for it, data in itemLocDict.items():
                data["possibleLocs"] = set(data["possibleLocs"]).intersection(priorityLocations)
            itemLocDict = {it: data for it, data in itemLocDict.items() if len(data['possibleLocs']) > 0}

        # keep only items where we still have step available locs after placing the item
        if not self.earlyGame:
            itemLocDict = {it: data for it, data in itemLocDict.items() if data['availLocsWoItemLen'] == step}

        if not itemLocDict:
            if not self.earlyGame:
                self.log.debug("no longer enforce that enough locs are available")
                self.earlyGame = True
                return True
            else:
                self.errorMsg = "No item with {} available locs after".format(step)
                self.log.debug(self.errorMsg)
                return False

        # debug display
        self.displayItemLocDict("after filter", itemLocDict)

        if len(self.alreadyTriedItems[step]) > 0:
            self.log.debug("self.alreadyTriedItems: {} / {}".format(len(self.alreadyTriedItems[step]), step))
            try:
                item = random.choice([it for it in itemLocDict.keys() if it not in self.alreadyTriedItems[step]])
            except IndexError:
                self.errorMsg = "Stucked after testing all items"
                return False
        else:
            if not self.earlyGame:
                # TODO::check if this doesn't create the same seeds:
                # choose first boss, then major, then ammo, then nothing
                boss = [it for it in itemLocDict.keys() if it.Category == 'Boss']
                remain = [it for it in itemLocDict.keys() if it.Category != 'Boss']
                #major = [it for it in itemLocDict.keys() if it.Category in ['Progression', 'Beam', 'Misc']]
                #ammo_energy = [it for it in itemLocDict.keys() if it.Category in ['Ammo', 'Energy']]
                #nothing = [it for it in itemLocDict.keys() if it.Category == 'Nothing']
                #self.log.debug("Available items: boss: {} major: {} ammo/energy: {} nothing: {}".format(len(boss), len(major), len(ammo_energy), len(nothing)))
                self.log.debug("Available items: boss: {} remain: {}".format(len(boss), len(remain)))

                items = boss if boss else remain
                self.log.debug("items in choice: {}".format([it.Type for it in items]))
            else:
                # choose between items with the highest number of available locs after
                maxAvailLocs = -1
                for it, data in itemLocDict.items():
                    if data["availLocsWoItemLen"] > maxAvailLocs:
                        maxAvailLocs = data["availLocsWoItemLen"]
                items = [it for it, data in itemLocDict.items() if data["availLocsWoItemLen"] == maxAvailLocs]

            item = random.choice(items)
        locations = list(itemLocDict[item]['possibleLocs'])
        self.log.debug("item chosen: {} - available locs: {}".format(item.Type, len(locations)))

        itemLoc = self.choice.chooseItemLoc({item: locations}, False)
        if itemLoc is None:
            self.log.debug("No remaining location for item {}".format(item.Type))
            self.alreadyTriedItems[step].add(item)
            return True
        self.log.debug("loc chosen: {}, difficulty: {}".format(itemLoc.Location.Name, itemLoc.Location.difficulty))

        self.collect(itemLoc)

        if itemLoc.Location in self.onlyBossLeftLocations:
            self.log.debug("Remove loc from onlyBossLeft locations")
            loc = itemLoc.Location
            if len(self.errorMsg) == 0:
                self.errorMsg = "Maximum difficulty could not be applied everywhere. Affected locations: "
            self.errorMsg += " {}: {}".format(loc.Name, diffValue2txt(self.onlyBossLeftLocations[loc]))
            del self.onlyBossLeftLocations[loc]

        self.log.debug("end ap: {}".format(self.ap))

        return True

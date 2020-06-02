
import copy, log

from parameters import Knows, isKnows, god
from smbool import SMBool
from rando.Filler import Filler
from rando.ItemLocContainer import ItemLocContainer, getItemListStr, getLocListStr

class ChozoFillerFactory(object):
    def __init__(self, graphSettings, areaGraph, restrictions, firstPhaseFact, secondPhaseFact):
        self.graphSettings = graphSettings
        self.areaGraph = areaGraph
        self.restrictions = restrictions
        self.firstPhaseFact = firstPhaseFact
        self.secondPhaseFact = secondPhaseFact

    def createFirstPhaseFiller(self, container):
        return self.firstPhaseFact(self.graphSettings, self.areaGraph, self.restrictions, container)

    def createSecondPhaseFiller(self, container, firstPhaseProg):
        return self.secondPhaseFact(self.graphSettings, self.areaGraph, self.restrictions, container, firstPhaseProg)

class ChozoWrapperFiller(Filler):
    def __init__(self, settings, container, fillerFactory):
        self.settings = settings
        self.maxDiff = self.settings.maxDiff
        self.baseContainer = container
        self.fillerFactory = fillerFactory
        self.log = log.get('ChozoWrapperFiller')

    def prepareFirstPhase(self):
        self.changedKnows = {}
        # forces IceZebSkip if necessary to finish with 10-10-5
        if Knows.IceZebSkip.bool == False or Knows.IceZebSkip.difficulty > self.maxDiff:
            self.changedKnows['IceZebSkip'] = Knows.IceZebSkip
            Knows.IceZebSkip = SMBool(True, 0, [])
        # hack knows to remove those > maxDiff
        for attr,k in Knows.__dict__.items():
            if isKnows(attr) and k.bool == True and k.difficulty > self.maxDiff:
                self.log.debug("prepareFirstPhase. disabling knows "+attr)
                self.changedKnows[attr] = k
                setattr(Knows, attr, SMBool(False, 0))
        # set max diff to god (for hard rooms/hellruns/bosses)
        self.settings.maxDiff = god
        # prepare 1st phase container
        itemCond = lambda item: item['Class'] == 'Chozo' or item['Category'] == 'Boss'
        locCond = lambda loc: 'Chozo' in loc['Class'] or 'Boss' in loc['Class']
        # this will create a new smbm with new knows functions
        cont = self.baseContainer.slice(itemCond, locCond)
        secondPhaseItems = [item for item in self.baseContainer.itemPool if item not in cont.itemPool]
        contLocs = self.baseContainer.extractLocs(cont.unusedLocations)
        secondPhaseLocs = [loc for loc in self.baseContainer.unusedLocations if loc not in contLocs]
        self.log.debug("prepareFirstPhase. secondPhaseItems="+getItemListStr(secondPhaseItems))
        self.log.debug("prepareFirstPhase. secondPhaseLocs="+getLocListStr(secondPhaseLocs))
        self.secondPhaseContainer = ItemLocContainer(cont.sm, secondPhaseItems, secondPhaseLocs)
        return self.fillerFactory.createFirstPhaseFiller(cont)

    def prepareSecondPhase(self, firstCont, progItemLocs):
        # restore knows and max diff
        for k,b in self.changedKnows.items():
            setattr(Knows, k, b)
        self.settings.maxDiff = self.maxDiff
        # transfer stuff to second container
        cont = copy.copy(self.secondPhaseContainer)
        firstCont.transferCollected(cont)
        self.log.debug("prepareSecondPhase. container="+cont.dump())
        return self.fillerFactory.createSecondPhaseFiller(cont, progItemLocs)

    def generateItems(self, vcr=None):
        filler = self.prepareFirstPhase()
        (isStuck, itemLocations, progItemLocs) = filler.generateItems(vcr=vcr)
        if isStuck:
            self.errorMsg = filler.errorMsg
            return (isStuck, itemLocations, progItemLocs)
        self.settings.runtimeLimit_s -= filler.runtime_s
        filler = self.prepareSecondPhase(filler.container, progItemLocs)
        (isStuck, itemLocations, secondProg) = filler.generateItems(vcr=vcr)
        self.errorMsg = filler.errorMsg
        return (isStuck, itemLocations, progItemLocs)

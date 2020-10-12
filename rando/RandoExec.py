
import sys, random, time

from graph.graph_locations import locations as graphLocations
from rando.Restrictions import Restrictions
from rando.RandoServices import RandoServices
from rando.GraphBuilder import GraphBuilder
from rando.RandoSetup import RandoSetup
from rando.Filler import FrontFiller
from rando.FillerProgSpeed import FillerProgSpeed, FillerProgSpeedChozoSecondPhase
from rando.FillerRandom import FillerRandom, FillerRandomSpeedrun
from rando.FillerAssumed import ReverseFiller
from rando.Chozo import ChozoFillerFactory, ChozoWrapperFiller
from rando.Items import ItemManager
from rando.ItemLocContainer import ItemLocation
from utils.vcr import VCR
from utils.doorsmanager import DoorsManager

# entry point for rando execution ("randomize" method)
class RandoExec(object):
    def __init__(self, seedName, vcr):
        self.errorMsg = ""
        self.seedName = seedName
        self.vcr = vcr

    def getFillerFactory(self, progSpeed, endDate):
        if progSpeed == "basic":
            return lambda graphSettings, graph, restr, cont: FrontFiller(graphSettings.startAP, graph, restr, cont, endDate)
        elif progSpeed == "speedrun":
            return lambda graphSettings, graph, restr, cont: FillerRandomSpeedrun(graphSettings, graph, restr, cont, endDate)
        elif progSpeed == "reverse":
            return lambda graphSettings, graph, restr, cont: ReverseFiller(graphSettings, graph, restr, cont, endDate)
        else:
            return lambda graphSettings, graph, restr, cont: FillerProgSpeed(graphSettings, graph, restr, cont, endDate)

    def createFiller(self, randoSettings, graphSettings, container, endDate):
        fact = self.getFillerFactory(randoSettings.progSpeed, endDate)
        if self.restrictions.split != "Chozo":
            return fact(graphSettings, self.areaGraph, self.restrictions, container)
        else:
            if randoSettings.progSpeed in ['basic', 'speedrun']:
                secondPhase = lambda graphSettings, graph, restr, cont, prog: FillerRandom(graphSettings.startAP, graph, restr, cont, endDate, diffSteps=100)
            else:
                secondPhase = lambda graphSettings, graph, restr, cont, prog: FillerProgSpeedChozoSecondPhase(graphSettings.startAP, graph, restr, cont, endDate)
            chozoFact = ChozoFillerFactory(graphSettings, self.areaGraph, self.restrictions, fact, secondPhase)
            return ChozoWrapperFiller(randoSettings, container, chozoFact)

    # processes settings to :
    # - create Restrictions and GraphBuilder objects
    # - create graph and item loc container using a RandoSetup instance: in area rando, if it fails, iterate on possible graph layouts
    # - create filler based on progression speed and run it
    # return (isStuck, itemLocs, progItemLocs)
    def randomize(self, randoSettings, graphSettings):
        self.restrictions = Restrictions(randoSettings)
        self.errorMsg = ""
        graphBuilder = GraphBuilder(graphSettings)
        container = None
        i = 0
        attempts = 500 if graphSettings.areaRando else 1
        now = time.process_time()
        endDate = sys.maxsize
        if randoSettings.runtimeLimit_s < endDate:
            endDate = now + randoSettings.runtimeLimit_s
        while container is None and i < attempts and now <= endDate:
            if graphSettings.doorsColorsRando == True:
                DoorsManager.randomize()
            self.areaGraph = graphBuilder.createGraph()
            services = RandoServices(self.areaGraph, self.restrictions)
            setup = RandoSetup(graphSettings, graphLocations, services)
            container = setup.createItemLocContainer()
            if container is None:
                sys.stdout.write('*')
                sys.stdout.flush()
                i += 1
            else:
                self.errorMsg += '\n'.join(setup.errorMsgs)
            now = time.process_time()
        if container is None:
            if graphSettings.areaRando:
                self.errorMsg += "Could not find an area layout with these settings"
            else:
                self.errorMsg += "Unable to process settings"
            return (True, [], [])
        graphBuilder.escapeGraph(container, self.areaGraph, randoSettings.maxDiff)
        self.areaGraph.printGraph()
        filler = self.createFiller(randoSettings, graphSettings, container, endDate)
        vcr = VCR(self.seedName, 'rando') if self.vcr == True else None
        ret = filler.generateItems(vcr=vcr)
        self.errorMsg = filler.errorMsg + '\n' + self.errorMsg
        return ret

    def postProcessItemLocs(self, itemLocs, hide):
        # hide some items like in dessy's
        if hide == True:
            for itemLoc in itemLocs:
                item = itemLoc.Item
                loc = itemLoc.Location
                if (item.Type not in ['Nothing', 'NoEnergy']
                    and loc.CanHidden == True
                    and loc.Visibility == 'Visible'):
                    if bool(random.getrandbits(1)) == True:
                        loc.Visibility = 'Hidden'
        # put nothing in unfilled locations
        filledLocNames = [il.Location.Name for il in itemLocs]
        unfilledLocs = [loc for loc in graphLocations if loc.Name not in filledLocNames]
        nothing = ItemManager.getItem('Nothing')
        for loc in unfilledLocs:
            loc.restricted = True
            itemLocs.append(ItemLocation(nothing, loc, False))

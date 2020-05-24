
import sys

from graph_locations import locations as graphLocations
from rando.Restrictions import Restrictions
from rando.RandoServices import RandoServices
from rando.GraphBuilder import GraphBuilder
from rando.RandoSetup import RandoSetup
from rando.Filler import FrontFiller
from rando.FillerProgSpeed import FillerProgSpeed
from rando.FillerRandom import FillerRandom
from rando.Chozo import ChozoFillerFactory, ChozoWrapperFiller
from vcr import VCR

class RandoExec(object):
    def __init__(self, seedName, vcr):
        self.errorMsg = ""
        self.seedName = seedName
        self.vcr = vcr

    def getFillerFactory(self, progSpeed):
        if progSpeed == "basic":
            return lambda graphSettings, graph, restr, cont: FrontFiller(graphSettings.startAP, graph, restr, cont)
        elif progSpeed == "speedrun":
            return lambda graphSettings, graph, restr, cont: FillerRandom(graphSettings.startAP, graph, restr, cont)
        else:
            return lambda graphSettings, graph, restr, cont: FillerProgSpeed(graphSettings, graph, restr, cont)

    def createFiller(self, randoSettings, graphSettings, container):
        fact = self.getFillerFactory(randoSettings.progSpeed)
        if self.restrictions.split != "Chozo":
            return fact(graphSettings, self.areaGraph, self.restrictions, container)
        else:
#            if randoSettings.progSpeed in ['basic', 'speedrun']:
            secondPhase = lambda graphSettings, graph, restr, cont, prog: FillerRandom(graphSettings.startAP, graph, restr, cont, diffSteps=100)
            # TODO 2nd phase for progression speed
            chozoFact = ChozoFillerFactory(graphSettings, self.areaGraph, self.restrictions, fact, secondPhase)
            return ChozoWrapperFiller(randoSettings, container, chozoFact)
        # TODO plando/rando ??

    # processes settings to build appropriate objects, run appropriate stuff
    # return (isStuck, itemLocs, progItemLocs)
    def randomize(self, randoSettings, graphSettings):
        self.restrictions = Restrictions(randoSettings)
        graphBuilder = GraphBuilder(graphSettings)
        container = None
        i = 0
        attempts = 500 if graphSettings.areaRando else 1
        while container is None and i < attempts:
            self.areaGraph = graphBuilder.createGraph()
            services = RandoServices(self.areaGraph, self.restrictions)
            setup = RandoSetup(graphSettings, graphLocations, services)
            container = setup.createItemLocContainer()
            if container is None:
                sys.stdout.write('*')
                sys.stdout.flush()
                i += 1
        if container is None:
            self.errorMsg = "Could not find an area layout with these settings"
            return (True, [], [])
        graphBuilder.escapeGraph(container, self.areaGraph, randoSettings.maxDiff)
        filler = self.createFiller(randoSettings, graphSettings, container)
        vcr = VCR(self.seedName, 'rando') if self.vcr == True else None
        ret = filler.generateItems(vcr=vcr)
        self.errorMsg = filler.errorMsg
        return ret

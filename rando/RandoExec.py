
import sys

from graph_locations import locations as graphLocations
from rando.Restrictions import Restrictions
from rando.RandoServices import RandoServices
from rando.GraphBuilder import GraphBuilder
from rando.RandoSetup import RandoSetup
from rando.Filler import FrontFiller
from rando.FillerProgSpeed import FillerProgSpeed

class RandoExec(object):
    def __init__(self):
        self.errorMsg = ""

    def createFiller(self, randoSettings, graphSettings):
        if randoSettings.progSpeed == 'basic':
            return FrontFiller(graphSettings.startAP, self.areaGraph, self.restrictions, self.container)
        elif randoSettings.progSpeed == 'speedrun':
            # TODO random filler with solver
            pass
        else:
            return FillerProgSpeed(graphSettings, self.areaGraph, self.restrictions, self.container)
        # TODO handle chozo here with chozo "wrapper filler"
        # TODO same for plando/rando ??

    # processes settings to build appropriate objects, run appropriate stuff
    # return (isStuck, itemLocs, progItemLocs)
    def randomize(self, randoSettings, graphSettings):
        self.restrictions = Restrictions(randoSettings)
        graphBuilder = GraphBuilder(graphSettings)
        self.container = None
        i = 0
        attempts = 500 if graphSettings.areaRando else 1
        while self.container is None and i < attempts:
            self.areaGraph = graphBuilder.createGraph()
            services = RandoServices(self.areaGraph, self.restrictions)
            setup = RandoSetup(graphSettings.startAP, graphLocations, services)
            self.container = setup.createItemLocContainer()
            if self.container is None:
                sys.stdout.write('*')
                sys.stdout.flush()
                i += 1
        if self.container is None:
            self.errorMsg = "Could not find an area layout with these settings"
            return (True, [], [])
        graphBuilder.escapeGraph(self.container, self.areaGraph, randoSettings.maxDiff)
        filler = self.createFiller(randoSettings, graphSettings)
        ret = filler.generateItems()
        self.errorMsg = filler.errorMsg
        return ret

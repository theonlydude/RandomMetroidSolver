
import sys

from graph_locations import locations as graphLocations
from rando.Restrictions import Restrictions
from rando.RandoServices import RandoServices
from rando.GraphBuilder import GraphBuilder
from rando.RandoSetup import RandoSetup
from rando.Filler import FrontFiller

class RandoExec(object):
    def __init__(self):
        self.errorMsg = ""

    # TODO factory methods to generate objects given settings
    
    # processes settings to build appropriate objects, run appropriate stuff
    # return (isStuck, itemLocs, progItemLocs)
    def randomize(self, randoSettings, graphSettings):
        restrictions = Restrictions(randoSettings)
        graphBuilder = GraphBuilder(graphSettings)
        container = None
        i = 0
        attempts = 500 if graphSettings.areaRando else 1
        while container is None and i < attempts:
            self.areaGraph = graphBuilder.createGraph()
            services = RandoServices(self.areaGraph, restrictions)
            setup = RandoSetup(graphSettings.startAP, graphLocations, services)
            container = setup.createItemLocContainer()
            if container is None:
                sys.stdout.write('*')
                sys.stdout.flush()
                i += 1
        if container is None:
            self.errorMsg = "Could not find an area layout with these settings"
            return (True, [], [])
        graphBuilder.escapeGraph(container, self.areaGraph, randoSettings.maxDiff)
        filler = FrontFiller(graphSettings.startAP, self.areaGraph, restrictions, container)
        ret = filler.generateItems()
        self.errorMsg = filler.errorMsg
        return ret

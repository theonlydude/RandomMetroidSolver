

from graph_locations import locations as graphLocations
from rando.Restrictions import Restrictions
from rando.RandoServices import RandoServices
from rando.GraphBuilder import GraphBuilder
from rando.RandoSetup import RandoSetup
from rando.Fillers import FrontFiller

# processes settings to build appropriate objects, run appropriate stuff
# return (isStuck, itemLocs, progItemLocs)
def randomize(randoSettings, graphSettings):
    restrictions = Restrictions(randoSettings)
    graphBuilder = GraphBuilder(graphSettings)
    container = None
    i = 0
    attempts = 500 if graphSettings.areaRando else 1
    while container is None and i < attempts:
        graph = graphBuilder.createGraph()
        services = RandoServices(graph, restrictions)
        setup = RandoSetup(graphSettings.startAP, graphLocations, services)
        container = setup.createItemLocContainer()
        if container is None:
            sys.stdout.write('*')
            sys.stdout.flush()
        i += 1
    if container is None:
        # TODO handle error messages
        return (True, [], [])
    filler = FrontFiller(graphSettings.startAP, graph, restrictions, container)
    return filler.generateItems()

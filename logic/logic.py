# entry point for the logic implementation
import copy

class Logic(object):
    _locationsCopy = None
    _locationsDictCopy = None
    _accessPointsCopy = None
    _accessPointsDictCopy = None

    @staticmethod
    def factory(implementation, new=False):
        if implementation == 'vanilla':
            from graph.vanilla.graph_helpers import HelpersGraph
            from graph.vanilla.graph_access import accessPoints, accessPointsDict
            from graph.vanilla.graph_locations import locations, LocationsHelper, postLoad, locationsDict
            import graph.vanilla.map_tiles
            import graph.vanilla.map_tilecount
            import graph.vanilla.boss_doors
            Logic.map_tiles = graph.vanilla.map_tiles
            Logic.map_tilecount = graph.vanilla.map_tilecount.tilecount
            Logic.boss_doors = graph.vanilla.boss_doors.boss_doors
            Logic._locations = locations
            Logic._locationsDict = locationsDict
            Logic._accessPoints = accessPoints
            Logic._accessPointsDict = accessPointsDict
            Logic.HelpersGraph = HelpersGraph
            Logic.patches = implementation
            Logic.LocationsHelper = LocationsHelper
            Logic.postSymbolsLoad = postLoad
        elif implementation == 'mirror':
            from graph.mirror.graph_helpers import HelpersGraphMirror as HelpersGraph
            from graph.mirror.graph_access import accessPoints, accessPointsDict
            from graph.mirror.graph_locations import locations, LocationsHelper, postLoad, locationsDict
            import graph.mirror.map_tiles
            import graph.mirror.map_tilecount
            import graph.mirror.boss_doors
            Logic.map_tiles = graph.mirror.map_tiles
            Logic.map_tilecount = graph.mirror.map_tilecount.tilecount
            Logic.boss_doors = graph.mirror.boss_doors.boss_doors
            Logic._locations = locations
            Logic._locationsDict = locationsDict
            Logic._accessPoints = accessPoints
            Logic._accessPointsDict = accessPointsDict
            Logic.HelpersGraph = HelpersGraph
            Logic.patches = implementation
            Logic.LocationsHelper = LocationsHelper
            Logic.postSymbolsLoad = postLoad
        else:
            raise ValueError("Unknown logic type : "+str(implementation))
        Logic.implementation = implementation

        if new:
            # used by isolver which will run several times in the same process,
            # so we need a fresh copy every time
            Logic._locationsCopy = copy.deepcopy(Logic._locations)
            Logic._locationsDictCopy = {loc.Name: loc for loc in Logic._locationsCopy}
            Logic._accessPointsCopy = copy.deepcopy(Logic._accessPoints)
            Logic._accessPointsDictCopy = copy.deepcopy(Logic._accessPointsDict)

    @staticmethod
    def list():
        return ['vanilla', 'mirror']

    @staticmethod
    def locations():
        if Logic._locationsCopy is not None:
            return Logic._locationsCopy
        else:
            return Logic._locations

    @staticmethod
    def locationsDict():
        if Logic._locationsDictCopy is not None:
            return Logic._locationsDictCopy
        else:
            return Logic._locationsDict

    @staticmethod
    def accessPoints():
        if Logic._accessPointsCopy is not None:
            return Logic._accessPointsCopy
        else:
            return Logic._accessPoints

    @staticmethod
    def accessPointsDict():
        if Logic._accessPointsDictCopy is not None:
            return Logic._accessPointsDictCopy
        else:
            return Logic._accessPointsDict

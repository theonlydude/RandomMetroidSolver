# entry point for the logic implementation

class Logic(object):
    @staticmethod
    def factory(implementation):
        if implementation == 'vanilla':
            from graph.vanilla.graph_helpers import HelpersGraph
            from graph.vanilla.graph_access import accessPoints
            from graph.vanilla.graph_locations import locations
            from graph.vanilla.graph_locations import LocationsHelper
            import graph.vanilla.map_tiles
            Logic.map_tiles = graph.vanilla.map_tiles
            Logic.locations = locations
            Logic.accessPoints = accessPoints
            Logic.HelpersGraph = HelpersGraph
            Logic.patches = implementation
            Logic.LocationsHelper = LocationsHelper
            Logic.postSymbolsLoad = lambda: None
        elif implementation == 'rotation':
            from graph.rotation.graph_helpers import HelpersGraph
            from graph.rotation.graph_access import accessPoints
            from graph.rotation.graph_locations import locations
            from graph.rotation.graph_locations import LocationsHelper
            Logic.locations = locations
            Logic.accessPoints = accessPoints
            Logic.HelpersGraph = HelpersGraph
            Logic.patches = implementation
            Logic.LocationsHelper = LocationsHelper
        elif implementation == 'mirror':
            from graph.mirror.graph_helpers import HelpersGraphMirror as HelpersGraph
            from graph.mirror.graph_access import accessPoints
            from graph.mirror.graph_locations import locations, LocationsHelper, fixLocAddresses
            import graph.mirror.map_tiles
            Logic.map_tiles = graph.mirror.map_tiles
            Logic.locations = locations
            Logic.accessPoints = accessPoints
            Logic.HelpersGraph = HelpersGraph
            Logic.patches = implementation
            Logic.LocationsHelper = LocationsHelper
            Logic.postSymbolsLoad = fixLocAddresses
        else:
            raise ValueError("Unknown logic type : "+str(implementation))
        Logic.implementation = implementation

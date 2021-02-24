# entry point for the logic implementation

class Logic(object):
    @staticmethod
    def factory(implementation):
        if implementation == 'varia':
            from graph.varia.graph_helpers import HelpersGraph
            from graph.varia.graph_access import accessPoints
            from graph.varia.graph_locations import locations
            Logic.locations = locations
            Logic.accessPoints = accessPoints
            Logic.HelpersGraph = HelpersGraph
            Logic.patches = implementation
        elif implementation == 'rotation':
            from graph.rotation.graph_helpers import HelpersGraph
            from graph.rotation.graph_access import accessPoints
            from graph.rotation.graph_locations import locations
            Logic.locations = locations
            Logic.accessPoints = accessPoints
            Logic.HelpersGraph = HelpersGraph
            Logic.patches = implementation
        Logic.implementation = implementation

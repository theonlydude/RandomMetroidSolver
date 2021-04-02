# entry point for the logic implementation

class Logic(object):
    @staticmethod
    def factory(implementation):
        if implementation == 'varia':
            from graph.varia.graph_helpers import HelpersGraph
            from graph.varia.graph_access import accessPoints
            from graph.varia.graph_locations import locations
            from utils.varia.settings import SettingsVaria as Settings
        elif implementation == 'rotation':
            from graph.rotation.graph_helpers import HelpersGraph
            from graph.rotation.graph_access import accessPoints
            from graph.rotation.graph_locations import locations
            from utils.rotation.settings import SettingsRotation as Settings
        Logic.locations = locations
        Logic.accessPoints = accessPoints
        Logic.HelpersGraph = HelpersGraph
        Logic.patches = implementation
        # update settings with custom values
        Settings.update()
        Logic.Settings = Settings
        Logic.implementation = implementation

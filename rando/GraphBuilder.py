
import log,random

from graph_access import GraphUtils, vanillaTransitions, vanillaBossesTransitions, accessPoints, escapeSource, escapeTargets
from graph import AccessGraph

class GraphBuilder(object):
    def __init__(self, graphSettings):
        self.graphSettings = graphSettings
        self.areaRando = graphSettings.areaRando
        self.bossRando = graphSettings.bossRando
        self.escapeRando = graphSettings.escapeRando
        self.log = log.get('GraphBuilder')

    # builds everything but escape transitions
    def createGraph(self, transitions=None):
        if transitions is None:
            transitions = []
            if not self.bossRando:
                transitions += vanillaBossesTransitions
            else:
                transitions += GraphUtils.createBossesTransitions()
            if not self.areaRando:
                transitions += vanillaTransitions
            else:
                transitions += GraphUtils.createAreaTransitions(self.graphSettings.bidir)
        return AccessGraph(accessPoints, transitions,
                           self.graphSettings.bidir, self.graphSettings.dotFile)

    def escapeGraph(self, emptyContainer, graph, maxDiff):
        if not self.escapeRando:
            return
        possibleTargets, dst, path = self.getPossibleEscapeTargets(emptyContainer, graph, maxDiff)
        # update graph with escape transition
        graph.addTransition(escapeSource, dst)
        # get timer value
        self.escapeTimer(graph, path)
        self.log.debug("escapeGraph: ({}, {}) timer: {}".format(escapeSource, dst, graph.EscapeAttributes['Timer']))
        # animals
        GraphUtils.escapeAnimalsTransitions(graph, possibleTargets, dst)

    def getPossibleEscapeTargets(self, emptyContainer, graph, maxDiff):
        sm = emptyContainer.sm
        # setup smbm with item pool
        sm.resetItems()
        # Ice not usable because of hyper beam
        # remove energy to avoid hell runs
        # (will add bosses as well)
        sm.addItems([item['Type'] for item in emptyContainer.itemPool if item['Type'] != 'Ice' and item['Category'] != 'Energy'])
        possibleTargets = [target for target in escapeTargets if graph.accessPath(sm, target, 'Landing Site', maxDiff) is not None]
        # failsafe
        if len(possibleTargets) == 0:
            possibleTargets.append('Climb Bottom Left')
        random.shuffle(possibleTargets)
        # pick one
        dst = possibleTargets.pop()
        path = graph.accessPath(sm, dst, 'Landing Site', maxDiff)
        # cleanup smbm
        sm.resetItems()
        return (possibleTargets, dst, path)

    # path: as returned by AccessGraph.accessPath
    def escapeTimer(self, graph, path):
        if self.areaRando == True:
            if path[0].Name == 'Climb Bottom Left':
                self.log.debug('escapeTimer: vanilla')
                return None
            traversedAreas = list(set([ap.GraphArea for ap in path]))
            self.log.debug("escapeTimer path: " + str([ap.Name for ap in path]))
            self.log.debug("escapeTimer traversedAreas: " + str(traversedAreas))
            # rough estimates of navigation within areas to reach "borders"
            # (can obviously be completely off wrt to actual path, but on the generous side)
            traversals = {
                'Crateria':90,
                'GreenPinkBrinstar':90,
                'WreckedShip':120,
                'LowerNorfair':135,
                'Maridia':150,
                'RedBrinstar':75,
                'Norfair': 120,
                # Kraid and Tourian can't be on the path
                'Kraid': 0,
                'Tourian': 0
            }
            t = 90
            for area in traversedAreas:
                t += traversals[area]
            t = max(t, 180)
        else:
            escapeTargetsTimer = {
                'Climb Bottom Left': None, # vanilla
                'Green Brinstar Main Shaft Top Left': 210, # brinstar
                'Basement Left': 210, # wrecked ship
                'Business Center Mid Left': 270, # norfair
                'Crab Hole Bottom Right': 270 # maridia
            }
            t = escapeTargetsTimer[path[0].Name]
        self.log.debug("escapeTimer. t="+str(t))
        graph.EscapeAttributes['Timer'] = t

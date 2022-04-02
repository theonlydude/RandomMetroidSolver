
import utils.log, random, copy

from graph.graph_utils import GraphUtils, vanillaTransitions, vanillaBossesTransitions, escapeSource, escapeTargets
from logic.logic import Logic
from graph.graph import AccessGraphRando as AccessGraph
from utils.objectives import Objectives
from rando.ItemLocContainer import getItemLocStr

# creates graph and handles randomized escape
class GraphBuilder(object):
    def __init__(self, graphSettings):
        self.graphSettings = graphSettings
        self.areaRando = graphSettings.areaRando
        self.bossRando = graphSettings.bossRando
        self.escapeRando = graphSettings.escapeRando
        self.minimizerN = graphSettings.minimizerN
        self.log = utils.log.get('GraphBuilder')

    # builds everything but escape transitions
    def createGraph(self):
        transitions = self.graphSettings.plandoRandoTransitions
        if transitions is None:
            transitions = []
            if self.minimizerN is not None:
                transitions = GraphUtils.createMinimizerTransitions(self.graphSettings.startAP, self.minimizerN)
            else:
                if not self.bossRando:
                    transitions += vanillaBossesTransitions
                else:
                    transitions += GraphUtils.createBossesTransitions()
                if not self.areaRando:
                    transitions += vanillaTransitions
                else:
                    transitions += GraphUtils.createAreaTransitions(self.graphSettings.lightAreaRando)
        return AccessGraph(Logic.accessPoints, transitions, self.graphSettings.dotFile)

    # fills in escape transitions if escape rando is enabled
    # escapeTrigger = None or (itemLocs, progItemlocs) couple from filler
    def escapeGraph(self, container, graph, maxDiff, escapeTrigger):
        if not self.escapeRando:
            return True
        emptyContainer = copy.copy(container)
        emptyContainer.resetCollected(reassignItemLocs=True)
        dst = None
        if escapeTrigger is None:
            possibleTargets, dst, path = self.getPossibleEscapeTargets(emptyContainer, graph, maxDiff)
            # update graph with escape transition
            graph.addTransition(escapeSource, dst)
        else:
            possibleTargets, path = self.escapeTrigger(emptyContainer, graph, maxDiff, escapeTrigger)
            if path is None:
                return False
        # get timer value
        self.escapeTimer(graph, path, self.areaRando or escapeTrigger is not None)
        self.log.debug("escapeGraph: ({}, {}) timer: {}".format(escapeSource, dst, graph.EscapeAttributes['Timer']))
        # animals
        GraphUtils.escapeAnimalsTransitions(graph, possibleTargets, dst)
        return True

    def _getTargets(self, sm, graph, maxDiff):
        possibleTargets = [target for target in escapeTargets if graph.accessPath(sm, target, 'Landing Site', maxDiff) is not None]
        self.log.debug('_getTargets. targets='+str(possibleTargets))
        # failsafe
        if len(possibleTargets) == 0:
            self.log.debug("Can't randomize escape, fallback to vanilla")
            possibleTargets.append('Climb Bottom Left')
        random.shuffle(possibleTargets)
        return possibleTargets

    def getPossibleEscapeTargets(self, emptyContainer, graph, maxDiff):
        sm = emptyContainer.sm
        # setup smbm with item pool
        # Ice not usable because of hyper beam
        # remove energy to avoid hell runs
        # (will add bosses as well)
        sm.addItems([item.Type for item in emptyContainer.itemPool if item.Type != 'Ice' and item.Category != 'Energy'])
        sm.addItem('Hyper')
        possibleTargets = self._getTargets(sm, graph, maxDiff)
        # pick one
        dst = possibleTargets.pop()
        path = graph.accessPath(sm, dst, 'Landing Site', maxDiff)
        return (possibleTargets, dst, path)

    def escapeTrigger(self, emptyContainer, graph, maxDiff, escapeTrigger):
        sm = emptyContainer.sm
        itemLocs,progItemLocs,split = escapeTrigger[0],escapeTrigger[1],escapeTrigger[2]
        # filter garbage itemLocs
        ilCheck = lambda il: not il.Location.isBoss() and not il.Location.restricted and il.Item.Category != "Nothing"
        itemLocs = [il for il in itemLocs if ilCheck(il)]
        # update item% objectives
        nAccessibleItems = len(itemLocs)
        sm.objectives.setItemPercentFuncs(nAccessibleItems)
        if split == "Scavenger":
            # update escape access for scav with last scav loc
            lastScavItemLoc = progItemLocs[-1]
            sm.objectives.updateScavengerEscapeAccess(lastScavItemLoc.Location.accessPoint)
            sm.objectives.setScavengerHuntFunc(lambda sm: sm.haveItem(lastScavItemLoc.Item.Type))
        self.log.debug("escapeTrigger. collect locs until G4 access")
        # collect all item/locations up until we can pass G4
        for il in itemLocs:
            self.log.debug("collecting " + getItemLocStr(il))
            emptyContainer.collect(il)
            if sm.canPassG4():
                break
        # final update of item% obj
        sm.objectives.updateItemPercentEscapeAccess(list({il.Location.accessPoint for il in emptyContainer.itemLocations}))
        possibleTargets = self._getTargets(sm, graph, maxDiff)
        # try to escape from all the possible objectives APs
        possiblePaths = []
        for goal in Objectives.activeGoals:
            n, possibleAccessPoints = goal.escapeAccessPoints
            count = 0
            for ap in possibleAccessPoints:
                self.log.debug("escapeTrigger. testing AP " + ap)
                path = graph.accessPath(sm, ap, 'Landing Site', maxDiff)
                if path is not None:
                    possiblePaths.append(path)
                    count += 1
            if count < n:
                # there is a goal we cannot escape from
                self.log.debug("escapeTrigger. goal %s: found %d/%d possible escapes, abort" % (goal.name, count, n))
                return (None, None)
        # pick the longest possible path
        path = max(possiblePaths, key=lambda p: self._computeTimer(graph, p))
        return (possibleTargets, path)

    def _computeTimer(self, graph, path):
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
            'WestMaridia':75,
            'EastMaridia':100,
            'RedBrinstar':75,
            'Norfair': 120,
            'Kraid': 40,
            'Crocomire': 40,
            # can't be on the path
            'Tourian': 0,
        }
        t = 90 if self.areaRando else 0
        for area in traversedAreas:
            t += traversals[area]
        t = max(t, 180)
        return t

    # path: as returned by AccessGraph.accessPath
    def escapeTimer(self, graph, path, compute):
        if compute == True:
            if path[0].Name == 'Climb Bottom Left':
                graph.EscapeAttributes['Timer'] = None
                return
            t = self._computeTimer(graph, path)
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

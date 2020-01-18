import random, sys

from itemrandomizerweb.Randomizer import Randomizer
from graph_access import GraphUtils
from helpers import Bosses

class AreaRandomizer(Randomizer):
    def __init__(self, locations, settings, seedName, bossTransitions,
                 bidir=True, dotDir=None, escape=True, removeEscapeEnemies=True):
        transitionsOk = False
        attempts = 0
        while not transitionsOk and attempts < 500:
            try:
                self.transitions = GraphUtils.createAreaTransitions(bidir)
                super(AreaRandomizer, self).__init__(locations,
                                                     settings,
                                                     seedName,
                                                     self.transitions + bossTransitions,
                                                     bidir,
                                                     dotDir)
                if escape == True:
                    self.escapeGraph()
                transitionsOk = True
            except RuntimeError:
                transitionsOk = False
                sys.stdout.write('*')
                sys.stdout.flush()
                attempts += 1
        if not transitionsOk:
            raise RuntimeError("Impossible seed! (too much fun in the settings, probably)")

    # adapt restrictions implementation to different area layout

    def areaDistance(self, loc, otherLocs):
        return self.areaDistanceProp(loc, otherLocs, 'GraphArea')

    # area graph update for randomized escape
    def escapeGraph(self):
        sm = self.smbm
        # setup smbm with item pool
        sm.resetItems()
        for boss in Bosses.bosses():
            Bosses.beatBoss(boss)
        # Ice not usable because of hyper beam
        # remove energy to avoid hell runs
        sm.addItems([item['Type'] for item in self.itemPool if item['Type'] != 'Ice' and item['Category'] != 'Energy'])
        path = None
        while path is None:
            (src, dst) = GraphUtils.createEscapeTransition()
            path = self.areaGraph.accessPath(sm, dst, 'Landing Site',
                                             self.difficultyTarget)
        # cleanup smbm
        sm.resetItems()
        Bosses.reset()
        # actually update graph
        self.areaGraph.addTransition(src, dst)
        # get timer value
        self.areaGraph.EscapeTimer = self.escapeTimer(path)

    # really rough, to be accurate it would require traversal times for all APs
    # combinations within areas
    def escapeTimer(self, path):
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
        }
        t = 90
        for area in traversedAreas:
            t += traversals[area]
        self.log.debug("escapeTimer. t="+str(t))
        return max(t, 180)

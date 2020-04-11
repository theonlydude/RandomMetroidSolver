import random, sys

from itemrandomizerweb.Randomizer import Randomizer
from graph_access import GraphUtils
from helpers import Bosses

class AreaRandomizer(Randomizer):
    def __init__(self, locations, settings, seedName, bossTransitions,
                 bidir=True, dotDir=None):
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
                transitionsOk = True
            except RuntimeError:
                transitionsOk = False
                sys.stdout.write('*')
                sys.stdout.flush()
                attempts += 1
        if not transitionsOk:
            raise RuntimeError("Impossible seed! (too much fun in the settings, probably)")

    # adapt restrictions implementation to different area layout
    def computeLateMorphLimitCheck(self):
        # TODO::allow lateMorphOutStartArea check for custom starts which doesn't require morph early
        if (self.lateMorphOutStartArea == False and self.stdStart == True
            and self.restrictions['MajorMinor'] == 'Full' and self.restrictions['Suits'] == False):
            # we can do better
            raise RuntimeError('Invalid layout for late morph')

    def areaDistance(self, loc, otherLocs):
        return self.areaDistanceProp(loc, otherLocs, 'GraphArea')

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
            'Kraid': 0,
            'Tourian': 0
        }
        t = 90
        for area in traversedAreas:
            t += traversals[area]
        self.log.debug("escapeTimer. t="+str(t))
        self.areaGraph.EscapeAttributes['Timer'] = max(t, 180)

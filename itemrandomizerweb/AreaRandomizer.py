import random

from itemrandomizerweb.Randomizer import Randomizer
from graph_access import vanillaTransitions, accessPoints, getAccessPoint, createAreaTransitions

class AreaRandomizer(Randomizer):
    def __init__(self, locations, settings, seedName, bossTransitions, bidir=True, dotDir=None):
        transitionsOk = False
        attempts = 0
        while not transitionsOk and attempts < 50:
            try:
                self.transitions = createAreaTransitions(bidir)
                super(AreaRandomizer, self).__init__(locations,
                                                     settings,
                                                     seedName,
                                                     self.transitions + bossTransitions,
                                                     bidir,
                                                     dotDir)
                transitionsOk = True
            except RuntimeError:
                transitionsOk = False
                attempts += 1
        if not transitionsOk:
            raise RuntimeError("Impossible seed! (too much fun in the settings, probably)")

    # adapt restrictions implementation to different area layout

    def areaDistance(self, loc, otherLocs):
        return self.areaDistanceProp(loc, otherLocs, 'GraphArea')

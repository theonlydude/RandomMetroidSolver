import random

from itemrandomizerweb.Randomizer import Randomizer
from graph_access import vanillaTransitions, accessPoints, getAccessPoint, createAreaTransitions, chooseEscape

class AreaRandomizer(Randomizer):
    def __init__(self, locations, settings, seedName, bossTransitions,
                 bidir=True, dotDir=None, escape=True, removeEscapeEnemies=True):
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
                if escape == True:
                    # TODO setup smbm with item pool
                    (src, dst) = chooseEscape(self.smbm)
                    # TODO cleanup smbm
                    self.areaGraph.addTransition(src, dst)
                transitionsOk = True
            except RuntimeError:
                transitionsOk = False
                attempts += 1
        if not transitionsOk:
            raise RuntimeError("Impossible seed! (too much fun in the settings, probably)")

    # adapt restrictions implementation to different area layout

    def areaDistance(self, loc, otherLocs):
        return self.areaDistanceProp(loc, otherLocs, 'GraphArea')

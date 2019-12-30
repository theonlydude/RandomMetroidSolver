import random

from itemrandomizerweb.Randomizer import Randomizer
from graph_access import vanillaTransitions, accessPoints, getAccessPoint, createAreaTransitions, createEscapeTransition
from helpers import Bosses

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
                    sm = self.smbm
                    # setup smbm with item pool
                    sm.resetItems()
                    for boss in Bosses.bosses():
                        Bosses.beatBoss(boss)
                    sm.addItems([item['Type'] for item in self.itemPool])
                    if removeEscapeEnemies == True:
                        sm.removeItem('Ice')
                    path = None
                    while path is None:
                        (src, dst) = createEscapeTransition()
                        print(dst)
                        path = self.areaGraph.accessPath(sm, dst, 'Landing Site',
                                                         self.difficultyTarget)
                    # cleanup smbm
                    sm.resetItems()
                    Bosses.reset()
                    # actually update graph
                    self.areaGraph.addTransition(src, dst)
                    # TODO compute timer value
                transitionsOk = True
            except RuntimeError:
                transitionsOk = False
                attempts += 1
        if not transitionsOk:
            raise RuntimeError("Impossible seed! (too much fun in the settings, probably)")

    # adapt restrictions implementation to different area layout

    def areaDistance(self, loc, otherLocs):
        return self.areaDistanceProp(loc, otherLocs, 'GraphArea')

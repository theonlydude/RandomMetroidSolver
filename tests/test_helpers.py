import unittest

from helpers import itemCountOkList
from helpers import energyReserveCountOkList
from parameters import easy
from parameters import medium
from parameters import hard
from parameters import hellRuns

from solver import Solver


class TestHelpers(unittest.TestCase):
    allItems = list(Solver.items.iteritems())

    def testItemCountOkList(self):
        chosenItem = self.allItems[0]
        difficulties = hellRuns['Ice']
        self.assertEqual((False, 0),
                         itemCountOkList(self.allItems,
                                         chosenItem,
                                         difficulties))

    def testEnergyReserveCountOkList(self):
        difficulties = hellRuns['Ice']
        self.assertEqual((False, 0),
                         energyReserveCountOkList(self.allItems,
                                                  difficulties))


if __name__ == '__main__':
    unittest.main()

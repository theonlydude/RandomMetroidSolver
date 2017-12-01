import unittest

from helpers import itemCountOkList
from helpers import energyReserveCountOkList
from parameters import easy, medium, hard
from parameters import Settings
from solver import RomReader


class TestHelpers(unittest.TestCase):
    allItems = list(RomReader.items.items())

    def testItemCountOkList(self):
        chosenItem = self.allItems[0]
        difficulties = Settings.hellRuns['Ice']
        self.assertEqual((False, 0),
                         itemCountOkList(self.allItems,
                                         chosenItem,
                                         difficulties))

    def testEnergyReserveCountOkList(self):
        difficulties = Settings.hellRuns['Ice']
        self.assertEqual((False, 0),
                         energyReserveCountOkList(self.allItems,
                                                  difficulties))


if __name__ == '__main__':
    unittest.main()

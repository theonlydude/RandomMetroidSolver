#!/usr/bin/env python

import sys

from parameters import *
from helpers import *
from smboolmanager import *
from solver import ParamsLoader

def stuff(base, nEtanks, nMissiles, nSupers, nPowerBombs):
    ret = base
    ret.extend(['ETank'] * nEtanks)
    ret.extend(['Missile'] * nMissiles)
    ret.extend(['Super'] * nSupers)
    ret.extend(['PowerBomb'] * nPowerBombs)
    return ret

itemSets = {
    'Kraid' : {
        'Standard' : stuff(['Spazer', 'Charge'], 1, 4, 1, 0),
        'ChargeLess' : stuff([], 1, 4, 1, 0),
        'NoTanks' : stuff(['Spazer', 'Charge'], 0, 4, 1, 0),
    },
    'Phantoon' : {
        'Standard' : stuff(['Spazer', 'Charge', 'Wave', 'Varia'], 5, 6, 1, 1),
        'ChargeLess' : stuff(['Varia'], 5, 6, 3, 1),
        'Tough' : stuff(['Charge', 'Wave'], 5, 3, 1, 1),
        'VeryTough': stuff(['Charge'], 1, 2, 1, 1),
        'NoTanks': stuff(['Charge'], 0, 2, 1, 1),
    },
    'Draygon' : {
        'Standard' : stuff(['Spazer', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 7, 10, 4, 3),
        'ChargeLess' : stuff(['Varia', 'Gravity'], 7, 10, 6, 3),
        'Tough' : stuff(['Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 5, 8, 2, 3),
    },
    'Ridley' : {
        'Standard' : stuff(['Plasma', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 7, 10, 6, 3),
        'ChargeLess' : stuff(['Varia', 'Gravity'], 9, 10, 9, 3),
        'Tough' : stuff(['Spazer', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 4, 10, 3, 3)
    },
    'MotherBrain' : {
        'Standard' : stuff(['Plasma', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 9, 10, 6, 3),
        'ChargeLess' : stuff(['Varia', 'Gravity'], 9, 10, 14, 3),
        'Tough' : stuff(['Spazer', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 5, 10, 5, 3)
    }
}

sm = SMBoolManager.factory('diff')

def boss(name, diffFunction):
    with open(name + ".csv", "w") as csvOut:
        csvOut.write("Diff_preset;Item_set;ok;diff\n")
        print("*** " + name + " ***")
        for presetName, diffPreset in Settings.bossesDifficultyPresets[name].items():
            print("** Diff preset :" + presetName)
            Settings.bossesDifficulty[name] = diffPreset
            print(str(Settings.bossesDifficulty[name]))
            for setName, itemSet in itemSets[name].items():
                print('* Item set ' + setName)
                #        print(str(itemSet))
                sm.resetItems()
                sm.addItems(itemSet)
                d = diffFunction()
                print('---> ' + str(d))
                csvOut.write(presetName + ";" + setName + ";" + str(d[0]) + ";" + str(d[1]) + "\n")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        params = sys.argv[1]
        ParamsLoader.factory(params).load()
    h = Helpers(sm)
    boss('Kraid', h.enoughStuffsKraid)
    boss('Phantoon', h.enoughStuffsPhantoon)
    boss('Draygon', h.enoughStuffsDraygon)
    boss('Ridley', h.enoughStuffsRidley)
    boss('MotherBrain', h.enoughStuffsMotherbrain)


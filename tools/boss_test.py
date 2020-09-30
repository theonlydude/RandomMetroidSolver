#!/usr/bin/env python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from parameters import *
from helpers import *
from smboolmanager import *
from utils import PresetLoader
from rom.rom_patches import RomPatches

def stuff(base, nEtanks, nMissiles, nSupers, nPowerBombs, patches=None):
    ret = base
    RomPatches.ActivePatches = [] if patches is None else patches
    ret.extend(['ETank'] * nEtanks)
    ret.extend(['Missile'] * nMissiles)
    ret.extend(['Super'] * nSupers)
    ret.extend(['PowerBomb'] * nPowerBombs)
    return ret

itemSets = {
    'Kraid' : {
        'Standard' : lambda: stuff(['Spazer', 'Charge'], 1, 4, 1, 0),
        'ChargeLess' : lambda: stuff([], 1, 4, 1, 0),
        'NoTanks' : lambda: stuff(['Spazer', 'Charge'], 0, 4, 1, 0),
    },
    'Phantoon' : {
        'Standard' : lambda: stuff(['Spazer', 'Charge', 'Wave', 'Varia'], 5, 6, 1, 1),
        'ChargeLess' : lambda: stuff(['Varia'], 5, 6, 3, 1),
        'ChargeLessSuitLess' : lambda: stuff([], 5, 6, 3, 1),
        'Tough' : lambda: stuff(['Charge', 'Wave'], 5, 3, 1, 1),
        'VeryTough': lambda: stuff(['Charge'], 1, 2, 1, 1),
        'NoTanks': lambda: stuff(['Charge'], 0, 2, 1, 1),
    },
    'Draygon' : {
        'Standard' : lambda: stuff(['Spazer', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 7, 10, 4, 3),
        'ChargeLess' : lambda: stuff(['Varia', 'Gravity'], 7, 10, 6, 3),
        'Tough' : lambda: stuff(['Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 5, 8, 2, 3),
    },
    'Ridley' : {
        'Standard' : lambda: stuff(['Plasma', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 7, 10, 6, 3),
        'ChargeLess' : lambda: stuff(['Varia', 'Gravity'], 9, 10, 9, 3),
        'Tough' : lambda: stuff(['Spazer', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 4, 10, 3, 3),
        'Crazy' : lambda: stuff(['Charge', 'Varia'], 1, 2, 1, 1)
    },
    'MotherBrain' : {
        'Standard' : lambda: stuff(['Plasma', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 9, 10, 6, 3),
        'ChargeLess' : lambda: stuff(['Varia', 'Gravity'], 9, 10, 14, 3),
        'Tough' : lambda: stuff(['Spazer', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 5, 10, 5, 3),
        'LowEnergy': lambda: stuff(['Plasma', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 3, 10, 6, 3),
        'LowEnergyUltraSparse': lambda: stuff(['Plasma', 'Charge', 'Wave', 'Ice', 'Varia', 'Gravity'], 0, 10, 6, 3, [RomPatches.NerfedRainbowBeam]),
        'LowEnergyNoVaria': lambda: stuff(['Plasma', 'Charge', 'Wave', 'Ice', 'Gravity'], 6, 10, 6, 3),
        'LowEnergyNoVariaUltraSparse': lambda: stuff(['Plasma', 'Charge', 'Wave', 'Ice', 'Gravity'], 0, 10, 6, 3, [RomPatches.NerfedRainbowBeam])
    }
}

sm = SMBoolManager()#.factory('diff')

def boss(name, diffFunction):
    with open(name + ".csv", "w") as csvOut:
        csvOut.write("Diff_preset;Item_set;ok;diff\n")
        print("*** " + name + " ***")
        for presetName, diffPreset in Settings.bossesDifficultyPresets[name].items():
            print("** Diff preset :" + presetName)
            Settings.bossesDifficulty[name] = diffPreset
            print(str(Settings.bossesDifficulty[name]))
            for setName, itemFunc  in itemSets[name].items():
                itemSet = itemFunc()
                print('* Item set ' + setName)
                print(str(itemSet))
                sm.resetItems()
                sm.addItems(itemSet)
                d = diffFunction()
                print('---> ' + str(d) + "\n")
                csvOut.write(presetName + ";" + setName + ";" + str(d[0]) + ";" + str(d[1]) + "\n")
        print("\n")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        params = sys.argv[1]
        PresetLoader.factory(params).load()
    h = Helpers(sm)
    boss('Kraid', h.enoughStuffsKraid)
    boss('Phantoon', h.enoughStuffsPhantoon)
    boss('Draygon', h.enoughStuffsDraygon)
    boss('Ridley', h.enoughStuffsRidley)
    boss('MotherBrain', h.enoughStuffsMotherbrain)


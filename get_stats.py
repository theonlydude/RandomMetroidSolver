#!/usr/bin/python

from solver import RomLoader
from sys import argv
from tournament_locations import locations

if __name__ == "__main__":
    roms = argv[1:]

    counts = {
        'Varia': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0},
        'Gravity': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0},
        'SpeedBooster': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0},
        'HiJump': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0},
        'Grapple': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0},
        'SpaceJump': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0},
        'Ice': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0},
        'Bomb': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0}
    }

    for rom in roms:
        romLoader = RomLoader.factory(rom)
        romLoader.assignItems(locations)

        for loc in locations:
            if loc['itemName'] in ['Varia', 'Gravity', 'SpeedBooster', 'HiJump', 'Grapple', 'SpaceJump', 'Ice', 'Bomb']:
                counts[loc['itemName']][loc['Area']] = counts[loc['itemName']][loc['Area']] + 1

    outFileName = 'stats.csv'
    with open(outFileName, 'w') as outFile:
        outFile.write(";Crateria;Brinstar;Norfair;WreckedShip;Maridia;LowerNorfair;")
        for item in ['Varia', 'Gravity', 'SpeedBooster', 'HiJump', 'Grapple', 'SpaceJump', 'Ice', 'Bomb']:
            outFile.write("{};{};{};{};{};{};{};\n".format(item,
                                                           counts[item]['Crateria'],
                                                           counts[item]['Brinstar'],
                                                           counts[item]['Norfair'],
                                                           counts[item]['WreckedShip'],
                                                           counts[item]['Maridia'],
                                                           counts[item]['LowerNorfair']))

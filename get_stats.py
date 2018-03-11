#!/usr/bin/python

from rom import RomLoader
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
        'Bomb': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0},
        'Charge': {'Crateria': 0, 'Brinstar': 0, 'Norfair': 0, 'LowerNorfair': 0, 'WreckedShip': 0, 'Maridia': 0}
    }

    locCounts = {}
    locNames = []
    progItems = ['Varia', 'Gravity', 'SpeedBooster', 'HiJump', 'Grapple', 'SpaceJump', 'Ice', 'Bomb', 'Charge']
    
    for rom in roms:
        romLoader = RomLoader.factory(rom)
        romLoader.assignItems(locations)

        for loc in locations:
            if loc['itemName'] in progItems:
                counts[loc['itemName']][loc['Area']] = counts[loc['itemName']][loc['Area']] + 1
                if not loc['itemName'] in locCounts:
                    locCounts[loc['itemName']] = {}
                if not loc['Name'] in locNames:
                    locNames.append(loc['Name'])
                if not loc['Name'] in locCounts[loc['itemName']]:
                    locCounts[loc['itemName']][loc['Name']] = 0
                locCounts[loc['itemName']][loc['Name']] += 1

    outFileName = 'area_stats.csv'
    with open(outFileName, 'w') as outFile:
        outFile.write("ITEM;Crateria;Brinstar;Norfair;WreckedShip;Maridia;LowerNorfair;\n")
        for item in ['Varia', 'Gravity', 'SpeedBooster', 'HiJump', 'Grapple', 'SpaceJump', 'Ice', 'Bomb']:
            outFile.write("{};{};{};{};{};{};{};\n".format(item,
                                                           counts[item]['Crateria'],
                                                           counts[item]['Brinstar'],
                                                           counts[item]['Norfair'],
                                                           counts[item]['WreckedShip'],
                                                           counts[item]['Maridia'],
                                                           counts[item]['LowerNorfair']))
    outFileName = 'loc_stats.csv'
    with open(outFileName, 'w') as outFile:
        outFile.write("LOCATION;")
        for itemName in progItems:
            outFile.write(itemName + ";")
        outFile.write('\n')
        for locName in locNames:
            outFile.write(locName + ";")
            for itemName in progItems:
                c = 0
                if locName in locCounts[itemName]:
                    c = locCounts[itemName][locName]
                outFile.write(str(c) + ';')
            outFile.write('\n')

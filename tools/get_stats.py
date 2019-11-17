#!/usr/bin/python

from rom import RomLoader
from sys import argv

if __name__ == "__main__":
    firstLogs = argv[1:]

    itemNames = []
    areaCounts = {}
    areaNames = []
    locCounts = {}
    locNames = []

    for log in firstLogs:
        with open(log, 'r') as logFile:
            lines = logFile.readlines()
        lines = [l.strip() for l in lines]
        for i in range(1, len(lines)): # skip header
            line = lines[i]
            fields = line.split(';')
            item, loc, area = fields[0], fields[1], fields[2]
            if loc not in locNames:
                locNames.append(loc)
            if area not in areaNames:
                areaNames.append(area)
            if item not in itemNames:
                itemNames.append(item)
            if item not in locCounts:
                locCounts[item] = {}
            if item not in areaCounts:
                areaCounts[item] = {}
            if area not in areaCounts[item]:
                areaCounts[item][area] = 0
            if loc not in locCounts[item]:
                locCounts[item][loc] = 0
            areaCounts[item][area] += 1
            locCounts[item][loc] += 1

    outFileName = 'area_stats.csv'
    with open(outFileName, 'w') as outFile:
        outFile.write("ITEM;{}\n".format(';'.join(sorted(areaNames))))
        for item in sorted(itemNames):
            outFile.write(item)
            for area in sorted(areaNames):
                c = 0
                if area in areaCounts[item]:
                    c = areaCounts[item][area]
                outFile.write(';' + str(c))
            outFile.write('\n')
    outFileName = 'loc_stats.csv'
    with open(outFileName, 'w') as outFile:
        outFile.write("LOCATION;{}\n".format(';'.join(sorted(itemNames))))
        for locName in sorted(locNames):
            outFile.write(locName + ";")
            for itemName in sorted(itemNames):
                c = 0
                if locName in locCounts[itemName]:
                    c = locCounts[itemName][locName]
                outFile.write(str(c) + ';')
            outFile.write('\n')

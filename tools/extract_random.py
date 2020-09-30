#!/usr/bin/python3

from rom.rom import RomLoader
from graph.graph_locations import locations
import os.path
import sys

# generate .json for a rom
if __name__ == "__main__":

    if len(sys.argv) == 2:
        romFileName = sys.argv[1]
    else:
        print("missing param: rom file")
        sys.exit(0)

    splited = os.path.splitext(romFileName)
    jsonFileName = splited[0] + '.json'

    romLoader = RomLoader.factory(romFileName)
    romLoader.assignItems(locations)
    romLoader.dump(jsonFileName)

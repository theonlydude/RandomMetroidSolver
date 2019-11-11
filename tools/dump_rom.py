#!/usr/bin/python

# from a .sfc get a .json
import sys
from rom import RomLoader

if len(sys.argv) != 3:
    print("missing parameters: ROM JSON")
    sys.exit(-1)

romFileName = sys.argv[1]
jsonFileName = sys.argv[2]

romLoader = RomLoader.factory(romFileName)
romLoader.dump(jsonFileName)

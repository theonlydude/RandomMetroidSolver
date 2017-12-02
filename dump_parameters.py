#!/usr/bin/python3

import sys, json
#from parameters import Conf,Settings,Knows
from solver import ParamsLoader

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("missing params: <param file> <out json file>")
        sys.exit(0)

    paramFileName = sys.argv[1]
    jsonFileName = sys.argv[2]

    loader = ParamsLoader.factory(paramFileName)
    loader.load()
    loader.printToScreen()
    loader.dump(jsonFileName)

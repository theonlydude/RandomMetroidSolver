#!/usr/bin/env python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.symbols import Symbols

if len(sys.argv) < 3:
    # nothing to do
    exit(0)

symbols = Symbols()

mslPath = sys.argv[1]

for wla in sys.argv[2:]:
    symbols.loadWLA(wla)

symbols.appendToMSL(mslPath)

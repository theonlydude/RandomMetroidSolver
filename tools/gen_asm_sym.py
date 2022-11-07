#!/usr/bin/env python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.symbols import Symbols

asm_sym = sys.argv[1]
wla_sym = sys.argv[2]

symbols = Symbols()

symbols.loadWLA(wla_sym)
symbols.writeSymbolsASM(asm_sym)

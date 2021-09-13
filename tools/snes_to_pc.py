#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import snes_to_pc

for addr10 in sys.argv[1:]:
    addr16 = int(addr10, 16)
    print("{} -> {}".format(hex(addr16), hex(snes_to_pc(addr16))))

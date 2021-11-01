#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import pc_to_snes

for addr10 in sys.argv[1:]:
    addr16 = int(addr10, 16)
    print("{} -> {}".format(hex(addr16), hex(pc_to_snes(addr16))))

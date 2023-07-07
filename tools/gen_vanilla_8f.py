#!/usr/bin/env python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import pc_to_snes

# dict of label: addr
with open('patches/vanilla/sym/bank_8f.json') as f:
    addresses = json.load(f)

for k, v in addresses.items():
    if k.startswith("Door_"):
        print("org ${}".format(hex(v)[2:]))
        print("{}:".format(k))


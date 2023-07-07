#!/usr/bin/env python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import pc_to_snes

pc_addr = int(sys.argv[1], 16)
snes_addr = pc_to_snes(pc_addr)

# dict of label: addr
with open('patches/vanilla/sym/bank_8f.json') as f:
    addresses = json.load(f)

# reverse dict
reverse = {v: k for k, v in addresses.items()}
label = reverse[snes_addr]

print("label for address: {}/{} is: {}".format(hex(pc_addr), hex(snes_addr), label))

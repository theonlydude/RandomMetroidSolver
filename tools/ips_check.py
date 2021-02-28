#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.ips import IPS_Patch
from rom.rom import pc_to_snes

vanilla=sys.argv[1]
ips_ranges = []

def addRanges(name, patch):
    for r in patch.getRanges():
        ips_ranges.append({'name':name, 'range':r})

def loadPatchPy():
    from rando.patches import patches as patches_py
    for name,patch in patches_py.items():
        addRanges(name, IPS_Patch(patch))

for patch in sys.argv[2:]:
    baseName = os.path.basename(patch)
    if baseName == "patches.py":
        loadPatchPy()
    else:
        addRanges(baseName, IPS_Patch.load(patch))

overlaps = {}
last, lstop = None, -1
for rg in sorted(ips_ranges, key=lambda r:r['range'].start):
    thisStart = rg['range'].start
    if last and lstop > thisStart and lstop != 0x7fe0: # overlap, skip checksum
        k = (last['name'], rg['name'])
        if k not in overlaps:
            overlaps[k] = []
        overlaps[k].append((lstop, thisStart))
    last = rg
    lstop = last['range'].stop

for k,v in overlaps.items():
    pc_addresses = ["(0x%x, 0x%x)" % a for a in v]
    snes_addresses = ["($%06x, $%06x)" % (pc_to_snes(a[0]), pc_to_snes(a[1])) for a in v]
    print("%s and %s overlap!\n\tPC:\t%s\n\tSNES:\t%s" % (k[0], k[1], pc_addresses, snes_addresses))

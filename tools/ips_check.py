#!/usr/bin/python3

import sys, os, re

# now that we're in directory 'tools/' we have to update sys.path
mainDir = os.path.dirname(sys.path[0])
sys.path.append(mainDir)

from rom.ips import IPS_Patch
from rom.rom import pc_to_snes
from logic.logic import Logic
from patches.patchaccess import PatchAccess

logic = sys.argv[1]
Logic.factory(logic)

patchNameFilter = os.getenv("IPS_CHECK_FILTER")

patchAccess = None
ips_ranges = []

def addRanges(name, patch):
    for r in patch.getRanges():
        ips_ranges.append({'name':name, 'range':r})

def loadPatchPy():
    patchAccess = PatchAccess(mainDir)
    patches_py = patchAccess.getDictPatches()
    for name,patch in patches_py.items():
        if patchNameFilter is None or not re.match(patchNameFilter, name):
            addRanges(name, IPS_Patch(patch))

for patch in sys.argv[2:]:
    if os.path.getsize(patch) == 0:
        continue
    baseName = os.path.basename(patch)
    if baseName == "patches.py":
        if patchAccess is None:
            loadPatchPy()
    elif patchNameFilter is None or not re.match(patchNameFilter, baseName) :
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
    pc_addresses = ["(0x%x, 0x%x)" % (a[1], a[0]) for a in v]
    snes_addresses = ["($%06x, $%06x)" % (pc_to_snes(a[1]), pc_to_snes(a[0])) for a in v]
    print("%s and %s overlap!\n\tPC:\t%s\n\tSNES:\t%s" % (k[0], k[1], pc_addresses, snes_addresses))

#!/usr/bin/python3

import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

# creates a "complete" IPS based on two patched files
# requirements: files have the same size and have been patched with different initial data

from rom.ips import IPS_Patch

patched1 = sys.argv[1]
patched2 = sys.argv[2]
output = sys.argv[3]

sz = os.path.getsize(patched1)

assert sz == os.path.getsize(patched2), "Files must have the same size"

with open(patched1, "rb") as fp:
    data1 = fp.read()
with open(patched2, "rb") as fp:
    data2 = fp.read()

patchDict = {offset:[data1[offset]] for offset in range(sz) if data1[offset] == data2[offset]}

base_off = -100
prev_off = -100
for offset in patchDict:
    if prev_off == offset - 1:
        patchDict[base_off] += patchDict[offset]
        del patchDict[offset]
        prev_off = offset
    else:
        base_off = offset
        prev_off = offset

patch = IPS_Patch(patchDict)

patch.save(output)

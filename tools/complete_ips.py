#!/usr/bin/python3

import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

# creates a "complete" IPS based on two patched files
# requirements: files have the same size and have been patched with different initial data

from rom.ips import IPS_Patch

vanilla = sys.argv[1]
patched1 = sys.argv[2]
patched2 = sys.argv[3]
output = sys.argv[4]

sz = os.path.getsize(patched1)

assert sz == os.path.getsize(patched2), "Files must have the same size"

vanilla_sz = os.path.getsize(vanilla)

with open(patched1, "rb") as fp:
    data1 = fp.read()
with open(patched2, "rb") as fp:
    data2 = fp.read()
with open(vanilla, "rb") as fp:
    vanilla_data = fp.read()

patchDict = {offset:[data1[offset]] for offset in range(sz) if data1[offset] == data2[offset] and (offset >= vanilla_sz or data1[offset] != vanilla_data[offset])}

base_off = -100
prev_off = -100

offsets = list(patchDict.keys())

for offset in offsets:
    if prev_off == offset - 1:
        patchDict[base_off] += patchDict[offset]
        del patchDict[offset]
        prev_off = offset
    else:
        base_off = offset
        prev_off = offset

patch = IPS_Patch(patchDict)

patch.save(output)

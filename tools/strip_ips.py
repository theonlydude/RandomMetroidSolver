#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.ips import IPS_Patch
from rom.rom import snes_to_pc, pc_to_snes

ips=sys.argv[1]
replace = None
try:
    replace=sys.argv[4]
except:
    pass

# handle both pc and snes addresses
low=int(sys.argv[2], 16)
high=int(sys.argv[3], 16)
if low >= 0x800000:
    low = snes_to_pc(low)
if high >= 0x80000:
    high = snes_to_pc(high)

ext = os.path.splitext(ips)[-1].lower()

if ext != ".ips":
    sys.stderr.write("Wrong ips extension")
    sys.exit(1)

# load ips
patch = IPS_Patch.load(ips)
patch_dict = patch.toDict()

# remove overlapping data
filtered_dict = {}
for keyLow, data in patch_dict.items():
    dataLength = len(data)
    keyHigh = keyLow + dataLength
    if keyHigh < low or keyLow > high:
        if replace is None:
            print("[{}, {}] we have {} bytes of data".format(hex(pc_to_snes(keyLow)),
                                                             hex(pc_to_snes(keyHigh)),
                                                             dataLength))
        filtered_dict[keyLow] = data
    else:
        print("[{}, {}] we have {} bytes of data overlaping with [{}, {}]".format(hex(pc_to_snes(keyLow)),
                                                                                  hex(pc_to_snes(keyHigh)),
                                                                                  dataLength,
                                                                                  hex(pc_to_snes(low)),
                                                                                  hex(pc_to_snes(high))))

if len(filtered_dict.keys()) < len(patch_dict.keys()):
    # write ips
    if replace is not None:
        out = ips
    else:
        split = os.path.split(ips)
        out = os.path.join(split[0], 'out_'+split[1])
    out_patch = IPS_Patch(filtered_dict)
    out_patch.save(out)

    print("filtered ips generated: {}".format(out))
else:
    print("no overlapping record found")

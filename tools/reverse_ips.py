#!/usr/bin/python3

import sys, os

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.ips import IPS_Patch
from rom.rom import RealROM
from patches.common import patches as common_patches

vanilla=sys.argv[1]
ipsToReverse = sys.argv[2:]

rom = RealROM(vanilla)

for ips in ipsToReverse:
    if ips not in common_patches.patches:
        ipsPath = os.path.abspath(ips)
        destDir, destFile = os.path.split(ipsPath)
        patch = IPS_Patch.load(ips)
        patchDict = patch.toDict()
    else:
        patchDict = common_patches.patches[ips]
        destDir = sys.path[0] + "/../patches/common/ips"
        destFile = ips + ".ips"
    destFile = "remove_" + destFile
    destPath = os.path.join(destDir, destFile)
    reversePatchDict = {}
    for addr, bytez in patchDict.items():
        sz = len(bytez)
        origBytes = []
        rom.seek(addr)
        for i in range(sz):
            origBytes.append(rom.readByte())
        assert len(origBytes) == sz
        reversePatchDict[addr] = origBytes
    reversePatch = IPS_Patch(reversePatchDict)
    reversePatch.save(destPath)

rom.close()

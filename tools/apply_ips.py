#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.ips import IPS_Patch

ips=sys.argv[1]

ext = os.path.splitext(ips)[-1].lower()

if ext != ".ips":
    sys.stderr.write("Wrong ips extension")
    sys.exit(1)

patch = IPS_Patch.load(ips)

for rom in sys.argv[2:]:
    with open(rom, 'rb+') as romHandle:
        patch.applyFile(romHandle)
    print("Applied "+ips+" to "+rom+" successfully")

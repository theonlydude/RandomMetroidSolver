#!/usr/bin/python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.ips import IPS_Patch
elev = IPS_Patch.load("patches/common/ips/elevators_speed.ips")
doors = IPS_Patch.load("patches/common/ips/fast_doors.ips")
merged = IPS_Patch()
merged.append(elev)
merged.append(doors)
merged.save("patches/common/ips/elevators_doors_speed.ips")

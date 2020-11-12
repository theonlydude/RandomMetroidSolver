#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.ips import IPS_Patch

original=sys.argv[1]
patched=sys.argv[2]
target=sys.argv[3]

patch = IPS_Patch.create(open(original, 'rb').read(), open(patched, 'rb').read())

patch.save(target)


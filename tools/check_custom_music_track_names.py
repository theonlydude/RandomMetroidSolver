#!/usr/bin/python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# helper tool to find track names included in other track names, to work around a web UI display bug

from rom.rom import RealROM, snes_to_pc
from rom.rompatcher import MusicPatcher,RomTypeForMusic
from utils.parameters import appDir

# use patcher ctor to load music metadata
p=MusicPatcher(None, RomTypeForMusic.VariaSeed, baseDir=os.path.join(appDir+'/..', 'varia_custom_sprites', 'music'))
allTracks=p.allTracks

trackNames = allTracks.keys()

for trackName in trackNames:
    inc = [t for t in trackNames if trackName in t and t != trackName]
    if len(inc) > 0:
        print("%s is in %s" % (trackName, str(inc)))

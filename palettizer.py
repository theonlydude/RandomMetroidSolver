#!/usr/bin/python

from itemrandomizerweb.PaletteRando import PaletteRando
import random, sys
from rom import RomPatcher

random.seed(random.randint(0, 9999999))

# we don't have access to the vanilla ROM in web mode
filename = sys.argv[1]
romPatcher = RomPatcher(filename)
paletteRando = PaletteRando(romPatcher)
paletteRando.randomize()

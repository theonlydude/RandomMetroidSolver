#!/usr/bin/python

from itemrandomizerweb.PaletteRando import PaletteRando
import random, sys
from rom import RomPatcher

random.seed(random.randint(0, 9999999))

# we don't have access to the vanilla ROM in web mode
filename = sys.argv[1]
romPatcher = RomPatcher(filename)

settings = {
    #set to True if all suits should get a separate hue-shift degree
    "individual_suit_shift": False,

    #set to True if all tileset palettes should get a separate hue-shift degree
    "individual_tileset_shift": False,

    #Match ship palette with power suit palette
    "match_ship_and_power": False,

    #Group up similar looking enemy palettes to give them similar looks after hue-shifting
    #(e.g. metroids, big+small sidehoppers)
    "seperate_enemy_palette_groups": True,

    #Match boss palettes with boss room degree
    "match_room_shift_with_boss": False,

    ### These variables define what gets shifted
    "shift_tileset_palette": True,
    "shift_boss_palettes": True,
    "shift_suit_palettes": True,
    "shift_enemy_palettes": True,
    "shift_beam_palettes": True,
    "shift_ship_palette": True
}

paletteRando = PaletteRando(romPatcher, settings)
paletteRando.randomize()

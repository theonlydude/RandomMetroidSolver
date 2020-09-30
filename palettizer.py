#!/usr/bin/python3

import random, sys, argparse
from rando.PaletteRando import PaletteRando
from rom.rompatcher import RomPatcher
import log

# for local "palette rando" patching of a seed
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Palettes Randomizer")
    parser.add_argument('--rom', '-r', help="the ROM", dest='rom', nargs='?', default=None)
    parser.add_argument('--individual_suit_shift', help="", action='store_true', dest='individual_suit_shift', default=False)
    parser.add_argument('--individual_tileset_shift', help="", action='store_true', dest='individual_tileset_shift', default=False)
    parser.add_argument('--no_match_ship_and_power', help="", action='store_false', dest='match_ship_and_power', default=True)
    parser.add_argument('--seperate_enemy_palette_groups', help="", action='store_true', dest='seperate_enemy_palette_groups', default=False)
    parser.add_argument('--no_match_room_shift_with_boss', help="", action='store_false', dest='match_room_shift_with_boss', default=True)
    parser.add_argument('--no_shift_tileset_palette', help="", action='store_false', dest='shift_tileset_palette', default=True)
    parser.add_argument('--no_shift_boss_palettes', help="", action='store_false', dest='shift_boss_palettes', default=True)
    parser.add_argument('--no_shift_suit_palettes', help="", action='store_false', dest='shift_suit_palettes', default=True)
    parser.add_argument('--no_shift_enemy_palettes', help="", action='store_false', dest='shift_enemy_palettes', default=True)
    parser.add_argument('--no_shift_beam_palettes', help="", action='store_false', dest='shift_beam_palettes', default=True)
    parser.add_argument('--no_shift_ship_palette', help="", action='store_false', dest='shift_ship_palette', default=True)
    parser.add_argument('--seed', '-s', help="randomization seed to use", dest='seed', nargs='?', default=0, type=int)
    parser.add_argument('--min_degree', help="min hue shift", dest='min_degree', nargs='?', default=-180, type=int)
    parser.add_argument('--max_degree', help="max hue shift", dest='max_degree', nargs='?', default=180, type=int)
    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug', action='store_true')
    parser.add_argument('--no_global_shift', help="", action='store_false', dest='global_shift', default=True)
    parser.add_argument('--invert', help="invert color range", dest='invert', action='store_true', default=False)

    args = parser.parse_args()

    # local mode
    if args.rom == None:
        print("Need --rom parameter")
        sys.exit(-1)

    log.init(args.debug)
    logger = log.get('Palette')

    if args.seed == 0:
        random.seed(random.randint(0, 9999999))
    else:
        random.seed(args.seed)

    settings = {
        # global same shift for everything flag
        "global_shift": True,

        #set to True if all suits should get a separate hue-shift degree
        "individual_suit_shift": False,

        #set to True if all tileset palettes should get a separate hue-shift degree
        "individual_tileset_shift": False,

        #Match ship palette with power suit palette
        "match_ship_and_power": True,

        #Group up similar looking enemy palettes to give them similar looks after hue-shifting
        #(e.g. metroids, big+small sidehoppers)
        "seperate_enemy_palette_groups": False,

        #Match boss palettes with boss room degree
        "match_room_shift_with_boss": True,

        ### These variables define what gets shifted
        "shift_tileset_palette": True,
        "shift_boss_palettes": True,
        "shift_suit_palettes": True,
        "shift_enemy_palettes": True,
        "shift_beam_palettes": True,
        "shift_ship_palette": True,

        # min/max hue shift
        "min_degree": -180,
        "max_degree": 180,
        "invert": False
    }

    for param in settings:
        settings[param] = getattr(args, param)

    logger = log.get('Palette')
    logger.debug("settings: {}".format(settings))

    romPatcher = RomPatcher(args.rom)
    paletteRando = PaletteRando(romPatcher, settings, None)
    paletteRando.randomize()

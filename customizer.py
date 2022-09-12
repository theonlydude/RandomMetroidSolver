#!/usr/bin/python3

import argparse, os.path, json, sys, shutil, random

from logic.logic import Logic
from rom.PaletteRando import PaletteRando
from rom.rompatcher import RomPatcher, MusicPatcher, RomTypeForMusic
from utils.utils import dumpErrorMsg

import utils.log
import utils.db as db

# we need to know the logic before doing anything else
def getLogic():
    # check if --logic is there
    logic = 'vanilla'
    for i, param in enumerate(sys.argv):
        if param == '--logic' and i+1 < len(sys.argv):
            logic = sys.argv[i+1]
    return logic
Logic.factory(getLogic())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Randomizer")
    parser.add_argument('--rom', '-r',
                        help="the vanilla ROM",
                        dest='rom', nargs='?', default=None)
    parser.add_argument('--output',
                        help="to choose the name of the generated json (for the webservice)",
                        dest='output', nargs='?', default=None)
    parser.add_argument('--logic', help='logic to use', dest='logic', nargs='?', default="varia", choices=["varia", "rotation"])
    parser.add_argument('--patch', '-c',
                        help="optional patches to add",
                        dest='patches', nargs='?', default=[], action='append',
                        choices=['itemsounds.ips', 'random_music.ips',
                                 'fast_doors.ips', 'elevators_speed.ips',
                                 'spinjumprestart.ips', 'rando_speed.ips', 'No_Music', 'AimAnyButton.ips',
                                 'max_ammo_display.ips', 'supermetroid_msu1.ips', 'Infinite_Space_Jump',
                                 'refill_before_save.ips', 'remove_elevators_speed.ips',
                                 'remove_fast_doors.ips', 'remove_Infinite_Space_Jump.ips',
                                 'remove_rando_speed.ips', 'remove_spinjumprestart.ips',
                                 'remove_itemsounds.ips', 'vanilla_music.ips', 'custom_ship.ips',
                                 'Ship_Takeoff_Disable_Hide_Samus', 'widescreen.ips',
                                 'hell.ips', 'lava_acid_physics.ips', 'color_blind.ips'])
    parser.add_argument('--controls',
                        help="specify controls, comma-separated, in that order: Shoot,Jump,Dash,ItemSelect,ItemCancel,AngleUp,AngleDown. Possible values: A,B,X,Y,L,R,Select,None",
                        dest='controls')
    parser.add_argument('--moonwalk',
                        help="Enables moonwalk by default",
                        dest='moonWalk', action='store_true', default=False)
    parser.add_argument('--palette', help="Randomize the palettes", dest='palette', action='store_true')
    parser.add_argument('--individual_suit_shift', help="palette param", action='store_true',
                        dest='individual_suit_shift', default=False)
    parser.add_argument('--individual_tileset_shift', help="palette param", action='store_true',
                        dest='individual_tileset_shift', default=False)
    parser.add_argument('--no_match_ship_and_power', help="palette param", action='store_false',
                        dest='match_ship_and_power', default=True)
    parser.add_argument('--seperate_enemy_palette_groups', help="palette param", action='store_true',
                        dest='seperate_enemy_palette_groups', default=False)
    parser.add_argument('--no_match_room_shift_with_boss', help="palette param", action='store_false',
                        dest='match_room_shift_with_boss', default=True)
    parser.add_argument('--no_shift_tileset_palette', help="palette param", action='store_false',
                        dest='shift_tileset_palette', default=True)
    parser.add_argument('--no_shift_boss_palettes', help="palette param", action='store_false',
                        dest='shift_boss_palettes', default=True)
    parser.add_argument('--no_shift_suit_palettes', help="palette param", action='store_false',
                        dest='shift_suit_palettes', default=True)
    parser.add_argument('--no_shift_enemy_palettes', help="palette param", action='store_false',
                        dest='shift_enemy_palettes', default=True)
    parser.add_argument('--no_shift_beam_palettes', help="palette param", action='store_false',
                        dest='shift_beam_palettes', default=True)
    parser.add_argument('--no_shift_ship_palette', help="palette param", action='store_false',
                        dest='shift_ship_palette', default=True)
    parser.add_argument('--min_degree', help="min hue shift", dest='min_degree', nargs='?', default=-180, type=int)
    parser.add_argument('--max_degree', help="max hue shift", dest='max_degree', nargs='?', default=180, type=int)
    parser.add_argument('--no_global_shift', help="", action='store_false', dest='global_shift', default=True)
    parser.add_argument('--invert', help="invert color range", dest='invert', action='store_true', default=False)
    parser.add_argument('--no_blue_door_palette', help="palette param", action='store_true',
                        dest='no_blue_door_palette', default=False)
    parser.add_argument('--sprite', help='use a custom sprite for Samus', dest='sprite', default=None)
    parser.add_argument('--no_spin_attack', help='when using a custom sprite, use the same animation for screw attack with or without Space Jump', dest='noSpinAttack', action='store_true', default=False)
    parser.add_argument('--customItemNames', help='add custom item names for some of them, related to the custom sprite',
                        dest='customItemNames', action='store_true', default=False)
    parser.add_argument('--ship', help='use a custom sprite for Samus ship', dest='ship', default=None)
    parser.add_argument('--seedIps', help='ips generated from previous seed', dest='seedIps', default=None)
    parser.add_argument('--music',
                        help="JSON file for music replacement mapping",
                        dest='music', nargs='?', default=None)
    parser.add_argument('--hellrun', help="Hellrun damage rate in percentage, between 0 and 400 (default 100)",
                        dest='hellrunRate', default=100, type=int)
    parser.add_argument('--etanks', help="Additional ETanks, between 0 (default) and 18",
                        dest='additionalEtanks', default=0, type=int)
    # parse args
    args = parser.parse_args()

    if args.output is None and args.rom is None:
        print("Need --output or --rom parameter")
        sys.exit(-1)
    elif args.output is not None and args.rom is not None:
        print("Can't have both --output and --rom parameters")
        sys.exit(-1)

    if args.additionalEtanks < 0 or args.additionalEtanks > 18:
        print("additionalEtanks must be between 0 and 18")
        sys.exit(-1)

    if args.hellrunRate < 0 or args.hellrunRate > 400:
        print("hellrunRate must be between 0 and 400")
        sys.exit(-1)

    utils.log.init(False)
    logger = utils.log.get('Custo')

    ctrlDict = None
    if args.controls:
        ctrlList = args.controls.split(',')
        if len(ctrlList) != 7:
            raise ValueError("Invalid control list size")
        ctrlKeys = ["Shot", "Jump", "Dash", "ItemSelect", "ItemCancel", "AngleUp", "AngleDown"]
        ctrlDict = {}
        i = 0
        for k in ctrlKeys:
            b = ctrlList[i]
            if b in RomPatcher.buttons:
                ctrlDict[k] = b
                i += 1
            else:
                raise ValueError("Invalid button name : " + str(b))

    try:
        if args.rom is not None:
            # patch local rom
            inFileName = args.rom
            romDir = os.path.dirname(inFileName)
            romFile = os.path.basename(inFileName)
            outFileName = os.path.join(romDir, 'Custom_' + romFile)
            shutil.copyfile(inFileName, outFileName)
            romPatcher = RomPatcher(outFileName)
        else:
            # web mode
            outFileName = args.output
            romPatcher = RomPatcher()

        musicPatcher = None
        if args.music is not None:
            args.patches.append('custom_music.ips')
            romType = 0
            with open(args.music, "r") as f:
                music = json.load(f)
            musicParams = music.get('params', {})
            musicMapping = music.get('mapping', {})

            variaSeed = musicParams.get('varia', False)
            areaSeed = musicParams.get('area', False)
            bossSeed = musicParams.get('boss', False)
            if variaSeed:
                romType |= RomTypeForMusic.VariaSeed
            if areaSeed:
                romType |= RomTypeForMusic.AreaSeed
            if bossSeed:
                romType |= RomTypeForMusic.BossSeed

            musicPatcher = MusicPatcher(romPatcher.romFile, romType)

        # from customizer permalink, apply previously generated seed ips first
        if args.seedIps is not None:
            romPatcher.applyIPSPatch(args.seedIps)

        romPatcher.addIPSPatches(args.patches)

        if args.sprite is not None:
            purge = args.ship is not None
            romPatcher.customSprite(args.sprite, args.customItemNames, args.noSpinAttack, purge) # adds another IPS
        if args.ship is not None:
            romPatcher.customShip(args.ship) # adds another IPS
            # don't color randomize custom ships
            args.shift_ship_palette = False

        # we have to write ips to ROM before doing our direct modifications
        # which will rewrite some parts (like in credits)
        romPatcher.commitIPS()
        if ctrlDict is not None:
            romPatcher.writeControls(ctrlDict)
        if args.moonWalk == True:
            romPatcher.enableMoonWalk()

        romPatcher.writeAdditionalETanks(args.additionalEtanks)
        romPatcher.writeHellrunRate(args.hellrunRate)

        if args.palette == True:
            paletteSettings = {
                "global_shift": None,
                "individual_suit_shift": None,
                "individual_tileset_shift": None,
                "match_ship_and_power": None,
                "seperate_enemy_palette_groups": None,
                "match_room_shift_with_boss": None,
                "shift_tileset_palette": None,
                "shift_boss_palettes": None,
                "shift_suit_palettes": None,
                "shift_enemy_palettes": None,
                "shift_beam_palettes": None,
                "shift_ship_palette": None,
                "min_degree": None,
                "max_degree": None,
                "invert": None,
                "no_blue_door_palette": None
            }
            for param in paletteSettings:
                paletteSettings[param] = getattr(args, param)
            PaletteRando(romPatcher, paletteSettings, args.sprite, 'color_blind.ips' in args.patches).randomize()
        if musicPatcher is not None:
            musicPatcher.replace(musicMapping,
                                 updateReferences=musicParams.get('room_states', True),
                                 output=musicParams.get("output", None))
        romPatcher.end()

        if args.rom is None:
            # web mode
            data = romPatcher.romFile.data
            with open(outFileName, 'w') as jsonFile:
                json.dump(data, jsonFile)
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stdout)
        msg = "Error patching {}: ({}: {})".format(outFileName, type(e).__name__, e)
        if args.rom is None:
            dumpErrorMsg(args.output, msg)
        else:
            print(msg)
        sys.exit(-1)

    print("Customized rom generated: {}".format(outFileName))

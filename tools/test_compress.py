#!/usr/bin/python3

import sys, os, subprocess, time, multiprocessing
from datetime import datetime

# now that we're in directory 'tools/' we have to update sys.path
dir_path = os.path.dirname(sys.path[0])
sys.path.append(dir_path)

from rom.rom import snes_to_pc, RealROM, FakeROM
from rom.compression import Compressor
from utils.utils import getPythonExec
from utils.log import init

romFile = sys.argv[1]
decomp_name = None
if len(sys.argv) > 2:
    decomp_name = sys.argv[2]
    decomp_address = int(sys.argv[3])

addresses = {
    "Palette 0: Upper Crateria": 0xC2AD7C,
    "Palette 1: Red Crateria": 0xC2AE5D,
    "Palette 2: Lower Crateria": 0xC2AF43,
    "Palette 3: Old Tourian": 0xC2B015,
    "Palette 4: Wrecked Ship - power on": 0xC2B0E7,
    "Palette 5: Wrecked Ship - power off": 0xC2B1A6,
    "Palette 6: Green/blue Brinstar": 0xC2B264,
    "Palette 7: Red Brinstar / Kraid's lair": 0xC2B35F,
    "Palette 8: Pre Tourian entrance corridor": 0xC2B447,
    "Palette 1Ah: Kraid's room": 0xC2B510,
    "Palette 9: Heated Norfair": 0xC2B5E4,
    "Palette Ah: Unheated Norfair": 0xC2B6BB,
    "Palette 1Bh: Crocomire's room": 0xC2B798,
    "Palette Bh: Sandless Maridia": 0xC2B83C,
    "Palette Ch: Sandy Maridia": 0xC2B92E,
    "Palette 1Ch: Draygon's room": 0xC2BA2C,
    "Palette Dh: Tourian": 0xC2BAED,
    "Palette Eh: Mother Brain's room": 0xC2BBC1,
    "Palette 15h: Map room / Tourian entrance": 0xC2BC9C,
    "Palette 16h: Wrecked Ship map room - power off": 0xC2BD7B,
    "Palette 17h: Blue refill room": 0xC2BE58,
    "Palette 18h: Yellow refill room": 0xC2BF3D,
    "Palette 19h: Save room": 0xC2C021,
    "Palette Fh/11h/13h: Blue Ceres": 0xC2C104,
    "Palette 10h/12h/14h: White Ceres": 0xC2C1E3,

    "Tileset 0/1: Upper Crateria": 0xC1B6F6,
    "Tileset 2/3: Lower Crateria": 0xC1BEEE,
    "Tileset 4/5: Wrecked Ship": 0xC1C5CF,
    "Tileset 6: Green/blue Brinstar": 0xC1CFA6,
    "Tileset 7/8: Red Brinstar / Kraid's lair": 0xC1D8DC,
    "Tileset 1Ah: Kraid's room": 0xC1E189,
    "Tileset 9/Ah: Norfair": 0xC1E361,
    "Tileset 1Bh: Crocomire's room": 0xC1F3AF,
    "Tileset Bh: Sandless Maridia": 0xC1F4B1,
    "Tileset Ch: Sandy Maridia": 0xC2855F,
    "Tileset 1Ch: Draygon's room": 0xC2960D,
    "Tileset Dh/Eh: Tourian": 0xC29B01,
    "Tileset 15h/16h/17h/18h/19h: Utility room": 0xC2A27B,
    "Tileset Fh/10h/11h/12h/13h/14h: Ceres": 0xC2A75E,

    "Tiles 0/1: Upper Crateria": 0xBAC629,
    "Tiles 2/3: Lower Crateria": 0xBAF911,
    "Tiles 4/5: Wrecked Ship": 0xBBAE9E,
    "Tiles 6: Green/blue Brinstar": 0xBBE6B0,
    "Tiles 7/8: Red Brinstar / Kraid's lair": 0xBCA5AA,
    "Tiles 1Ah: Kraid's room": 0xBCDFF0,
    "Tiles 9/Ah: Norfair": 0xBDC3F9,
    "Tiles 1Bh: Crocomire's room": 0xBDFE2A,
    "Tiles Bh: Sandless Maridia": 0xBEB130,
    "Tiles Ch: Sandy Maridia": 0xBEE78D,
    "Tiles 1Ch: Draygon's room": 0xBF9DEA,
    "Tiles Dh/Eh: Tourian": 0xBFD414,
    "Tiles 15h/16h/17h/18h/19h: Utility room": 0xC0860B,
    "Tiles Fh/10h: Ceres": 0xC0B004,
    "Tiles 11h/12h: Ceres elevator": 0xC0E22A,
    "Tiles 13h/14h: Ceres Ridley's room": 0xC18DA9,

    "Room $91F8: Landing site": 0xC2C2BB,
    "Room $92B3: Gauntlet east": 0xC2D6E8,
    "Room $92FD: Crateria mainstreet": 0xC2DBC4,
    "Room $93AA: Landing site power bombs cave": 0xC2E977,
    "Room $93FE: Wrecked Ship entrance": 0xC2EB45,
    "Room $9461: Pre orange zoomer hall": 0xC38E1F,
    "Room $948C: Pre moat room": 0xC38FFE,
    "Room $94CC: Crateria -> Maridia elevator": 0xC39BFC,
    "Room $94FD: Wrecked Ship back door": 0xC39DB8,
    "Room $9552: East Crateria kago shaft": 0xC3ACDB,
    "Room $957D: East Crateria maze": 0xC3B1BA,
    "Room $95A8: Post Crateria maze yellow door": 0xC3BB9B,
    "Room $95D4: Crateria pipe tunnel": 0xC3BCD2,
    "Room $95FF: Moat": 0xC3BD6D,
    "Room $962A: Crateria -> Red Brinstar elevator": 0xC3C145,
    "Room $965B: Gauntlet west": 0xC3C301,
    "Room $968F: Orange zoomer hall": 0xC3C80C,
    "Room $96BA: Old Tourian escape shaft": 0xC3C998,
    "Room $975C: Old Mother Brain room": 0xC3D9F7,
    "Room $97B5: Crateria -> Blue Brinstar elevator": 0xC3DF23,
    "Room $9804: Bomb Torizo": 0xC3E0D0,
    "Room $9879: Pre Bomb Torizo hall": 0xC3E16E,
    "Room $98E2: Pre Crateria map station hall": 0xC3E232,
    "Room $990D: Crateria slope": 0xC3E2FC,
    "Room $9938: Crateria -> Green Brinstar elevator": 0xC3E985,
    "Room $9969: West Crateria kago hall": 0xC3EB35,
    "Room $99BD: Crateria space pirate shaft": 0xC3EE60,
    "Room $99F9: Crateria spike floor room": 0xC3F4D3,
    "Room $9A44: Crateria bomb block hall": 0xC4811E,
    "Room $9A90: Crateria chozo missile": 0xC48232,
    "Room $C98E: Wrecked Ship spike floor hall": 0xC48322,
    "Room $CA08: Wrecked Ship entrance treadmill": 0xC49D2E,
    "Room $CA52, state $CA64: Wrecked Ship attic": 0xC49EAE,
    "Room $CA52, state $CA7E: Wrecked Ship attic": 0xC4A2E7,
    "Room $CAAE: Wrecked Ship attic missile tank room": 0xC4A720,
    "Room $CAF6, state $CB08: Wrecked Ship mainstreet": 0xC4A9AC,
    "Room $CAF6, state $CB22: Wrecked Ship mainstreet": 0xC4BDC0,
    "Room $CB8B: Wrecked Ship flooded spikey hall": 0xC4D187,
    "Room $CBD5: Wrecked Ship east exit": 0xC4D3EE,
    "Room $CC27: Wrecked Ship chozo energy tank room": 0xC4D883,
    "Room $CC6F: Pre Phantoon hall": 0xC4E14E,
    "Room $CD13: Phantoon": 0xC4E58C,
    "Room $CD5C: Wrecked Ship first flooded room": 0xC4E6A5,
    "Room $CDA8: Wrecked Ship obvious super missile room": 0xC4E94E,
    "Room $CDF1, state $CE03: Wrecked Ship hidden super missile hall": 0xC4EA8F,
    "Room $CDF1, state $CE1D: Wrecked Ship hidden super missile hall": 0xC4ED98,
    "Room $CE40: Gravity suit room": 0xC4F0A1,
    "Room $9AD9: Green Brinstar mainstreet": 0xC4F1CE,
    "Room $9B5B: Spore Spawn's super missile shaft": 0xC58BD5,
    "Room $9B9D: Pre Brinstar map room hall": 0xC59642,
    "Room $9BC8: Early supers room": 0xC59755,
    "Room $9C07: Brinstar reserve tank room": 0xC59B00,
    "Room $9C5E: Fireflea room": 0xC59CAC,
    "Room $9CB3: Dechora room": 0xC5A15F,
    "Room $9D19: Charge beam room": 0xC5B54D,
    "Room $9D9C: Pre Spore Spawn hall": 0xC5CBA7,
    "Room $9DC7: Spore Spawn": 0xC5CE34,
    "Room $9E11: Brinstar false wall super-sidehopper power bomb room": 0xC5D18F,
    "Room $9E52: Brinstar diagonal room": 0xC5D559,
    "Room $9E9F: Morph ball room": 0xC5DED5,
    "Room $9F11: Old Kraid entrance": 0xC5E63A,
    "Room $9F64: Blue Brinstar ceiling e-tank hall": 0xC5E86F,
    "Room $9FBA: n00b bridge": 0xC5ECAE,
    "Room $9FE5: Brinstar false floor beetom room": 0xC5EF71,
    "Room $A011: Brinstar false floor spike hall": 0xC5F057,
    "Room $A051: Brinstar post false floor super missiles": 0xC5F43E,
    "Room $A0A4: Post Spore Spawn supers hall": 0xC5F4C9,
    "Room $A0D2: Pink Brinstar flooded hall": 0xC5F778,
    "Room $A107: Blue Brinstar missile room": 0xC5FD50,
    "Room $A130: Brinstar sidehopper wave-gate room": 0xC5FE1B,
    "Room $A15B: Brinstar post side-hopper wave-gate energy tank": 0xC681C2,
    "Room $A1AD: Blue Brinstar boulder room": 0xC68318,
    "Room $A1D8: Blue Brinstar double missile room": 0xC68437,
    "Room $A253: Red Brinstar mainstreet": 0xC684EE,
    "Room $A293: Pre x-ray spike hall": 0xC691E3,
    "Room $A2CE: X-ray room": 0xC69BF9,
    "Room $A2F7: Red Brinstar damage boost hall": 0xC69D70,
    "Room $A322: Red Brinstar -> Crateria elevator": 0xC69F4B,
    "Room $A37C: Red Brinstar super-sidehopper power bomb floor room": 0xC6B31F,
    "Room $A3AE: Early power bombs room": 0xC6B58C,
    "Room $A3DD: Red Brinstar skree-duo hall": 0xC6B739,
    "Room $A408: Pre spazer room": 0xC6B91C,
    "Room $A447: Spazer room": 0xC6BCC7,
    "Room $A471: Kraid BTS madness": 0xC6BD83,
    "Room $A4B1: Kraid beetom room": 0xC6C469,
    "Room $A4DA: Kraid keyhunter hall": 0xC6C630,
    "Room $A521: Fake Kraid's room": 0xC6CDB9,
    "Room $A56B: Pre Kraid room": 0xC6D2CB,
    "Room $A59F: Kraid": 0xC6D620,
    "Room $A5ED: Pre Tourian hall": 0xC6D88D,
    "Unused": 0xC6DD77,
    "Room $A6A1: Kraid's lair entrance": 0xC6DEE0,
    "Room $A6E2: Varia suit room": 0xC6E355,
    "Room $A75D: Post ice beam mockball hall": 0xC6E4A4,
    "Room $A788: Norfair lava hidden missile room": 0xC6E5F5,
    "Room $A7B3: First hot room": 0xC6ECB9,
    "Room $A7DE: Norfair mainstreet": 0xC6F2E1,
    "Room $A815: Ice beam mockball hall": 0xC6F8C1,
    "Room $A865: Ice beam practice room": 0xC782ED,
    "Room $A890: Ice beam room": 0xC784A3,
    "Room $A8B9: Pre ice beam shaft": 0xC785D6,
    "Room $A8F8: Crumble block platform shaft": 0xC78A47,
    "Room $A923: Norfair slope": 0xC78CFA,
    "Room $A98D: Crocomire": 0xC79D71,
    "Room $A9E5: Hi-jump room": 0xC7A036,
    "Room $AA0E: Norfair grapple ceiling room": 0xC7A18D,
    "Room $AA41: Pre hi-jump room": 0xC7AA70,
    "Room $AA82: Post Crocomire room": 0xC7AEB3,
    "Room $AADE: Post Crocomire power bombs room": 0xC7B28B,
    "Room $AB07: Post Crocomire shaft": 0xC7B3E7,
    "Room $AB3B: Post Crocomire fluctuating acid missiles cave": 0xC7B780,
    "Room $AB64: Double lake grapple practice room": 0xC7BB6B,
    "Room $AB8F: Huge jump room": 0xC7BECB,
    "Room $ABD2: Grapple practice shaft": 0xC7CD91,
    "Room $AC00: Single lake grapple practice room": 0xC7CFCD,
    "Room $AC2B: Grapple room": 0xC7D13C,
    "Room $AC5A: Bubble Norfair reserve tank room": 0xC7D4FE,
    "Room $AC83: Bubble Norfair pre reserve tank room": 0xC7D66F,
    "Room $ACB3: Bubble Norfair mainstreet": 0xC7D895,
    "Room $ACF0: Speed booster lavaquake": 0xC7E08C,
    "Room $AD1B: Speed booster room": 0xC7EAA8,
    "Room $AD5E: Lower Norfair -> Bubble Norfair": 0xC7EC03,
    "Room $ADAD: Pre wave beam room": 0xC7FF02,
    "Room $ADDE: Wave beam room": 0xC88532,
    "Room $AE07: Norfair sinking kamer hall": 0xC8865C,
    "Room $AE32: Norfair funes and lavaquake room": 0xC88953,
    "Room $AE74: Pre Lower Norfair entrance shaft": 0xC8943A,
    "Room $AEB4: Norfair multiviola and lavamen hall": 0xC89D5D,
    "Room $AEDF: Pre 'useless cave' shaft": 0xC89FE3,
    "Room $AF14: Lower Norfair entrance": 0xC8A2CF,
    "Room $AF3F: Norfair -> Lower Norfair elevator": 0xC8AA89,
    "Room $AF72: Norfair wave gate room": 0xC8ABED,
    "Room $AFA3: Norfair long lavaquake hall": 0xC8B15B,
    "Room $AFCE: Boring near-Crocomire hall": 0xC8B4F9,
    "Room $AFFB: Norfair spike floor hall": 0xC8B853,
    "Room $B051: 'useless cave'": 0xC8B9CF,
    "Room $B07A: Pre speed booster lavaquake room": 0xC8BB21,
    "Room $B106: Norfair speed blockade hall": 0xC8BDE8,
    "Room $B139: Norfair stone zoomer shaft": 0xC8C165,
    "Room $B1E5: Golden chozo statue lava lake": 0xC8C4D3,
    "Unused": 0xC8CDA9,
    "Room $B236: Lower Norfair mainstreet": 0xC8D59C,
    "Room $B283: Golden Torizo": 0xC8E09D,
    "Room $B2DA: Screw attack practice": 0xC8E900,
    "Room $B32E: Ridley": 0xC8EBFD,
    "Room $B37A: Pre Ridley hall": 0xC8EDCE,
    "Room $B3A5: Lower Norfair power bomb floor shaft": 0xC8F01F,
    "Room $B3E1: Unused room": 0xC8F40B,
    "Room $B40A: Lower Norfair multi-level one-way shaft": 0xC8F58B,
    "Room $B457: Lower Norfair breakable pillars hall": 0xC8FCC5,
    "Room $B482: Lower Norfair holtz room": 0xC98222,
    "Room $B4AD: Lower Norfair wall jumping space pirates shaft": 0xC984D3,
    "Room $B4E5: Lower Norfair lavaquake room": 0xC9899F,
    "Room $B510: Lower Norfair mini metal maze room": 0xC994BA,
    "Room $B55A: Lower Norfair crumble walls power bomb room": 0xC99CE2,
    "Room $B585: Lower Norfair kihunter shaft": 0xC99E7B,
    "Room $B5D5: Lower Norfair super desgeega hall": 0xC9A88C,
    "Room $B62B: Elite pirate hall": 0xC9B1C7,
    "Room $B656: Impossible's x-ray room": 0xC9B4AB,
    "Room $B698: Ridley's energy tank": 0xC9C30D,
    "Room $B6C1: Screw attack shaft": 0xC9C428,
    "Room $B6EE: Norfair rolling boulder shaft": 0xC9C706,
    "Room $CEFB, state $CF0D: n00b tube": 0xC9DB52,
    "Room $CEFB, state $CF27: n00b tube": 0xC9E129,
    "Room $CF54: n00b tube west": 0xC9E6AE,
    "Room $CF80: n00b tube east": 0xC9E809,
    "Room $CFC9: Maridia mainstreet": 0xC9F225,
    "Room $D017: Maridia space pirate room": 0xCA8EFF,
    "Room $D055: Maridia spinning turtle room": 0xCAA113,
    "Room $D08A: Maridia green gate hall": 0xCAAF99,
    "Room $D0B9: Mt. Doom": 0xCAB24F,
    "Room $D104: Maridia -> Red Brinstar room": 0xCACE42,
    "Room $D13B: Sandy Maridia missile and super missile room": 0xCAD474,
    "Room $D16D: Sandy Maridia memu room": 0xCADBC8,
    "Room $D1A3: Maridia pink room": 0xCAE458,
    "Room $D1DD: Sandy Maridia unused passage to Sandy Maridia mainstreet": 0xCAF59C,
    "Room $D21C: Maridia broken glass tube room": 0xCB83DB,
    "Room $D252: Maridia broken glass tube room east": 0xCB883A,
    "Room $D27E: Plasma beam puyo room": 0xCB89E0,
    "Room $D2AA: Plasma beam room": 0xCB8BD4,
    "Room $D2D9: Sandy Maridia thin platform hall": 0xCB9792,
    "Room $D30B: Maridia -> Crateria elevator": 0xCBA0D0,
    "Room $D340: Sandy Maridia mainstreet": 0xCBA878,
    "Room $D387: Pre plasma beam shaft": 0xCBC64F,
    "Room $D408: Maridia elevatube": 0xCBCD9F,
    "Room $D433: Sandy Maridia drowning sand pit room": 0xCBDCF3,
    "Room $D461: Sand falls west": 0xCBDE8F,
    "Room $D48E: Elevatube south": 0xCBE472,
    "Room $D4C2: Sand falls east": 0xCBE899,
    "Room $D4EF: Maridia reserve tank room": 0xCBEC32,
    "Room $D51E: PB #66 room": 0xCBF580,
    "Room $D54D: Pre Maridia reserve tank room sand fall room": 0xCBFEC8,
    "Room $D57A: Pre PB #66 room sand fall room": 0xCC80B8,
    "Room $D5A7: Snail room": 0xCC82A8,
    "Room $D5EC: Sandy Maridia sand pit room": 0xCCA13B,
    "Room $D617: Mochtroid room": 0xCCA34A,
    "Room $D646: Pre Shaktool shaft": 0xCCAC48,
    "Room $D69A: Pre Shaktool shaft section": 0xCCB843,
    "Room $D6D0: Springball room": 0xCCBD31,
    "Room $D6FD: Sand falls sand pit": 0xCCC22F,
    "Room $D72A: Maridia grapple room": 0xCCC9F1,
    "Room $D78F: Pre Draygon room": 0xCCE5B1,
    "Room $D7E4: Maridia speed blockade hall": 0xCCEE0C,
    "Room $D86E: Sandy Maridia sand falls room": 0xCCFA8D,
    "Room $D898: Sand falls": 0xCCFB88,
    "Room $D8C5, state $D8D7: Shaktool": 0xCCFD75,
    "Room $D8C5, state $D8F1: Shaktool": 0xCD8404,
    "Room $D913: Maridia grapple wall shaft": 0xCD8A37,
    "Room $D95E: Botwoon": 0xCD950E,
    "Room $D9AA: Space jump room": 0xCD991E,
    "Room $D9FE: Plasma beam shortcut cacatac room": 0xCD9B28,
    "Room $DA2B: Plasma beam shortcut spike room": 0xCDA00D,
    "Room $DA60: Draygon": 0xCDB19D,
    "Room $DF45: Ceres elevator shaft": 0xCDB846,
    "Room $DF8D: Ceres pre elevator hall": 0xCDBBFE,
    "Room $DFD7: Ceres stairs": 0xCDBD78,
    "Room $E021: Ceres baby metroid hall": 0xCDBFC9,
    "Room $E06B: Pre Ceres Ridley hall": 0xCDC330,
    "Room $E0B5: Ceres Ridley": 0xCDC43F,
    "Room $DAAE: Tourian -> Crateria elevator": 0xCDC4FE,
    "Room $DAE1: Metroid room 1": 0xCDC8DC,
    "Room $DB31: Metroid room 2": 0xCDCDA0,
    "Room $DB7D: Metroid room 3": 0xCDD02D,
    "Room $DBCD: Metroid room 4": 0xCDD3E5,
    "Room $DC19: Tourian super-sidehopper room": 0xCDD5EB,
    "Room $DC65: Drained Torizo room": 0xCDD7C4,
    "Room $DCB1: Shitroid room": 0xCDD930,
    "Room $DCFF: Post Shitroid room": 0xCDDBF8,
    "Room $DD58: Mother Brain": 0xCDDEDE,
    "Room $DDC4: Tourian eye-door room": 0xCDE20F,
    "Room $DDF3: Pre Mother Brain shaft": 0xCDE518,
    "Room $DE4D: Escape room 1": 0xCDE914,
    "Room $DE7A: Escape room 2": 0xCDEB5B,
    "Room $DEA7: Escape room 3": 0xCDED7A,
    "Room $DEDE: Escape room 4": 0xCDF534,
    "Room $9C35/$B0B4/$CCCB: Map station - right side door": 0xCE83C3,
    "Room $9994/$D3B6: Map station - left side door": 0xCE86BD,
    "Room $A07B/$A618: Energy station - right side door": 0xCE89B6,
    "Room $9C89: Missile station - right side door": 0xCE8CB3,
    "Room $B026: Energy station - both doors": 0xCE8FA6,
    "Room $93D5/$A184/$A201/$A22A/$B0DD/$B1BB/$D765/$DE23: Save station - right side door": 0xCE92CB,
    "Room $A70B/$A734/$AAB5/$B192/$B741/$CE8A/$CED2/$D3DF/$DF1B: Save station - left side door": 0xCE95C2,
    "Room $B305/$D9D4: Energy station - left side door": 0xCE98DC,
    "Room $A66A: Tourian entrance": 0xCE9BE9,
    "Room $B167/$D81A: Draygon save station - both doors": 0xCE9EF6,
    "Room $A641: Refill station - left side door": 0xCEA201,
    "Unused": 0xCEA503,
    "Room $DD2E: Refill station - right side door": 0xCEA823,
    "Room $D845: Missile station - left side door": 0xCEAB31,
    "Room $E82C: Debug room": 0xCEAE3E,

    "CRE tiles": 0xB98000,
    "CRE tile table": 0xB9A09D,
}

max_cpu = multiprocessing.cpu_count()

def wait_for_child(processes):
    while True:
        for p in processes:
            if p.poll() is not None:
                processes.remove(p)
                return
        time.sleep(0.1)

if decomp_name is None:

    print("{:>48} | {:>8} | {:>8} | {:>8} | Result".format("Name", "Address", "VC", "U"))
    print("-"*100)

    processes = []
    for name, address in addresses.items():
        p = subprocess.Popen([getPythonExec(), os.path.join(dir_path, 'tools', 'test_compress.py'),
                              romFile, name, str(address)])
        processes.append(p)

        if len(processes) == max_cpu:
            wait_for_child(processes)

    for p in processes:
        p.wait()
else:
    rom = RealROM(romFile)
    #init(True)
    output = Compressor().decompress(rom, snes_to_pc(decomp_address))
    vanilla_compressed_length, data = output

    #print("")
    #print("#"*128)
    #print("")

    start = datetime.now()
    compressed = Compressor().compress(data)
    end = datetime.now()
    duration = (end - start).total_seconds() * 1000
    recompressed_length = len(compressed)

    #print("")
    #print("#"*128)
    #print("")

    # decompress again to validate same data
    pc_address = snes_to_pc(decomp_address)
    fake = FakeROM({pc_address+i: v for i, v in enumerate(compressed)})
    _, ddata = Compressor().decompress(fake, pc_address)
    assert data == ddata, "{} Buggy compression !".format(decomp_name)

    print("{:>48} | {:>8} | {:>8} | {:>8} | {}{} {}ms".format(decomp_name, hex(decomp_address),
                                                              vanilla_compressed_length, len(data),
                                                              "XX " if recompressed_length > vanilla_compressed_length else "",
                                                              recompressed_length, round(duration, 2)))

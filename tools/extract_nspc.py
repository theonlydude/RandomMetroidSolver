#!/usr/bin/python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# extract vanilla soundtrack as nspc files. args:
# - vanilla ROM
# - path to nspc directory. *has* to be one level deeper than music base dir
# - path to JSON metadata file to write.
# will also parse room state headers, and list pointers where
# music data/track has to be written, ie track number >= 5
# also lists the extra pointers for area rando, all of this
# stored in the JSON metadata

from rom.rom import RealROM, snes_to_pc

vanilla=sys.argv[1]
nspc_dir=sys.argv[2]
json_path=sys.argv[3]

rom=RealROM(vanilla)
musicDataTable = snes_to_pc(0x8FE7E4)
musicDataEnd = snes_to_pc(0xDED1C0)
# tracks pointed  music table, in that order
# array is songs in music data: (name, spc_path)
vanillaMusicData = [
    # Song 0: intro,
    # Song 1: menu theme
    [("Title sequence intro", "vanilla/title_menu.spc"),
     ("Menu theme", None)],
    # Song 0: thunder - zebes asleep,
    # Song 1: thunder - zebes awake,
    # Song 2: no thunder (morph room...)
    [("Crateria Landing - Thunder, Zebes asleep", "vanilla/crateria_arrival.spc"),
     ("Crateria Landing - Thunder, Zebes awake", "vanilla/crateria_rainstorm.spc"),
     ("Crateria Landing - No Thunder", "vanilla/crateria_underground.spc")],
    # Song 0: Main theme,
    # Song 1: Tourian Entrance
    [("Crateria Pirates", "vanilla/crateria_pirates.spc"),
     ("Tourian Entrance", "vanilla/tourian_entrance.spc")],
    # Song 0: Upper Crateria with PBs/outside Wrecked Ship
    [("Samus Theme", "vanilla/samus_theme.spc")],
    [("Green Brinstar", "vanilla/green_brinstar.spc")],
    [("Red Brinstar", "vanilla/red_brinstar.spc")],
    [("Upper Norfair", "vanilla/upper_norfair.spc")],
    [("Lower Norfair", "vanilla/lower_norfair.spc")],
    # Song 0: East Maridia,
    # Song 1: West Maridia
    [("East Maridia", "vanilla/east_maridia.spc"),
     ("West Maridia", "vanilla/west_maridia.spc")],
    # Song 0: Tourian, Song 1: no music
    [("Tourian", "vanilla/tourian.spc")],
    [("Mother Brain", "vanilla/mother_brain.spc")],
    # Song 0: BT/Ridley/Draygon,
    # Song 1: BT tension,
    # Song 2: Escape
    [("Boss fight - BT/Ridley/Draygon", "vanilla/boss1.spc"),
     ("Boss fight - BT tension", "vanilla/bt_tension.spc"),
     ("Escape", "vanilla/escape.spc")],
    # Song 0: Kraid/Phantoon/Croc,
    # Song 1: Tension
    [("Boss fight - Kraid/Phantoon/Croc", "vanilla/boss2.spc"),
     ("Boss fight - Kraid/Phantoon/Croc tension", "vanilla/tension.spc")],
    # Song 0: Spore Spawn/Botwoon
    [("Boss fight - Spore Spawn/Botwoon", "vanilla/mini_boss.spc")],
    # Song 0: Flying to Ceres,
    # Song 1: Ceres,
    # Song 2: Flying to Zebes,
    # Song 3: Ceres time up
    [("Flying to Ceres", "vanilla/space_ship.spc"),
     ("Ceres", "vanilla/ceres.spc"),
     ("Flying to Zebes", "vanilla/to_zebes.spc"),
     ("Ceres time up", "vanilla/ceres_explodes.spc")],
    # Song 0: Power off,
    # Song 1: Power on
    [("Wrecked Ship - Power off", "vanilla/wrecked_ship_off.spc"),
     ("Wrecked Ship - Power on", "vanilla/wrecked_ship_on.spc")],
    [("Zebes boom", "vanilla/zebes_explodes.spc")],
    [("Intro", "vanilla/intro.spc")],
    [("Death", "vanilla/samus_cry.spc")],
    [("Ending/Credits", "vanilla/ending.spc")],
    [("The last Metroid is in captivity", None)],
    [("The galaxy is at peace", None)],
    # Song 0: Boss music,
    # Song 1: Pre-boss music,
    # Song 2: No music
    [("Baby Metroid", "vanilla/boss2.spc"),
     ("Baby Metroid - Tension", "vanilla/tension.spc"),
     ("Baby Metroid - No music", None)],
    [("Mother Brain 3 (Samus Theme 2)", "vanilla/samus_theme.spc")]
]

metadata = {}

for i in range(len(vanillaMusicData)):
    addr = musicDataTable+i*3
    ptr = snes_to_pc(rom.readLong(addr))
    if i < len(vanillaMusicData)-1:
        # vanilla data ptrs are conveniently sorted
        endptr = snes_to_pc(rom.readLong(addr+3))
    else:
        endptr = musicDataEnd
    rom.seek(addr)
    nspc_path = "%s/vanilla_%06x_%06x.nspc" % (nspc_dir, ptr, endptr-1)
    print("Writing %s ..." % nspc_path)
    rom.seek(ptr)
    with open(nspc_path, "wb") as nspc:
        nspc.write(rom.read(endptr-ptr))
    musicdata = vanillaMusicData[i]
    for j in range(len(musicdata)):
        track = musicdata[j][0]
        spc_path = musicdata[j][1]
        h,t=os.path.split(nspc_path)
        metadata[track] = {
            'nspc_path':os.path.join(os.path.split(h)[1], t),
            'data_index':i,
            'track_index':j,
            'original_author':'Kenji Yamamoto',
            'port_author': '',
            'description': "Original track from vanilla Super Metroid"
        }
        if spc_path is not None:
            metadata[track]['spc_path'] = spc_path

# key: music ID (music data, music track)
# value: track name
tracksByMusicId = {}

for i in range(len(vanillaMusicData)):
    dataId = (i+1)*3
    tracks = vanillaMusicData[i]
    for j in range(len(tracks)):
        trackId = j+5
        track = tracks[j][0]
#        print("(%d, %d) = %s" % (dataId, trackId, track))
        tracksByMusicId[(dataId, trackId)] = track

# now parse room headers, and get song data addresses in metadata
# (a lot of it is copy-pasted from gen_area_in_rooms, well that's
#  how it goes for one-time use tools I guess)
statesChecksArgSize = {
    0xe5eb: 2,
    0xe612: 1,
    0xe629: 1
}

from rooms import rooms

for room in rooms:
#    print(room['Name'])
    def processState(stateWordAddr):
        pc_addr = (0x70000 | stateWordAddr) + 4
        rom.seek(pc_addr)
        dataId = int(rom.readByte())
        trackId = int(rom.readByte())
        if dataId == 0x0 and trackId >= 0x5:
            # helper to have addresses of special rooms to be input by hand below.
            # indeed, there is no way to guess the intended dataId, as it will be
            # in a nearby room.
            print("Special - %s (SMILE ID %X) : %d" % (room['Name'], room['Address'], pc_addr))
        if dataId > 0 and trackId >= 0x5 and trackId != 0x80:
            track = tracksByMusicId[(dataId, trackId)]
            trackMeta = metadata[track]
            if 'pc_addresses' not in trackMeta:
                trackMeta['pc_addresses'] = []
            trackMeta['pc_addresses'].append(pc_addr)
    address = room['Address']+11
    while True:
        w=rom.readWord(address)
        if w == 0xe5e6:
            break
        address += 2 + statesChecksArgSize.get(w, 0)
        processState(rom.readWord(address))
        address += 2
    # default state
    processState((address+2)-0x70000)

# extra addresses for special music (see custom_music.asm patch)
def addExtraAddress(track, snesAddress=None, pcAddress=None):
    assert (snesAddress is None) != (pcAddress is None)
    if "pc_addresses" not in metadata[track]:
        metadata[track]["pc_addresses"] = []
    if pcAddress is None:
        pcAddress = snes_to_pc(snesAddress)
    metadata[track]["pc_addresses"].append(pcAddress)

addExtraAddress("Title sequence intro", 0x8FE86D)
addExtraAddress("Menu theme", 0x8FE86F)
addExtraAddress("Escape", 0x8FE871)
addExtraAddress("Ending/Credits", 0x8FE873)
addExtraAddress("Mother Brain 3 (Samus Theme 2)", 0x8FE875)
addExtraAddress("Mother Brain", 0x8FE877)

# add random start music (no impact if not random start as it is current area music anyway)
addExtraAddress("Crateria Pirates", 0x8F99CE) # gauntlet
addExtraAddress("West Maridia", 0x8FD14C) # watering hole
addExtraAddress("West Maridia", 0x8FD066) # mama turtle
addExtraAddress("Green Brinstar", 0x8FA062) # etecoon supers
addExtraAddress("Lower Norfair", 0x8FB56B) # firefleas

# add special rooms to force data ID and avoid to handle (00, trackId) cases
# (at the occasional cost of some load time during transition)

# Pit Room [Old Mother Brain Room]: forces track one because of elevator room (in zebes alseep state)
addExtraAddress("Crateria Landing - Thunder, Zebes asleep", pcAddress=497521)
# [Crab Maze to Elevator] : no idea why vanilla loads 'crateria pirates' in the first place from maridia elevator,
# as it is Samus Theme when coming from the other way
addExtraAddress("Samus Theme", pcAddress=497081)
# Lower Mushrooms : vanilla loads space pirates theme in the elevator.
# The other room in this case (Green Pirates Shaft), is already handled above for gauntlet start.
addExtraAddress("Crateria Pirates", pcAddress=498042)
# Early Supers Room: forces track one because of item room
addExtraAddress("Green Brinstar", pcAddress=498649)
# Red Brinstar Fireflea Room: forces track one because of item room
addExtraAddress("Red Brinstar", pcAddress=500388)
# Below Spazer: forces track one because of item room
addExtraAddress("Red Brinstar", pcAddress=500761)
# Warehouse Zeela Room: forces track one because of elevator room
addExtraAddress("Red Brinstar", pcAddress=500866)
# Ice Beam Snake Room: forces track one because of item room
addExtraAddress("Upper Norfair", pcAddress=501962)
# Hi Jump Energy Tank Room: forces track one because of item room
addExtraAddress("Upper Norfair", pcAddress=502354)
# Post Crocomire Jump Room: forces track one because of item room
addExtraAddress("Upper Norfair", pcAddress=502688)
# Grapple Tutorial Room 1: forces track one because of item room
addExtraAddress("Upper Norfair", pcAddress=502801)
# Speed Booster Hall: forces track one because of item room
addExtraAddress("Upper Norfair", pcAddress=503041)
# Double Chamber: forces track one because of item room
addExtraAddress("Upper Norfair", pcAddress=503230)
# Lava Dive Room: forces track one because of elevator room
addExtraAddress("Upper Norfair", pcAddress=503589)
# Bat Cave: forces track one for no reason (should be a 00/00 room)
addExtraAddress("Upper Norfair", pcAddress=503947)
# Lower Norfair Spring Ball Maze Room: forces track one for no reason (should be a 00/00 room)
addExtraAddress("Lower Norfair", pcAddress=505121)
# Plasma Spark Room: forces track one for no reason (should be a 00/00 room)
addExtraAddress("East Maridia", pcAddress=512849)
# Plasma Climb: forces track one because of item room
addExtraAddress("East Maridia", pcAddress=512920)

# finally, add extra addresses for area/boss rando
from graph.vanilla.graph_access import accessPoints

for ap in accessPoints:
    if ap.EntryInfo is not None and 'song' in ap.EntryInfo:
        dataId = ap.EntryInfo['song']
        trackId = 0x5
        track = tracksByMusicId[(dataId, trackId)]
        trackMeta = metadata[track]
        key = 'pc_addresses_area' if not ap.Boss else 'pc_addresses_boss'
        if key not in trackMeta:
            trackMeta[key] = []
        trackMeta[key] += [0x70000 | a for a in ap.RoomInfo['songs']]

print("Writing %s ..." % json_path)
with open(json_path, 'w') as fp:
    json.dump(metadata, fp, indent=4)

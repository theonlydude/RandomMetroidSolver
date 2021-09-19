#!/usr/bin/python3

import sys, os, json

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# helper tool to debug written music data of seeds with customized music:
# use the playlist to find original tracks nspc data and compare

from rom.rom import RealROM, snes_to_pc
from rom.rompatcher import MusicPatcher,RomTypeForMusic
from utils.parameters import appDir

seed=sys.argv[1]
playlist_json=sys.argv[2]

# load args
rom=RealROM(seed)
with open(playlist_json, 'r') as f:
    playlist=json.load(f)

# use patcher ctor to load music metadata
p=MusicPatcher(rom, RomTypeForMusic.VariaSeed, baseDir=os.path.join(appDir+'/..', 'varia_custom_sprites', 'music'))
vanillaTracks=p.vanillaTracks
allTracks=p.allTracks
tableAddr=p.musicDataTableAddress-3
baseDir=p.baseDir
preserved=p.constraints['preserve']

# build the music data table to expect:
# dataId => expected nspc file path
# dataId is direct offset from tableAddr
expected_table = {}

# helper function that work with modified names from playlist
def getVanillaTrackData(vTrack):
    if vTrack not in vanillaTracks:
        for track in vanillaTracks:
            if vTrack == ''.join(e for e in track if e.isalnum()):
                vTrack = track
                break
    assert vTrack in vanillaTracks, "Invalid vanilla track name: "+vTrack
    return vanillaTracks[vTrack]

def updateTable(dataId, rTrack, vTrack):
    expected_nspc = os.path.join(baseDir, allTracks[rTrack]['nspc_path'])
    if dataId in expected_table and expected_nspc != expected_table[dataId]:
        print("Inconsistent music table!")
        print("dataId=$%02x, vTrack=%s, rTrack=%s, previous=%s" % (dataId,vTrack,rTrack,expected_table[dataId]))
    expected_table[dataId] = expected_nspc
    print("Data $%02x, expected data from track %s" % (dataId, rTrack))

# custom tracks
for vTrack,rTrack in playlist.items():
    vTrackData = getVanillaTrackData(vTrack)
    addr = vTrackData['pc_addresses'][0]
    dataId = rom.readByte(addr)
    updateTable(dataId, rTrack, vTrack)

# preserved tracks
for vTrack in preserved:
    vTrackData = getVanillaTrackData(vTrack)
    dataId = (vTrackData['data_index']+1)*3
    updateTable(dataId, vTrack, vTrack)

# compare nspc data and dump if different than expected
for dataId, expected_nspc in expected_table.items():
    with open(expected_nspc, 'rb') as f:
        expected_music_data = f.read()
    sz = len(expected_music_data)
    addr = snes_to_pc(rom.readLong(tableAddr+dataId))
    rom.seek(addr)
    music_data = rom.read(sz)
    if music_data != expected_music_data:
        print("Music data $%02x differ from the one of %s !" % (dataId, expected_nspc))
        out_nspc = "track_%02x.nspc" % dataId
        print("Dumping it in %s ..." % out_nspc)
        with open(out_nspc, 'wb') as f:
            f.write(music_data)

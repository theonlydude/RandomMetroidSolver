#!/usr/bin/python3

import sys, os, json, hashlib

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc, pc_to_snes
from rom.rompatcher import MusicPatcher,RomTypeForMusic
from rom.addresses import Addresses
from utils.parameters import appDir
from utils.utils import removeChars

seed=sys.argv[1]
baseDir=os.path.join(appDir+'/..', 'varia_custom_sprites', 'music')
rom=RealROM(seed)
p=MusicPatcher(rom, RomTypeForMusic.VariaSeed, baseDir=baseDir)
vanillaTracks=p.vanillaTracks
allTracks=p.allTracks
tableAddr=Addresses.getOne('musicDataTable')-3
nspcMetaPath = os.path.join(baseDir, "nspc_metadata.json")
with open(nspcMetaPath, "r") as f:
    nspcMeta = json.load(f)

def readNspcData(rom, addr):
    # songs can have two tracks
    nspcCount = 0
    step = 0
    data = []
    maxSize = 64*1024
    rom.seek(addr)
    for i in range(maxSize):
        b = rom.readByte()
        data.append(b)
        if step == 0:
            if b == 0x00:
                step = 1
        elif step == 1:
            if b == 0x00:
                step = 2
            else:
                step = 0
        elif step == 2:
            if b == 0x00:
                step = 3
            else:
                step = 0
        elif step == 3:
            if b == 0x15:
                # end found
                if nspcCount == 0:
                    firstData = data[:]
                    nspcCount = 1
                    step = 0
                else:
                    return (firstData, data)
            elif b != 0x00:
                step = 0

    if nspcCount == 0:
        #with open("{}.nspc".format(hex(addr)), 'wb') as f:
        #    f.write(bytes(data))
        return (None, None)
    else:
        return (firstData, None)

def getMd5Sum(data):
    return hashlib.md5(bytes(data)).hexdigest()

# read table
tracksTable = {}
for trackName, data in vanillaTracks.items():
    if 'pc_addresses' not in data:
        continue
    addr = data['pc_addresses'][0]
    dataId = rom.readByte(addr)
    addr = snes_to_pc(rom.readLong(tableAddr+dataId))
    print("dataId: {} - addr: {} for song: {}".format(hex(dataId), hex(addr), trackName))
    tracksTable[addr] = {"trackName": trackName, "dataId": dataId}

# get nspc data in rom and compute its md5 sum
for addr in sorted(tracksTable.keys()):
    trackData = tracksTable[addr]
    #print("{} {:4} {}".format(hex(pc_to_snes(addr)), hex(trackData["dataId"]), trackData["trackName"]))
    nspcData = readNspcData(rom, addr)
    if nspcData[0] is None and nspcData[1] is None:
        print("  Warning: no nspc end found for {}".format(trackData["trackName"]))
        tracksTable[addr]["nspcData"] = [None]
        tracksTable[addr]["nspc_md5sum"] = [None]
        continue

    md5sum = getMd5Sum(nspcData[0])
    tracksTable[addr]["nspcData"] = [nspcData[0]]
    tracksTable[addr]["nspc_md5sum"] = [md5sum]

    if nspcData[1] is not None:
        md5sum = getMd5Sum(nspcData[1])
        tracksTable[addr]["nspcData"].append(nspcData[1])
        tracksTable[addr]["nspc_md5sum"].append(md5sum)

# index by md5sum
allTracksMd5 = {}
for songName, data in allTracks.items():
    allTracksMd5[nspcMeta[data["nspc_path"]]["md5sum"]] = songName

playlist = {}
for data in tracksTable.values():
    md5sums = data["nspc_md5sum"]
    if md5sums[0] in allTracksMd5 or (len(md5sums) > 1 and md5sums[1] in allTracksMd5):
        md5sum = md5sums[0] if md5sums[0] in allTracksMd5 else md5sums[1]
        #print("$%02x %s replaced with: %s" % (data["dataId"], data["trackName"], allTracksMd5[md5sum]))
        playlist[removeChars(data["trackName"], ' ,()-/')] = allTracksMd5[md5sum]
    else:
        print("  Warning: replacement not found for {} - {} - {}".format(hex(data["dataId"]), data["trackName"], data["nspc_md5sum"]))

playlistName = sys.argv[1][:-4]+'.json'
with open(playlistName, 'w') as f:
    json.dump(playlist, f, indent=4)

print("playlist generated: {}".format(playlistName))

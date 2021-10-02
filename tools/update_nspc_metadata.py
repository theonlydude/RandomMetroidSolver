#!/usr/bin/python3

import sys, os, json, hashlib

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# goes through music tracks metadata to update metadata about music
# data (everything that is not on track level, but at data level)

from rom.rom import RealROM

music_dir=sys.argv[1]

metadata_dir = os.path.join(music_dir, "_metadata")
outPath = os.path.join(music_dir, "nspc_metadata.json")
nspc_meta = {}

allTracks = {}
for metaFile in os.listdir(metadata_dir):
    metaPath = os.path.join(metadata_dir, metaFile)
    if not metaPath.endswith(".json"):
        continue
    with open(metaPath, 'r') as f:
        meta = json.load(f)
    allTracks.update(meta)

def getMd5Sum(nspcFileName):
    with open(nspcFileName, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    return md5

def getBlockHeaderOffsets(nspcFileName):
    offsets = []
    f = RealROM(nspcFileName)
    addr = 0
    while True:
        offsets.append(addr)
        blkSize = f.readWord(addr)
        if blkSize == 0:
            break
        addr += 4 + blkSize # 4 is the size of the header itself
    return offsets

for trackName, trackData in allTracks.items():
    if trackData['nspc_path'] in nspc_meta:
        continue
    meta = {}
    nspc_meta[trackData['nspc_path']] = meta
    nspc_path = os.path.join(music_dir, trackData['nspc_path'])
    # MD5
    meta["md5sum"] = getMd5Sum(nspc_path)
    # data block headers offset within music data. when written, they shall not cross banks
    meta["block_headers_offsets"] = getBlockHeaderOffsets(nspc_path)

with open(outPath, 'w') as f:
    json.dump(nspc_meta, f, indent=4)

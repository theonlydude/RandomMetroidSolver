#!/usr/bin/python3

import sys, os, json, hashlib

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rom import RealROM, snes_to_pc
from utils.parameters import appDir

baseDir=os.path.join(appDir+'/..', 'varia_custom_sprites', 'music')
metaDir = os.path.join(baseDir, "_metadata")

def getMd5Sum(nspcFileName):
    return hashlib.md5(open(os.path.join(baseDir, nspcFileName),'rb').read()).hexdigest()

allMetas = {}
for metaFile in os.listdir(metaDir):
    metaPath = os.path.join(metaDir, metaFile)
    if not metaPath.endswith(".json"):
        continue
    with open(metaPath, 'r') as f:
        allMetas[metaFile] = json.load(f)

for metaFile, meta in allMetas.items():
    for song, data in meta.items():
        data['md5sum'] = getMd5Sum(data['nspc_path'])

    metaPath = os.path.join(metaDir, metaFile)
    with open(metaPath, 'w') as f:
        json.dump(meta, f, indent=4)

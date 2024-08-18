#!/usr/bin/python3

# impot custom music from another source tree, fixing file names in the process
# produces 3 files to ease merging :
# - new.json : actual new tracks, can be added as metadata file of its own, or appended to existing. spc/nspc files are copied
# - updated.json : existing tracks that have updated metadata. spc/nspc files are copied.
# - conflict.json : renamed tracks for which we found a matching NSPC (added as original_nspc in entries). spc/nspc files are untouched.

import sys, os, re, json, copy, shutil, filecmp

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from rom.rompatcher import MusicPatcher

dirFrom = sys.argv[1]
dirTo = sys.argv[2]

patcherFrom = MusicPatcher(None, 0, dirFrom)
patcherTo = MusicPatcher(None, 0, dirTo)

nspcByChecksum = {}
for nspc, info in patcherTo.nspcInfo.items():
    nspcByChecksum[info["md5sum"]] = nspc

illegalCharsRegex = re.compile(r'[^a-zA-Z0-9\-._/]')
fixPath = lambda p: re.sub(illegalCharsRegex, "_", p)

def nspcExistsInDestination(fromTrackData):
    nspc = patcherFrom._nspc_path(fromTrackData["nspc_path"])
    info = patcherFrom.nspcInfo.get(nspc)
    return nspcByChecksum.get(info["md5sum"]) if info else None

def copyFile(src_path, dest_path):
    src_path = os.path.join(dirFrom, src_path)
    dest_path = os.path.join(dirTo, dest_path)
    if os.path.exists(dest_path) and filecmp.cmp(src_path, dest_path, shallow=False):
        return False
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copy2(src_path, dest_path)
    return True

def copyTrackData(orig):
    trackData = copy.copy(orig)
    trackData["nspc_path"] = fixPath(trackData["nspc_path"])    
    modified = copyFile(orig["nspc_path"], trackData["nspc_path"])
    spc = trackData.get("spc_path")
    if spc is not None and len(spc) > 0:
        trackData["spc_path"] = fixPath(spc)
        modified |= copyFile(orig["spc_path"], trackData["spc_path"])
    return trackData, modified

def eqTrackData(a, b):
    filtered = ["spc_path", "nspc_path"]
    filt_a = {k:v for k, v in a.items() if k not in filtered}
    filt_b = {k:v for k, v in b.items() if k not in filtered}
    return filt_a == filt_b

newTracks = {}
conflictingTracks = {}
updatedTracks = {}

for fromTrack, fromTrackData in patcherFrom.allTracks.items():
    toTrackData = patcherTo.allTracks.get(fromTrack)
    if toTrackData is None:
        existingNspc = nspcExistsInDestination(fromTrackData)
        if not existingNspc:
            # actual new track, copy info and NSPC/SPC files
            newTracks[fromTrack], _ = copyTrackData(fromTrackData)
        else:
            # conflicting track
            conflictingTracks[fromTrack] = copy.copy(fromTrackData)
            conflictingTracks[fromTrack]['original_nspc'] = existingNspc
    else:
        # compare/update track data (including actual spc/nspc file contents)
        trackData, modified = copyTrackData(fromTrackData)        
        if not eqTrackData(trackData, toTrackData) or modified:
            updatedTracks[fromTrack] = trackData

with open("new.json", 'w') as fp:
    json.dump(newTracks, fp, indent=4)
with open("conflict.json", 'w') as fp:
    json.dump(conflictingTracks, fp, indent=4)
with open("updated.json", 'w') as fp:
    json.dump(updatedTracks, fp, indent=4)

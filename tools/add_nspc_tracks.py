#!/usr/bin/python3

import sys, os, json, hashlib

# we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

# will do its best to automate importation of a set of related nspc
# tracks but some stuff will still have to be done manually like
# proper naming of the tracks etc. at least a json will be generated,
# that can be edited afterwards

directory=sys.argv[1]
if directory.endswith('/'):
    directory=directory[:-1]
json_path=sys.argv[2]
orig_auth=sys.argv[3] if len(sys.argv) > 3 else ''
port_auth=sys.argv[4] if len(sys.argv) > 4 else ''
desc=sys.argv[5] if len(sys.argv) > 5 else ''

files=os.listdir(directory)
metadata={}

dbase=os.path.split(directory)[1]

def getMd5Sum(nspcFileName):
    return hashlib.md5(open(nspcFileName,'rb').read()).hexdigest()

for f in files:
    dname,e=os.path.splitext(f)
    if e == ".bin" or e == ".nspc":
        spc_files = [s for s in files if s.startswith(dname) and s.endswith(".spc")]
        nb_tracks = len(spc_files)
        if nb_tracks == 0:
            nb_tracks = 1
        for i in range(nb_tracks):
            tname = dname
            if i > 0:
                tname += "_"+str(i)
            metadata[tname] = {
                "nspc_path":os.path.join(dbase,f),
                "track_index":i,
                "original_author":orig_auth,
                "port_author":port_auth,
                "description":desc,
                "nspc_md5sum": getMd5Sum(os.path.join(directory,f))
            }
            metadata[tname]['spc_path'] = os.path.join(dbase, spc_files[i]) if len(spc_files) > 0 else ''

with open(json_path, 'w') as fp:
    json.dump(metadata, fp, indent=4)

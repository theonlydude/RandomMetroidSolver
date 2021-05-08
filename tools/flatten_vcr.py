#!/usr/bin/python3
# remove rollbacks from a VCR file

import sys, os, json

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

vcrFileName = sys.argv[1]

with open(vcrFileName) as jsonFile:
    vcrData = json.load(jsonFile)

flattenVcr = []

for action in vcrData:
    if action["type"] == 'rollback':
        for i in range(action["count"]):
            flattenVcr.pop()
    else:
        flattenVcr.append(action)

if len(vcrData) == len(flattenVcr):
    print("no rollback in VCR")
else:
    (base, ext) = os.path.splitext(vcrFileName)
    flattenVcrFileName = "{}.flatten{}".format(base, ext)

    with open(flattenVcrFileName, 'w') as jsonFile:
        json.dump(flattenVcr, jsonFile)

    print("rollbacks removed from VCR: {}".format(flattenVcrFileName))

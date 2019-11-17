#!/usr/bin/python

from utils import PresetLoader
import os, sys

def loadPresetsList(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f != 'solution.json']

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit()

    presets = loadPresetsList(sys.argv[1])

    for preset in presets:
        print(preset)

        loader = PresetLoader.factory(preset)

        # check
#        for know in ['GravLessLevel1', 'GravLessLevel3']: #['SuitlessOuterMaridia', 'SuitlessSandpit', 'GravLessLevel1', 'GravLessLevel3']:
#            if know in loader.params['Knows']:
#                print "{} in {}: {}".format(know, preset, loader.params['Knows'][know])
#            else:
#                print "{} not in {}".format(know, preset)

        for know in ['GravLessLevel1', 'GravLessLevel3']:
            if know in loader.params['Knows']:
                del loader.params['Knows'][know]

        newNames = {
            'SuitlessOuterMaridia' : 'GravLessLevel1',
            'SuitlessSandpit' : 'GravLessLevel3'
        }
        for oldKnow in newNames:
            if oldKnow in loader.params['Knows']:
                loader.params['Knows'][newNames[oldKnow]] = loader.params['Knows'][oldKnow]
                del loader.params['Knows'][oldKnow]

#        for know in ['SuitlessOuterMaridia', 'SuitlessSandpit', 'GravLessLevel1', 'GravLessLevel3']:
#            if know in loader.params['Knows']:
#                print "{} in {}: {}".format(know, preset, loader.params['Knows'][know])
#            else:
#                print "{} not in {}".format(know, preset)

        loader.dump(preset)

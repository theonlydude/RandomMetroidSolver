#!/usr/bin/python3

from utils.utils import PresetLoader
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

        loader.dump(preset)

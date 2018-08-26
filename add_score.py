#!/usr/bin/python

from utils import PresetLoader
import os

def loadPresetsList():
    return [os.path.join('standard_presets', f) for f in os.listdir('standard_presets') if f != 'solution.json'] + [os.path.join('community_presets', f) for f in os.listdir('community_presets')]

if __name__ == "__main__":
    presets = loadPresetsList()

    for preset in presets:
        print(preset)

        loader = PresetLoader.factory(preset)

        loader.dump(preset)

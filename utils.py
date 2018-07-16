#!/usr/bin/python

import os, json, random, sys
from parameters import Knows, Settings, Controller, isKnows, isSettings, isButton
from smbool import SMBool

# gauss random in [0, r] range
# the higher the slope, the less probable extreme values are
def randGaussBounds(r, slope=8):
    r = float(r)
    n = int(round(random.gauss(r/2, r/slope), 0))
    if n < 0:
        n = 0
    if n > r:
        n = int(r)
    return n

class PresetLoader(object):
    @staticmethod
    def factory(params):
        # can be a json, a python file or a dict with the parameters
        if type(params) is str:
            ext = os.path.splitext(params)
            if ext[1].lower() == '.json':
                return PresetLoaderJson(params)
            else:
                print("wrong parameters file type: {}".format(ext[1]))
                sys.exit(-1)
        elif type(params) is dict:
            return PresetLoaderDict(params)
        else:
            print("wrong parameters input, is neither a string nor a json file name: {}".format(params))
            sys.exit(-1)

    def __init__(self):
        if 'Knows' not in self.params:
            self.params['Knows'] = {}
        if 'Settings' not in self.params:
            self.params['Settings'] = {}
        if 'Controller' not in self.params:
            self.params['Controller'] = {}

    def load(self):
        # update the parameters in the parameters classes: Knows, Settings

        # Knows
        for param in self.params['Knows']:
            if isKnows(param) and hasattr(Knows, param):
                setattr(Knows, param, SMBool(self.params['Knows'][param][0],
                                             self.params['Knows'][param][1],
                                             ['{}'.format(param)]))
        # Settings
        ## hard rooms
        for hardRoom in ['X-Ray', 'Gauntlet']:
            if hardRoom in self.params['Settings']:
                Settings.hardRooms[hardRoom] = Settings.hardRoomsPresets[hardRoom][self.params['Settings'][hardRoom]]

        ## bosses
        for boss in ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain']:
            if boss in self.params['Settings']:
                Settings.bossesDifficulty[boss] = Settings.bossesDifficultyPresets[boss][self.params['Settings'][boss]]

        ## hellruns
        for hellRun in ['Ice', 'MainUpperNorfair', 'LowerNorfair']:
            if hellRun in self.params['Settings']:
                Settings.hellRuns[hellRun] = Settings.hellRunPresets[hellRun][self.params['Settings'][hellRun]]

        # Controller
        for button in self.params['Controller']:
            if isButton(button):
                setattr(Controller, button, self.params['Controller'][button])

    def dump(self, fileName):
        with open(fileName, 'w') as jsonFile:
            json.dump(self.params, jsonFile)

    def printToScreen(self):
        print("self.params: {}".format(self.params))

        print("loaded knows: ")
        for knows in Knows.__dict__:
            if isKnows(knows):
                print("{}: {}".format(knows, Knows.__dict__[knows]))
        print("loaded settings:")
        for setting in Settings.__dict__:
            if isSettings(setting):
                print("{}: {}".format(setting, Settings.__dict__[setting]))
        print("loaded controller:")
        for button in Controller.__dict__:
            if isButton(button):
                print("{}: {}".format(button, Controller.__dict__[button]))

class PresetLoaderJson(PresetLoader):
    # when called from the test suite
    def __init__(self, jsonFileName):
        with open(jsonFileName) as jsonFile:
            self.params = json.load(jsonFile)
        super(PresetLoaderJson, self).__init__()

class PresetLoaderDict(PresetLoader):
    # when called from the website
    def __init__(self, params):
        self.params = params
        super(PresetLoaderDict, self).__init__()

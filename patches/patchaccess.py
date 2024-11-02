import os, importlib
from logic.logic import Logic
from patches.common.patches import patches, additional_PLMs
from utils.parameters import appDir
from rom.addresses import Addresses

class PatchAccess(object):
    def __init__(self, baseDir = None):
        # load all ips patches
        self.patchesPath = {}
        self.symbolsDirs = []
        if baseDir is None:
            baseDir = appDir
        commonDir = os.path.join(baseDir, 'patches/common/ips/')
        self.symbolsDirs.append(os.path.join(baseDir, 'patches/common/sym/'))
        for patch in os.listdir(commonDir):
            self.patchesPath[patch] = commonDir
        logicDir = os.path.join(baseDir, 'patches/{}/ips/'.format(Logic.patches))
        self.symbolsDirs.append(os.path.join(baseDir, 'patches/{}/sym/'.format(Logic.patches)))
        for patch in os.listdir(logicDir):
            self.patchesPath[patch] = logicDir

        # load dict patches
        self.dictPatches = patches
        logicPatches = importlib.import_module("patches.{}.patches".format(Logic.patches)).patches
        self.dictPatches.update(logicPatches)

        # load additional PLMs
        self.additionalPLMs = additional_PLMs
        logicPLMs = importlib.import_module("patches.{}.patches".format(Logic.patches)).additional_PLMs
        self.additionalPLMs.update(logicPLMs)

    def getPatchPath(self, patch):
        # is patch preloaded
        if patch in self.patchesPath:
            return os.path.join(self.patchesPath[patch], patch)
        else:
            # patchs from varia_repository used by the customizer for permalinks
            if os.path.exists(patch):
                return patch
            else:
                raise Exception("unknown patch: {}".format(patch))

    def getDictPatches(self):
        return self.dictPatches

    def getAdditionalPLMs(self):
        return self.additionalPLMs

    def updateAdditionalPLMs(self, plms):
        self.additionalPLMs.update(plms)

    def postSymbolsLoad(self):
        # allow patches to have a label instead of an address
        replacements = {}
        for name, patches in self.dictPatches.items():
            for symbol, values in patches.items():
                if type(symbol) == str:
                    replacements[name] = [symbol, Addresses.getOne(symbol)]
        for name, replace in replacements.items():
            self.dictPatches[name][replace[1]] = self.dictPatches[name][replace[0]]
            del self.dictPatches[name][replace[0]]

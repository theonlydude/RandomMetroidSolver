#!/usr/bin/env python3
import sys, os

mainDir = os.path.dirname(sys.path[0])
sys.path.append(mainDir)

destFile = sys.argv[1]

from solver.standardSolver import StandardSolver
from patches.patchaccess import PatchAccess

class SolverArgs:
    def __init__(self, values):
        self._values = values

    def __getattr__(self, name):
        return self._values.get(name)

args = SolverArgs({
    "romFileName": "vanilla.sfc",
    "outputType": "rando",
    "pickupStrategy": "all",
    "presetFileName": 'standard_presets/regular.json',
    "runtimeLimit_s": 0,
    "itemsForbidden": []
})
solver = StandardSolver(args, baseDir=mainDir)
solver.solveRom()

with open(destFile, "w") as f:
    f.write("""
from rando.Items import ItemManager
from rando.ItemLocContainer import ItemLocation
from logic.logic import Logic

_locs = Logic.locationsDict()
vanillaItemLocations = [
""")
    for loc in solver.container.visitedLocations():
        if loc.Name == "Gunship":
            continue
        f.write(f"    ItemLocation(ItemManager.getItem('{loc.itemName}'), _locs['{loc.Name}']),\n")
    f.write("]\n")

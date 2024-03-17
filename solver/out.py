import sys, json, os
from solver.difficultyDisplayer import DifficultyDisplayer
from utils.objectives import Objectives
from utils.utils import fixEnergy

class Out:
    @staticmethod
    def factory(outputType, solver, outputFileName=None):
        if outputType == 'web':
            return OutWeb(solver, outputFileName)
        if outputType == 'console':
            return OutConsole(solver)
        if outputType == 'rando':
            return OutRando(solver)
        raise Exception("Wrong output type for the Solver: {}".format(outputType))

class OutWeb(Out):
    def __init__(self, solver, outputFileName):
        self.solver = solver
        self.outputFileName = outputFileName
        self.order = {
            'Kraid': 0,
            'Phantoon': 1,
            'Draygon': 2,
            'Ridley': 3,
            'SporeSpawn': 4,
            'Crocomire': 5,
            'Botwoon': 6,
            'GoldenTorizo': 7,
            'Varia': 8,
            'Gravity': 9,
            'Morph': 10,
            'Bomb': 11,
            'SpringBall': 12,
            'ScrewAttack': 13,
            'HiJump': 14,
            'SpaceJump': 15,
            'SpeedBooster': 16,
            'Charge': 17,
            'Ice': 18,
            'Wave': 19,
            'Spazer': 20,
            'Plasma': 21,
            'Grapple': 22,
            'XRayScope': 23,
            'CrystalFlash': 24,
            'ETank': 25,
            'Reserve': 26,
            'Missile': 27,
            'Super': 28,
            'PowerBomb': 29
        }
        self.key = lambda item: self.order[item[item.find('-')+1:]] if '-' in item else self.order[item]

    def out(self):
        s = self.solver
        if s.romConf.areaRando == True:
            dotFileName = os.path.basename(os.path.splitext(s.conf.romFileName)[0])+'.json'
            dotFileName = os.path.join(os.path.expanduser('~/web2py/applications/solver/static/graph'), dotFileName)
            s.areaGraph.toDot(dotFileName)
            (pngFileName, pngThumbFileName) = self.generatePng(dotFileName)
            if pngFileName is not None and pngThumbFileName is not None:
                pngFileName = os.path.basename(pngFileName)
                pngThumbFileName = os.path.basename(pngThumbFileName)
        else:
            pngFileName = None
            pngThumbFileName = None

        randomizedRom = os.path.basename(os.path.splitext(s.conf.romFileName)[0])+'.sfc'
        diffPercent = DifficultyDisplayer(s.difficulty).percent()
        generatedPath = self.getUnifiedPath(s.container)
        collectedItems = s.smbm.getItems()
        scavengerOrder = [loc.Name for loc in s.romConf.scavengerOrder]
        tourian = s.romConf.tourian

        if s.difficulty == -1:
            remainTry = self.getPath(s.tryRemainingLocs())
            remainMajors = self.getPath(s.getRemainMajors())
            remainMinors = self.getPath(s.getRemainMinors())
            skippedMajors = None
            unavailMajors = None
        else:
            remainTry = None
            remainMajors = None
            remainMinors = None
            skippedMajors = self.getPath(s.getSkippedMajors())
            unavailMajors = self.getPath(s.getUnavailMajors())

        result = dict(randomizedRom=randomizedRom, difficulty=s.difficulty,
                      generatedPath=generatedPath, diffPercent=diffPercent,
                      knowsUsed=(s.knowsUsed, s.knowsKnown), itemsOk=s.itemsOk,
                      patches=s.getPatchDescriptionsByGroup(),
                      pngFileName=pngFileName, pngThumbFileName=pngThumbFileName,
                      remainTry=remainTry, remainMajors=remainMajors, remainMinors=remainMinors,
                      skippedMajors=skippedMajors, unavailMajors=unavailMajors, collectedItems=collectedItems,
                      scavengerOrder=scavengerOrder, objectives=Objectives.getGoalsList(),
                      nbActiveGoals=Objectives.nbActiveGoals, nbRequiredGoals=Objectives.nbRequiredGoals,
                      tourian=tourian)

        with open(self.outputFileName, 'w') as jsonFile:
            json.dump(result, jsonFile)

    def getLoc(self, loc):
        if loc.locDifficulty is not None:
            # draygon fight is in it's path
            if loc.Name == 'Draygon':
                loc.locDifficulty = loc.pathDifficulty

            fixEnergy(loc.locDifficulty.items)
            fixEnergy(loc.pathDifficulty.items)

            return [
                (loc.Name, loc.Room), loc.Area, loc.SolveArea, loc.itemName,
                '{0:.2f}'.format(loc.locDifficulty.difficulty),
                sorted(loc.locDifficulty.knows),
                sorted(list(set(loc.locDifficulty.items)), key=self.key),
                '{0:.2f}'.format(loc.pathDifficulty.difficulty),
                sorted(loc.pathDifficulty.knows),
                sorted(list(set(loc.pathDifficulty.items)), key=self.key),
                [ap.Name for ap in loc.path] if loc.path is not None else None,
                loc.Class
            ]

        else:
            fixEnergy(loc.difficulty.items)

            return [
                (loc.Name, loc.Room), loc.Area, loc.SolveArea, loc.itemName,
                '{0:.2f}'.format(loc.difficulty.difficulty),
                sorted(loc.difficulty.knows),
                sorted(list(set(loc.difficulty.items)), key=self.key),
                '0.00', [], [],
                [ap.Name for ap in loc.path] if loc.path is not None else None,
                loc.Class
            ]

    def getUnifiedPath(self, container):
        out = []

        for step in container.steps:
            if container.isStepLocation(step):
                out.append(self.getLoc(step.location))
            else:
                if step.paths is not None:
                    for path in step.paths:
                        out.append([
                            None, None, None, None, None, None, None,
                            '{0:.2f}'.format(path.pdiff.difficulty),
                            sorted(path.pdiff.knows),
                            sorted(list(set(path.pdiff.items)), key=self.key),
                            [ap.Name for ap in path.path],
                            None
                        ])

                out.append(["Objective completed: {}".format(step.objectiveName), None, None, None,
                            None, None, None, None, None, None, None,
                            "objective"])

        return out

    def getPath(self, locations):
        if locations is None:
            return None
        return [self.getLoc(loc) for loc in locations]

    def generatePng(self, dotFileName):
        # use dot to generate the graph's image .png
        # use convert to generate the thumbnail
        # dotFileName: the /directory/image.dot
        # the png and thumbnails are generated in the same directory as the dot
        # requires that graphviz is installed
        import subprocess

        splited = os.path.splitext(dotFileName)
        pngFileName = splited[0] + '.png'
        pngThumbFileName = splited[0] + '_thumbnail.png'

        # dot -Tpng VARIA_Randomizer_AFX5399_noob.dot -oVARIA_Randomizer_AFX5399_noob.png
        params = ['dot', '-Tpng', dotFileName, '-o'+pngFileName]
        ret = subprocess.call(params)
        if ret != 0:
            print("Error calling dot {}: {}".format(params, ret))
            return (None, None)

        params = ['convert', pngFileName, '-resize', '1024', pngThumbFileName]
        ret = subprocess.call(params)
        if ret != 0:
            print("Error calling convert {}: {}".format(params, ret))
            os.remove(pngFileName)
            return (None, None)

        return (pngFileName, pngThumbFileName)

class OutConsole(Out):
    def __init__(self, solver):
        self.solver = solver

    def out(self):
        s = self.solver
        self.displayOutput()

        print("({}, {}): diff : {}".format(round(float(s.difficulty), 3), s.itemsOk, s.conf.romFileName))
        print("{}/{}: knows Used : {}".format(s.knowsUsed, s.knowsKnown, s.conf.romFileName))

        if s.difficulty >= 0:
            sys.exit(0)
        else:
            sys.exit(1)

    def printPathHead(self, message):
        print("")
        print(message)
        print('{} {:>48} {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'.format("Z", "Location Name", "Area", "Sub Area", "Distance", "Item", "Difficulty", "Knows used", "Items used"))
        print('-'*150)

    def printLocation(self, loc, displayAPs):
        if displayAPs == True and loc.path is not None:
            path = [ap.Name for ap in loc.path]
            if len(path) > 1:
                path = " -> ".join(path)
                pathDiff = loc.pathDifficulty
                print('{}: {} {} {} {}'.format('Path', path, round(float(pathDiff.difficulty), 2), sorted(pathDiff.knows), sorted(list(set(pathDiff.items)))))
        line = '{} {:>48}: {:>12} {:>34} {:>8} {:>16} {:>14} {} {}'

        if loc.locDifficulty is not None:
            fixEnergy(loc.locDifficulty.items)

            print(line.format('Z' if loc.isChozo() else ' ',
                              loc.Name,
                              loc.Area,
                              loc.SolveArea,
                              loc.distance if loc.distance is not None else 'nc',
                              loc.itemName,
                              round(float(loc.locDifficulty.difficulty), 2) if loc.locDifficulty is not None else 'nc',
                              sorted(loc.locDifficulty.knows) if loc.locDifficulty is not None else 'nc',
                              sorted(list(set(loc.locDifficulty.items))) if loc.locDifficulty is not None else 'nc'))
        elif loc.difficulty is not None:
            fixEnergy(loc.difficulty.items)

            print(line.format('Z' if loc.isChozo() else ' ',
                              loc.Name,
                              loc.Area,
                              loc.SolveArea,
                              loc.distance if loc.distance is not None else 'nc',
                              loc.itemName,
                              round(float(loc.difficulty.difficulty), 2),
                              sorted(loc.difficulty.knows),
                              sorted(list(set(loc.difficulty.items)))))
        else:
            print(line.format('Z' if loc.isChozo() else ' ',
                              loc.Name,
                              loc.Area,
                              loc.SolveArea,
                              loc.distance if loc.distance is not None else 'nc',
                              loc.itemName,
                              'nc',
                              'nc',
                              'nc'))


    def printUnifiedPath(self, message, container):
        self.printPathHead(message)
        for step in container.steps:
            if container.isStepLocation(step):
                self.printLocation(step.location, displayAPs=True)
            else:
                if step.paths is not None:
                    for path in step.paths:
                        display_path = " -> ".join([ap.Name for ap in path.path])
                        print('{}: {} {} {} {}'.format('Path', display_path, round(float(path.pdiff.difficulty), 2), sorted(path.pdiff.knows), sorted(list(set(path.pdiff.items)))))
                print(" Objective completed: {} ".format(step.objectiveName).center(160, '='))

    def printPath(self, message, locations, displayAPs=True):
        self.printPathHead(message)
        for loc in locations:
            self.printLocation(loc, displayAPs)

    def displayOutput(self):
        s = self.solver

        print("all patches: {}".format(s.romLoader.getAllPatches()))
        print("objectives: {}".format(Objectives.getGoalsList()))
        print("objectives required: {}/{}".format(Objectives.nbRequiredGoals, Objectives.nbActiveGoals))
        print("tourian: {}".format(s.romConf.tourian))

        # print generated path
        if s.conf.displayGeneratedPath == True:
            self.printUnifiedPath("Generated path:", s.container)

            # if we've aborted, display missing techniques and remaining locations
            if s.difficulty == -1:
                self.printPath("Next locs which could have been available if more techniques were known:", s.tryRemainingLocs(), displayAPs=True)

                remainMajors = s.getRemainMajors()
                if remainMajors:
                    self.printPath("Remaining major locations:", remainMajors, displayAPs=False)

                remainMinors = s.getRemainMinors()
                if remainMinors:
                    self.printPath("Remaining minor locations:", remainMinors, displayAPs=False)

            else:
                # if some locs are not picked up display those which are available
                # and those which are not
                skippedMajors = s.getSkippedMajors()
                if skippedMajors:
                    self.printPath("Skipped major locations:", skippedMajors, displayAPs=False)
                else:
                    print("No skipped major locations")

                unavailMajors = s.getUnavailMajors()
                if unavailMajors:
                    self.printPath("Unaccessible major locations:", unavailMajors, displayAPs=False)
                else:
                    print("No unaccessible major locations")

            items = s.smbm.getItems()
            print("ETank: {}, Reserve: {}, Missile: {}, Super: {}, PowerBomb: {}".format(items['ETank'], items['Reserve'], items['Missile'], items['Super'], items['PowerBomb']))
            print("Majors: {}".format(sorted([item for item in items if items[item] == 1])))

        # display difficulty scale
        self.displayDifficulty(s.difficulty)

    def displayDifficulty(self, difficulty):
        if difficulty >= 0:
            text = DifficultyDisplayer(difficulty).scale()
            print("Estimated difficulty: {}".format(text))
        else:
            print("Aborted run, can't finish the game with the given prerequisites")

class OutRando(OutConsole):
    def __init__(self, solver):
        self.solver = solver

    def out(self):
        pass

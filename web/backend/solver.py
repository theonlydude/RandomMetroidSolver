import os, json, tempfile, subprocess
from datetime import datetime

from web.backend.utils import getAddressesToRead, loadPresetsList, generateJsonROM
from utils.parameters import Knows, diff2text, text2diff, diff4solver
from utils.parameters import easy, medium, hard, harder, hardcore, mania
from utils.utils import getPresetDir, getPythonExec
from utils.db import DB
from solver.conf import Conf
from logic.logic import Logic
from patches.patchaccess import PatchAccess
from rom.symbols import Symbols
from utils.doorsmanager import DoorsManager
from rom.addresses import Addresses

from gluon.validators import IS_ALPHANUMERIC, IS_LENGTH, IS_MATCH
from gluon.http import redirect
from gluon.html import URL

class Solver(object):
    def __init__(self, session, request, cache):
        self.session = session
        self.request = request
        self.cache = cache
        # required for symbols
        Logic.factory('vanilla') # TODO will have to be changed when handling mirror/rotation etc
        self.vars = self.request.vars

    def run(self):
        # init session
        self.initSolverSession()

        if self.vars.action == 'Solve':
            (ok, msg) = self.validateSolverParams()
            if not ok:
                self.session.flash = msg
                redirect(URL(r=self.request, f='solver'))

            self.updateSolverSession()

            preset = self.vars.preset

            # new uploaded rom ?
            error = False
            if self.vars.romJson != '':
                try:
                    (base, jsonRomFileName) = generateJsonROM(self.vars.romJson)
                    self.session.solver['romFile'] = base
                    if base not in self.session.solver['romFiles']:
                        self.session.solver['romFiles'].append(base)
                except Exception as e:
                    print("Error loading the ROM file, exception: {}".format(e))
                    self.session.flash = "Error loading the json ROM file"
                    error = True

            elif self.vars['romFile'] is not None and len(self.vars['romFile']) != 0:
                self.session.solver['romFile'] = os.path.splitext(self.vars['romFile'])[0]
                jsonRomFileName = 'roms/' + self.session.solver['romFile'] + '.json'
            else:
                self.session.flash = "No rom file selected for upload"
                error = True

            if not error:
                # check that the json file exists
                if not os.path.isfile(jsonRomFileName):
                    self.session.flash = "Missing json ROM file on the server"
                else:
                    try:
                        (ok, result) = self.computeDifficulty(jsonRomFileName, preset)
                        if not ok:
                            self.session.flash = result
                            redirect(URL(r=self.request, f='solver'))
                        self.session.solver['result'] = result
                    except Exception as e:
                        print("Error loading the ROM file, exception: {}".format(e))
                        self.session.flash = "Error loading the ROM file"

            redirect(URL(r=self.request, f='solver'))

        # display result
        result = self.prepareResult()

        ROMs = self.getROMsList()

        # last solved ROM
        lastRomFile = self.getLastSolvedROM()

        # load presets list
        (stdPresets, tourPresets, comPresets) = loadPresetsList(self.cache)

        # generate list of addresses to read in the ROM
        symbols = Symbols(PatchAccess())
        symbols.loadAllSymbols()
        Addresses.updateFromSymbols(symbols)
        DoorsManager.setDoorsAddress(symbols)
        addresses = getAddressesToRead()

        # send values to view
        return dict(desc=Knows.desc, stdPresets=stdPresets, tourPresets=tourPresets, comPresets=comPresets, roms=ROMs,
                    lastRomFile=lastRomFile, difficulties=diff2text, categories=Knows.categories,
                    result=result, addresses=addresses,
                    easy=easy, medium=medium, hard=hard, harder=harder, hardcore=hardcore, mania=mania)

    def initSolverSession(self):
        if self.session.solver is None:
            self.session.solver = {
                'preset': 'regular',
                'difficultyTarget': Conf.difficultyTarget,
                'pickupStrategy': Conf.itemsPickup,
                'itemsForbidden': [],
                'romFiles': [],
                'romFile': None,
                'result': None,
                'complexity': 'simple'
            }

    def updateSolverSession(self):
        if self.session.solver is None:
           self.initSolverSession()

        self.session.solver['preset'] = self.vars.preset
        self.session.solver['difficultyTarget'] = text2diff[self.vars.difficultyTarget]
        self.session.solver['pickupStrategy'] = self.vars.pickupStrategy
        self.session.solver['complexity'] = self.vars.complexity

        itemsForbidden = []
        for item in ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
            boolvar = self.vars[item+"_bool"]
            if boolvar is not None:
                itemsForbidden.append(item)

        self.session.solver['itemsForbidden'] = itemsForbidden

    def getROMsList(self):
        return ['{}.sfc'.format(base) for base in self.session.solver['romFiles']]

    def getLastSolvedROM(self):
        return '{}.sfc'.format(self.session.solver['romFile']) if self.session.solver['romFile'] is not None else None

    def genPathTable(self, locations, scavengerOrder, displayAPs=True):
        if locations is None or len(locations) == 0:
            return None

        lastAP = None
        pathTable = """
    <table class="full">
      <colgroup>
        <col class="locName" /><col class="area" /><col class="subarea" /><col class="item" /><col class="difficulty" /><col class="knowsUsed" /><col class="itemsUsed" />
      </colgroup>
      <tr>
        <th>Location Name</th><th>Area</th><th>SubArea</th><th>Item</th><th>Difficulty</th><th>Techniques used</th><th>Items used</th>
      </tr>
    """

        currentSuit = 'Power'
        for location, area, subarea, item, locDiff, locTechniques, locItems, pathDiff, pathTechniques, pathItems, path, _class in locations:
            if _class == "objective":
                pathTable += """<tr><td colspan="7" class="center objective">{}</td></tr>""".format(location)
                continue

            if path is not None:
                lastAP = path[-1]
                if displayAPs == True and not (len(path) == 1 and path[0] == lastAP):
                    pathTable += """<tr class="grey"><td colspan="3">{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n""".format(" -&gt; ".join(path), """<img alt="samus" class="imageItem" src="/solver/static/images/solver/samus_run_{}.gif" title="samus" />""".format(currentSuit), self.getDiffImg(pathDiff), self.getTechniques(pathTechniques), self.getItems(pathItems))

            (name, room) = location

            # not picked up items start with an '-'
            if item[0] != '-':
                pathTable += """
    <tr class="{}">
      <td>{}</td>
      <td>{}</td>
      <td>{}</td>
      <td>{}</td>
      <td>{}</td>
      <td>{}</td>
      <td>{}</td>
    </tr>
    """.format(item, self.getRoomLink(name, room), self.getAreaLink(area), self.getSubArea(subarea),
               self.getItemImg(item, location=name, scavengerOrder=scavengerOrder, boss="Boss" in _class),
               self.getDiffImg(locDiff),
               self.getTechniques(locTechniques),
               self.getItems(locItems))

                if item == 'Varia' and currentSuit == 'Power':
                    currentSuit = 'Varia'
                elif item == 'Gravity':
                    currentSuit = 'Gravity'

        pathTable += "</table>"

        return pathTable

    def getItems(self, items):
        ret = ""
        for item in items:
            if item[0] >= '0' and item[0] <= '9':
                # for etanks and reserves
                count = item[:item.find('-')]
                item = item[item.find('-')+1:]
                ret += "<span>{}-{}</span>".format(count, self.getItemImg(item, small=True))
            else:
                ret += self.getItemImg(item, small=True)
        return ret

    def getTechniques(self, techniques):
        ret = ""
        for tech in techniques:
            if tech in Knows.desc and Knows.desc[tech]['href'] != None:
                ret += """ <a class="marginKnows" href="{}" target="_blank">{}</a>""".format(Knows.desc[tech]['href'], tech)
            else:
                ret += """ {}""".format(tech)
        return ret

    def getRoomLink(self, name, room):
        roomUrl = room.replace(' ', '_').replace("'", '%27')
        roomImg = room.replace(' ', '').replace('-', '').replace("'", '')
        return """<a target="_blank" href="https://wiki.supermetroid.run/{}" data-thumbnail-src="/solver/static/images/rooms/{}.png" class="room">{}</a>""".format(roomUrl, roomImg, name)

    def getAreaLink(self, name):
        if name == "WreckedShip":
            url = "Wrecked_Ship"
        elif name == "LowerNorfair":
            url = "Norfair"
        else:
            url = name

        return """<a target="_blank" href="https://metroid.fandom.com/wiki/{}" class="area">{}</a>""".format(url, name)

    def getSubArea(self, subarea):
        img = subarea.replace(' ', '')
        if img in ["Kraid", "Tourian"]:
            # kraid is already the image for kraid boss
            img += "SubArea"
        return """<span data-thumbnail-src="/solver/static/images/rooms/{}.png" class="subarea">{}</span>""".format(img, subarea)

    def getItemImg(self, item, location=None, scavengerOrder=[], small=False, boss=False):
        if boss:
            _class = "imageBoss"
        elif small == True:
            _class = "imageItems"
        else:
            _class = "imageItem"
        itemImg = """<img alt="{}" class="{}" src="/solver/static/images/tracker/inventory/{}.png" title="{}" />""".format(item, _class, item.replace(' ', ''), item)

        if location is not None and len(scavengerOrder) > 0 and location in scavengerOrder:
            index = scavengerOrder.index(location) + 1
            if index >= 10:
                itemImg += """<img class="imageItems" src="/solver/static/images/tracker/inventory/1.png"/>"""
            index %= 10
            itemImg += """<img class="imageItems" src="/solver/static/images/tracker/inventory/{}.png"/>""".format(index)
        return itemImg

    def getDiffImg(self, diff):
        diffId, diffName = diff4solver(float(diff))

        return """<img alt="{}" class="imageItem" src="/solver/static/images/solver/marker_{}.png" title="{}" />""".format(diffName, diffId, diffName)

    def genCollectedItems(self, locations):
        items = set()
        for _, _, _, item, _, _, _, _, _, _, _, _ in locations:
            items.add(item)
        return items

    def prepareResult(self):
        if self.session.solver['result'] is not None:
            result = self.session.solver['result']

            if result['difficulty'] == -1:
                result['resultText'] = "The ROM \"{}\" is not finishable with the known techniques".format(result['randomizedRom'])
            else:
                if result['itemsOk'] is False:
                    result['resultText'] = "The ROM \"{}\" is finishable but not all the requested items can be picked up with the known techniques. Estimated difficulty is: ".format(result['randomizedRom'])
                else:
                    result['resultText'] = "The ROM \"{}\" estimated difficulty is: ".format(result['randomizedRom'])

            # add generated path (spoiler !)
            result['pathTable'] = self.genPathTable(result['generatedPath'], result['scavengerOrder'])
            result['pathremainTry'] = self.genPathTable(result['remainTry'], result['scavengerOrder'])
            result['pathremainMajors'] = self.genPathTable(result['remainMajors'], result['scavengerOrder'], False)
            result['pathremainMinors'] = self.genPathTable(result['remainMinors'], result['scavengerOrder'], False)
            result['pathskippedMajors'] = self.genPathTable(result['skippedMajors'], result['scavengerOrder'], False)
            result['pathunavailMajors'] = self.genPathTable(result['unavailMajors'], result['scavengerOrder'], False)
            result['collectedItems'] = self.genCollectedItems(result['generatedPath'])

            # display the result only once
            self.session.solver['result'] = None
        else:
            result = None

        return result

    def validateSolverParams(self):
        for param in ['difficultyTarget', 'pickupStrategy', 'complexity']:
            if self.vars[param] is None:
                return (False, "Missing parameter {}".format(param))

        if self.vars.preset == None:
            return (False, "Missing parameter preset")
        preset = self.vars.preset

        if IS_ALPHANUMERIC()(preset)[1] is not None:
            return (False, "Wrong value for preset, must be alphanumeric")

        if IS_LENGTH(maxsize=32, minsize=1)(preset)[1] is not None:
            return (False, "Wrong length for preset, name must be between 1 and 32 characters")

        # check that preset exists
        fullPath = '{}/{}.json'.format(getPresetDir(preset), preset)
        if not os.path.isfile(fullPath):
            return (False, "Unknown preset: {}".format(preset))

        difficultyTargetChoices = ["easy", "medium", "hard", "very hard", "hardcore", "mania"]
        if self.vars.difficultyTarget not in difficultyTargetChoices:
            return (False, "Wrong value for difficultyTarget: {}, authorized values: {}".format(self.vars.difficultyTarget, difficultyTargetChoices))

        pickupStrategyChoices = ["all", "any"]
        if self.vars.pickupStrategy not in pickupStrategyChoices:
            return (False, "Wrong value for pickupStrategy: {}, authorized values: {}".format(self.vars.pickupStrategy, pickupStrategyChoice))

        complexityChoices = ["simple", "advanced"]
        if self.vars.complexity not in complexityChoices:
            return (False, "Wrong value for complexity: {}, authorized values: {}".format(self.vars.complexity, complexityChoices))

        itemsForbidden = []
        for item in ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
            boolvar = self.vars[item+"_bool"]
            if boolvar is not None:
                if boolvar != 'on':
                    return (False, "Wrong value for {}: {}, authorized values: on/off".format(item, boolvar))

        if self.vars.romJson is None and self.vars.uploadFile is None and self.vars.romFile is None:
            return (False, "Missing ROM to solve")

        if self.vars.romFile is not None:
            if IS_LENGTH(maxsize=255, minsize=1)(self.vars.romFile)[1] is not None:
                return (False, "Wrong length for romFile, name must be between 1 and 256 characters: {}".format(request.vars.romFile))

        if self.vars.romJson is not None and len(self.vars.romJson) > 0:
            try:
                json.loads(self.vars.romJson)
            except:
                return (False, "Wrong value for romJson, must be a JSON string: [{}]".format(self.vars.romJson))

        if self.vars.uploadFile is not None:
            if type(self.vars.uploadFile) == str:
                if IS_MATCH('[a-zA-Z0-9_\.() ,\-]*', strict=True)(request.vars.uploadFile)[1] is not None:
                    return (False, "Wrong value for uploadFile, must be a valid file name: {}".format(self.vars.uploadFile))

                if IS_LENGTH(maxsize=256, minsize=1)(self.vars.uploadFile)[1] is not None:
                    return (False, "Wrong length for uploadFile, name must be between 1 and 255 characters")

        return (True, None)

    def computeDifficulty(self, jsonRomFileName, preset):
        randomizedRom = os.path.basename(jsonRomFileName.replace('json', 'sfc'))

        presetFileName = "{}/{}.json".format(getPresetDir(preset), preset)
        (fd, jsonFileName) = tempfile.mkstemp()

        db = DB()
        id = db.initSolver()

        params = [
            getPythonExec(),  os.path.expanduser("~/RandomMetroidSolver/solver.py"),
            '-r', str(jsonRomFileName),
            '--preset', presetFileName,
            '--difficultyTarget', str(self.session.solver['difficultyTarget']),
            '--pickupStrategy', self.session.solver['pickupStrategy'],
            '--type', 'web',
            '--output', jsonFileName,
            '--runtime', '10'
        ]

        for item in self.session.solver['itemsForbidden']:
            params += ['--itemsForbidden', item]

        db.addSolverParams(id, randomizedRom, preset, self.session.solver['difficultyTarget'],
                           self.session.solver['pickupStrategy'], self.session.solver['itemsForbidden'])

        print("before calling solver: {}".format(params))
        start = datetime.now()
        ret = subprocess.call(params)
        end = datetime.now()
        duration = (end - start).total_seconds()
        print("ret: {}, duration: {}s".format(ret, duration))

        if ret == 0:
            with open(jsonFileName) as jsonFile:
                result = json.load(jsonFile)
        else:
            result = "Solver: something wrong happened while solving the ROM"

        db.addSolverResult(id, ret, duration, result)
        db.close()

        os.close(fd)
        os.remove(jsonFileName)

        return (ret == 0, result)

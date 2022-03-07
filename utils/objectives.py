import random
from rom.rom import snes_to_pc
from logic.helpers import Bosses
from logic.smbool import SMBool
import utils.log, logging

LOG = utils.log.get('Objectives')

class Synonyms(object):
    killSynonyms = [
        "defeat",
        "massacre",
        "slaughter",
        "slay",
        "wipe out",
        "eradicate",
        "erase",
        "finish",
        "destroy",
        "wreck",
        "smash",
        "crush",
        "end",
        "eliminate",
        "terminate"
    ]
    alreadyUsed = []
    @staticmethod
    def getVerb(): 
        verb = random.choice(Synonyms.killSynonyms)
        while verb in Synonyms.alreadyUsed:
            verb = random.choice(Synonyms.killSynonyms)
        Synonyms.alreadyUsed.append(verb)
        return verb

class Goal(object):
    def __init__(self, name, available, gtype, clearFunc, checkAddr, exclusion, items, text, useSynonym, expandable, expandableList=[]):
        self.name = name
        self.available = available
        self.clearFunc = clearFunc
        # in bank $82, see objectives_pause.asm
        self.checkAddr = checkAddr
        self.rank = -1
        # possible values:
        #  - boss
        #  - miniboss
        #  - other
        self.gtype = gtype
        # example for kill three g4
        # {
        #  "list": [list of objectives],
        #  "type: "boss",
        #  "limit": 2
        # }
        self.exclusion = exclusion
        self.items = items
        self.text = text
        self.useSynonym = useSynonym
        self.expandable = expandable
        self.expandableList = expandableList

    def setRank(self, rank):
        self.rank = rank

    def canClearGoal(self, smbm):
        return self.clearFunc(smbm)

    def getText(self):
        out = "{}. ".format(self.rank)
        if self.useSynonym:
            out += self.text.format(Synonyms.getVerb())
        else:
            out += self.text
        assert len(out) <= 28, "Goal text '{}' is too long: {}, max 28".format(out, len(out))
        return out

class Objectives(object):
    objectivesList = snes_to_pc(0x82f983)
    activeGoals = []
    nbActiveGoals = 0
    maxActiveGoals = 5
    tourianRequired = True
    goals = {
        "kill kraid": Goal("kill kraid", True, "boss", lambda sm: Bosses.bossDead(sm, 'Kraid'), 0xF98F,
                           {"list": ["kill all G4", "kill one G4"]}, ["Kraid"], "{} kraid", True, False),
        "kill phantoon": Goal("kill phantoon", True, "boss", lambda sm: Bosses.bossDead(sm, 'Phantoon'), 0xF997,
                              {"list": ["kill all G4", "kill one G4"]}, ["Phantoon"], "{} phantoon", True, False),
        "kill draygon": Goal("kill draygon", True, "boss", lambda sm: Bosses.bossDead(sm, 'Draygon'), 0xF99F,
                             {"list": ["kill all G4", "kill one G4"]}, ["Draygon"], "{} draygon", True, False),
        "kill ridley": Goal("kill ridley", True, "boss", lambda sm: Bosses.bossDead(sm, 'Ridley'), 0xF9A7,
                            {"list": ["kill all G4", "kill one G4"]}, ["Ridley"], "{} ridley", True, False),
        "kill one G4": Goal("kill one G4", True, "other", lambda sm: Bosses.xBossesDead(sm, 1), 0xFA54,
                            {"list": ["kill kraid", "kill phantoon", "kill draygon", "kill ridley",
                                      "kill all G4", "kill two G4", "kill three G4"]},
                            ["Kraid", "Phantoon", "Draygon", "Ridley"], "{} one golden4", True, False),
        "kill two G4": Goal("kill two G4", True, "other", lambda sm: Bosses.xBossesDead(sm, 2), 0xFA5D,
                            {"list": ["kill all G4", "kill one G4", "kill three G4"],
                             "type": "boss",
                             "limit": 1},
                            ["Kraid", "Phantoon", "Draygon", "Ridley"], "{} two golden4", True, False),
        "kill three G4": Goal("kill three G4", True, "other", lambda sm: Bosses.xBossesDead(sm, 3), 0xFA66,
                              {"list": ["kill all G4", "kill one G4", "kill two G4"],
                               "type": "boss",
                               "limit": 2},
                              ["Kraid", "Phantoon", "Draygon", "Ridley"], "{} three golden4", True, False),
        "kill all G4": Goal("kill all G4", True, "other", lambda sm: Bosses.allBossesDead(sm), 0xF9AF,
                            {"list": ["kill kraid", "kill phantoon", "kill draygon", "kill ridley", "kill one G4", "kill two G4", "kill three G4"]},
                            ["Kraid", "Phantoon", "Draygon", "Ridley"],
                            "{} all golden4", True, True, ["kill kraid", "kill phantoon", "kill draygon", "kill ridley"]),
        "kill spore spawn": Goal("kill spore spawn", True, "miniboss", lambda sm: Bosses.bossDead(sm, 'SporeSpawn'), 0xF9C5,
                                 {"list": ["kill all mini bosses", "kill one miniboss"]}, ["SporeSpawn"], "{} spore spawn", True, False),
        "kill botwoon": Goal("kill botwoon", True, "miniboss", lambda sm: Bosses.bossDead(sm, 'Botwoon'), 0xF9CD,
                             {"list": ["kill all mini bosses", "kill one miniboss"]}, ["Botwoon"], "{} botwoon", True, False),
        "kill crocomire": Goal("kill crocomire", True, "miniboss", lambda sm: Bosses.bossDead(sm, 'Crocomire'), 0xF9D5,
                               {"list": ["kill all mini bosses", "kill one miniboss"]}, ["Crocomire"], "{} crocomire", True, False),
        "kill golden torizo": Goal("kill golden torizo", True, "miniboss", lambda sm: Bosses.bossDead(sm, 'GoldenTorizo'), 0xF9DD,
                                   {"list": ["kill all mini bosses", "kill one miniboss"]}, ["GoldenTorizo"], "{} golden torizo", True, False),
        "kill one miniboss": Goal("kill one miniboss", True, "other", lambda sm: Bosses.xMiniBossesDead(sm, 1), 0xFA6F,
                                  {"list": ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo",
                                            "kill all mini bosses", "kill two minibosses", "kill three minibosses"]},
                                  ["SporeSpawn", "Botwoon", "Crocomire", "GoldenTorizo"], "{} one miniboss", True, False),
        "kill two minibosses": Goal("kill two minibosses", True, "other", lambda sm: Bosses.xMiniBossesDead(sm, 2), 0xFA78,
                                    {"list": ["kill all mini bosses", "kill one miniboss", "kill three minibosses"],
                                     "type": "miniboss",
                                     "limit": 1},
                                    ["SporeSpawn", "Botwoon", "Crocomire", "GoldenTorizo"], "{} two minibosses", True, False),
        "kill three minibosses": Goal("kill three minibosses", True, "other", lambda sm: Bosses.xMiniBossesDead(sm, 3), 0xFA81,
                                      {"list": ["kill all mini bosses", "kill one miniboss", "kill two minibosses"],
                                       "type": "miniboss",
                                       "limit": 2},
                                      ["SporeSpawn", "Botwoon", "Crocomire", "GoldenTorizo"], "{} three minibosses", True, False),
        "kill all mini bosses": Goal("kill all mini bosses", True, "other", lambda sm: Bosses.allMiniBossesDead(sm), 0xF9E5,
                                     {"list": ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo",
                                               "kill one miniboss", "kill two minibosses", "kill three minibosses"]},
                                     ["SporeSpawn", "Botwoon", "Crocomire", "GoldenTorizo"],
                                     "{} all mini bosses", True, True, ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo"]),
        "shaktool cleared path": Goal("shaktool cleared path", False, "other", None, 0xFAFB,
                                      {"list": []}, [], "shaktool cleared its path", False, False),
        "finish scavenger hunt": Goal("finish scavenger hunt", False, "other", lambda sm: SMBool(True), 0xFA03,
                                      {"list": []}, [], "finish scavenger hunt", False, False),
        "nothing": Goal("nothing", True, "other", lambda sm: SMBool(True), 0xFA1A,
                        {"list": ["kill kraid", "kill phantoon", "kill draygon", "kill ridley", "kill all G4",
                                  "kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo", "kill all mini bosses",
                                  "shaktool cleared path", "finish scavenger hunt",
                                  "kill one G4", "kill two G4", "kill three G4",
                                  "kill one miniboss", "kill two minibosses", "kill three minibosses"]},
                        [], "nothing", False, False),
    }

    def resetGoals(self):
        Objectives.activeGoals = []
        Objectives.nbActiveGoals = 0

    def conflict(self, newGoal):
        LOG.debug("check if new goal {} conflicts with existing active goals".format(newGoal.name))
        count = 0
        for goal in Objectives.activeGoals:
            if newGoal.name in goal.exclusion["list"]:
                LOG.debug("new goal {} in exclusion list of active goal {}".format(newGoal.name, goal.name))
                return True
            # count bosses/minibosses already active if new goal has a limit
            if newGoal.exclusion.get("type") == goal.gtype:
                count += 1
                LOG.debug("new goal limit type: {} same as active goal {}. count: {}".format(newGoal.exclusion["type"], goal.name, count))
        if count > newGoal.exclusion.get("limit", 0):
            LOG.debug("new goal {} limit {} is lower than active goals of type: {}".format(newGoal.name, newGoal.exclusion["limit"], newGoal.exclusion["type"]))
            return True
        LOG.debug("no direct conflict detected for new goal {}".format(newGoal.name))

        # if at least one active goal has a limit and new goal has the same type of one of the existing limit
        # check that new goal doesn't exceed the limit
        for goal in Objectives.activeGoals:
            goalExclusionType = goal.exclusion.get("type")
            if goalExclusionType is not None and goalExclusionType == newGoal.gtype:
                count = 0
                for lgoal in Objectives.activeGoals:
                    if lgoal.gtype == newGoal.gtype:
                        count += 1
                # add new goal to the count
                if count >= goal.exclusion["limit"]:
                    LOG.debug("new Goal {} would excess limit {} of active goal {}".format(newGoal.name, goal.exclusion["limit"], goal.name))
                    return True

        LOG.debug("no backward conflict detected for new goal {}".format(newGoal.name))

        return False

    def addGoal(self, goalName):
        LOG.debug("addGoal: {}".format(goalName))
        goal = Objectives.goals[goalName]
        if self.conflict(goal):
            return
        Objectives.nbActiveGoals += 1
        assert Objectives.nbActiveGoals <= Objectives.maxActiveGoals, "Too many active goals"
        goal.setRank(Objectives.nbActiveGoals)
        Objectives.activeGoals.append(goal)

    def removeGoal(self, goal):
        Objectives.nbActiveGoals -= 1
        Objectives.activeGoals.remove(goal)

    def setVanilla(self):
        self.addGoal("kill kraid")
        self.addGoal("kill phantoon")
        self.addGoal("kill draygon")
        self.addGoal("kill ridley")

    def setScavengerHunt(self, triggerEscape):
        if triggerEscape:
            LOG.debug("triggerEscape: {}, tourian not required")
            Objectives.tourianRequired = False

        self.addGoal("finish scavenger hunt")

    def setScavengerHuntFunc(self, scavClearFunc):
        Objectives.goals["finish scavenger hunt"].clearFunc = scavClearFunc

    def expandGoals(self):
        # try to replace 'kill all G4' with the four associated objectives.
        # we need at least 3 empty objectives out of the max (-1 +4)
        if Objectives.maxActiveGoals - Objectives.nbActiveGoals < 3:
            return

        expandable = None
        for goal in Objectives.activeGoals:
            if goal.expandable:
                expandable = goal
                break

        if expandable is None:
            return

        LOG.debug("replace {} with {}".format(expandable.name, expandable.expandableList))
        self.removeGoal(expandable)
        for name in expandable.expandableList:
            self.addGoal(name)

        # rebuild ranks
        for i, goal in enumerate(Objectives.activeGoals, 1):
            goal.rank = i

    # call from logic
    @staticmethod
    def canClearGoals(smbm):
        result = SMBool(True)
        for goal in Objectives.activeGoals:
            result = smbm.wand(result, goal.canClearGoal(smbm))
        return result

    def getGoalFromCheckFunction(self, checkFunction):
        for name, goal in Objectives.goals.items():
            if goal.checkAddr == checkFunction:
                return goal
        assert True, "Goal with check function {} not found".format(hex(checkFunction))

    # call from web
    @staticmethod
    def getAddressesToRead():
        terminator = 1
        objectiveSize = 2
        bytesToRead = (Objectives.maxActiveGoals + terminator) * objectiveSize
        return [Objectives.objectivesList+i for i in range(0, bytesToRead+1)]

    @staticmethod
    def getExclusions():
        # to compute exclusions in the front end
        return {goalName: goal.exclusion for goalName, goal in Objectives.goals.items()}

    @staticmethod
    def getObjectivesTypes():
        # to compute exclusions in the front end
        types = {'boss': [], 'miniboss': []}
        for goalName, goal in Objectives.goals.items():
            if goal.gtype in types:
                types[goal.gtype].append(goalName)
        return types

    @staticmethod
    def getObjectivesSort():
        return list(Objectives.goals.keys())

    # call from rando check pool and solver
    @staticmethod
    def getMandatoryBosses():
        r = [goal.items for goal in Objectives.activeGoals]
        return [item for items in r for item in items]

    # call from solver
    @staticmethod
    def getGoalsList():
        return [goal.name for goal in Objectives.activeGoals]

    # call from rando
    @staticmethod
    def getAllGoals(removeNothing=False):
        return [goal.name for goal in Objectives.goals.values() if goal.available and (not removeNothing or goal.name != "nothing")]

    # call from rando
    def setRandom(self, nbGoals, availableGoals):
        while Objectives.nbActiveGoals < nbGoals and availableGoals:
            goalName = random.choice(availableGoals)
            self.addGoal(goalName)
            availableGoals.remove(goalName)

    def readGoals(self, romReader):
        self.resetGoals()
        romReader.romFile.seek(Objectives.objectivesList)
        checkFunction = romReader.romFile.readWord()
        checkScavEscape = False
        while checkFunction != 0x0000:
            goal = self.getGoalFromCheckFunction(checkFunction)
            if goal.name == 'finish scavenger hunt':
                checkScavEscape = True
            Objectives.activeGoals.append(goal)
            checkFunction = romReader.romFile.readWord()

        for goal in Objectives.activeGoals:
            LOG.debug("active goal: {}".format(goal.name))

        if checkScavEscape:
            Objectives.tourianRequired = not romReader.patchPresent('Escape_Scavenger')
            LOG.debug("tourianRequired: {}".format(Objectives.tourianRequired))

    def writeGoals(self, romFile):
        # write check functions
        romFile.seek(Objectives.objectivesList)
        for goal in Objectives.activeGoals:
            romFile.writeWord(goal.checkAddr)
        # list terminator
        romFile.writeWord(0x0000)

        # compute chars
        char2tile = {
            '.': 0x4A,
            '?': 0x4B,
            '!': 0x4C,
            ' ': 0x00,
            '%': 0x02,
            '*': 0x03,
            '0': 0x04,
            'a': 0x30,
        }
        for i in range(1, ord('z')-ord('a')+1):
            char2tile[chr(ord('a')+i)] = char2tile['a']+i
        for i in range(1, ord('9')-ord('0')+1):
            char2tile[chr(ord('0')+i)] = char2tile['0']+i

        # write text
        tileSize = 2
        lineLength = 32 * tileSize
        firstChar = 3 * tileSize
        # start at 8th line
        baseAddr = 0xB6F200 + lineLength * 8 + firstChar
        # space between two lines of text
        space = 3 if Objectives.nbActiveGoals == 5 else 4
        for i, goal in enumerate(Objectives.activeGoals):
            addr = baseAddr + i * lineLength * space
            text = goal.getText()
            romFile.seek(snes_to_pc(addr))
            for c in text:
                romFile.writeWord(0x3800 + char2tile[c])

        # write goal completed positions y in sprites OAM
        baseY = 0x40
        addr = snes_to_pc(0x82FD40)
        spritemapSize = 5 + 2
        for i, goal in enumerate(Objectives.activeGoals):
            y = baseY + i * space * 8
            # sprite center is at 128
            y = (y - 128) & 0xFF
            romFile.writeByte(y, addr+4 + i*spritemapSize)

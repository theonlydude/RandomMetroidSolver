import random
from rom.rom import snes_to_pc
from logic.helpers import Bosses
from logic.smbool import SMBool
import utils.log, logging

LOG = utils.log.get('Objectives')

class Synonyms(object):
    killSynonyms = [
        "massacre",
        "slaughter",
        "slay",
        "wipe out",
        "annihilate",
        "eradicate",
        "erase",
        "exterminate",
        "finish",
        "neutralize",
        "obliterate",
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
    def __init__(self, name, available, clearFunc, checkAddr, exclusionList, items, text, useSynonym):
        self.name = name
        self.available = available
        self.clearFunc = clearFunc
        # in bank $82, see objectives_pause.asm
        self.checkAddr = checkAddr
        self.rank = -1
        self.exclusionList = exclusionList
        self.items = items
        self.text = text
        self.useSynonym = useSynonym

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
        assert len(out) <= 28, "Goal text is too long: {}, max 28".format(len(out))
        return out

class Objectives(object):
    objectivesList = snes_to_pc(0x82f983)
    activeGoals = []
    nbActiveGoals = 0
    maxActiveGoals = 5
    tourianRequired = True
    goals = {
        "kill kraid": Goal("kill kraid", True, lambda sm: Bosses.bossDead(sm, 'Kraid'), 0xF98F,
                           ["kill G4"], ["Kraid"], "{} kraid", True),
        "kill phantoon": Goal("kill phantoon", True, lambda sm: Bosses.bossDead(sm, 'Phantoon'), 0xF997,
                              ["kill G4"], ["Phantoon"], "{} phantoon", True),
        "kill draygon": Goal("kill draygon", True, lambda sm: Bosses.bossDead(sm, 'Draygon'), 0xF99F,
                             ["kill G4"], ["Draygon"], "{} draygon", True),
        "kill ridley": Goal("kill ridley", True, lambda sm: Bosses.bossDead(sm, 'Ridley'), 0xF9A7,
                            ["kill G4"], ["Ridley"], "{} ridley", True),
        "kill G4": Goal("kill G4", True, lambda sm: Bosses.allBossesDead(sm), 0xF9AF,
                        ["kill kraid", "kill phantoon", "kill draygon", "kill ridley"],
                        ["Kraid", "Phantoon", "Draygon", "Ridley"],
                        "{} golden four", True),
        "kill spore spawn": Goal("kill spore spawn", True, lambda sm: Bosses.bossDead(sm, 'SporeSpawn'), 0xF9C5,
                                 ["kill mini bosses"], ["SporeSpawn"], "{} spore spawn", True),
        "kill botwoon": Goal("kill botwoon", True, lambda sm: Bosses.bossDead(sm, 'Botwoon'), 0xF9CD,
                             ["kill mini bosses"], ["Botwoon"], "{} botwoon", True),
        "kill crocomire": Goal("kill crocomire", True, lambda sm: Bosses.bossDead(sm, 'Crocomire'), 0xF9D5,
                               ["kill mini bosses"], ["Crocomire"], "{} crocomire", True),
        "kill golden torizo": Goal("kill golden torizo", True, lambda sm: Bosses.bossDead(sm, 'GoldenTorizo'), 0xF9E5,
                                   ["kill mini bosses"], ["GoldenTorizo"], "{} golden torizo", True),
        "kill mini bosses": Goal("kill mini bosses", True, lambda sm: Bosses.allMiniBossesDead(sm), 0xF9ED,
                                 ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo"],
                                 ["SporeSpawn", "Botwoon", "Crocomire", "GoldenTorizo"],
                                 "{} mini bosses", True),
        "shaktool cleared path": Goal("shaktool cleared path", False, None, 0xFA08,
                                      [], [], "shaktool cleared its path", False),
        "finish scavenger hunt": Goal("finish scavenger hunt", False, lambda sm: SMBool(True), 0xFA10,
                                      [], [], "finish scavenger hunt", False),
        "nothing": Goal("nothing", True, lambda sm: SMBool(True), 0xFA27, ["kill kraid", "kill phantoon", "kill draygon", "kill ridley", "kill G4", "kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo", "kill mini bosses", "shaktool cleared path", "finish scavenger hunt"], [], "nothing", False)
    }

    def resetGoals(self):
        Objectives.activeGoals = []
        Objectives.nbActiveGoals = 0

    def conflict(self, newGoalName):
        for goal in Objectives.activeGoals:
            if newGoalName in goal.exclusionList:
                return True
        return False

    def addGoal(self, goalName):
        if self.conflict(goalName):
            return
        goal = Objectives.goals[goalName]
        Objectives.nbActiveGoals += 1
        assert Objectives.nbActiveGoals <= Objectives.maxActiveGoals, "Too many active goals"
        goal.setRank(Objectives.nbActiveGoals)
        Objectives.activeGoals.append(goal)

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

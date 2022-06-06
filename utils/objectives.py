import random
from rom.addresses import Addresses
from logic.helpers import Bosses
from logic.smbool import SMBool
from logic.logic import Logic
import utils.log, logging

LOG = utils.log.get('Objectives')

class Synonyms(object):
    killSynonyms = [
        "defeat",
        "massacre",
        "slay",
        "wipe out",
        "erase",
        "finish",
        "destroy",
        "wreck",
        "smash",
        "crush",
        "end"
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
    def __init__(self, name, gtype, clearFunc, checkAddr,
                 escapeAccessPoints=None, exclusion=None, items=None, text=None,
                 available=True, expandableList=None, category=None, area=None):
        self.name = name
        self.available = available
        self.clearFunc = clearFunc
        # in bank $82, see objectives.asm
        self.checkAddr = checkAddr
        self.escapeAccessPoints = escapeAccessPoints
        if self.escapeAccessPoints is None:
            self.escapeAccessPoints = (1, [])
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
        if self.exclusion is None:
            self.exclusion = {"list": []}
        self.items = items
        if self.items is None:
            self.items = []
        self.text = name if text is None else text
        self.useSynonym = text is not None
        self.expandableList = expandableList
        if self.expandableList is None:
            self.expandableList = []
        self.expandable = len(self.expandableList) > 0
        self.category = category
        self.area = area

    def setRank(self, rank):
        self.rank = rank

    def canClearGoal(self, smbm, ap=None):
        # not all objectives require an ap (like limit objectives)
        return self.clearFunc(smbm, ap)

    def getText(self):
        out = "{}. ".format(self.rank)
        if self.useSynonym:
            out += self.text.format(Synonyms.getVerb())
        else:
            out += self.text
        assert len(out) <= 28, "Goal text '{}' is too long: {}, max 28".format(out, len(out))
        return out

    def isLimit(self):
        return "type" in self.exclusion

    def __repr__(self):
        return self.name

def getBossEscapeAccessPoint(boss):
    return (1, [Bosses.accessPoints[boss]])

def getG4EscapeAccessPoints(n):
    return (n, [Bosses.accessPoints[boss] for boss in Bosses.Golden4()])

def getMiniBossesEscapeAccessPoints(n):
    return (n, [Bosses.accessPoints[boss] for boss in Bosses.miniBosses()])

def getAreaEscapeAccessPoints(area):
    return (1, list({list(loc.AccessFrom.keys())[0] for loc in Logic.locations if loc.GraphArea == area}))

_goalsList = [
    Goal("kill kraid", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Kraid'), 0xF98F,
         escapeAccessPoints=getBossEscapeAccessPoint("Kraid"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Kraid"],
         text="{} kraid",
         category="Bosses"),
    Goal("kill phantoon", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Phantoon'), 0xF997,
         escapeAccessPoints=getBossEscapeAccessPoint("Phantoon"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Phantoon"],
         text="{} phantoon",
         category="Bosses"),
    Goal("kill draygon", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Draygon'), 0xF99F,
         escapeAccessPoints=getBossEscapeAccessPoint("Draygon"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Draygon"],
         text="{} draygon",
         category="Bosses"),
    Goal("kill ridley", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Ridley'), 0xF9A7,
         escapeAccessPoints=getBossEscapeAccessPoint("Ridley"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Ridley"],
         text="{} ridley",
         category="Bosses"),
    Goal("kill one G4", "other", lambda sm, ap: Bosses.xBossesDead(sm, 1), 0xFA43,
         escapeAccessPoints=getG4EscapeAccessPoints(1),
         exclusion={"list": ["kill kraid", "kill phantoon", "kill draygon", "kill ridley",
                             "kill all G4", "kill two G4", "kill three G4"],
                    "type": "boss",
                    "limit": 0},
         text="{} one golden4",
         category="Bosses"),
    Goal("kill two G4", "other", lambda sm, ap: Bosses.xBossesDead(sm, 2), 0xFA4C,
         escapeAccessPoints=getG4EscapeAccessPoints(2),
         exclusion={"list": ["kill all G4", "kill one G4", "kill three G4"],
                    "type": "boss",
                    "limit": 1},
         text="{} two golden4",
         category="Bosses"),
    Goal("kill three G4", "other", lambda sm, ap: Bosses.xBossesDead(sm, 3), 0xFA55,
         escapeAccessPoints=getG4EscapeAccessPoints(3),
         exclusion={"list": ["kill all G4", "kill one G4", "kill two G4"],
                    "type": "boss",
                    "limit": 2},
         text="{} three golden4",
         category="Bosses"),
    Goal("kill all G4", "other", lambda sm, ap: Bosses.allBossesDead(sm), 0xF9AF,
         escapeAccessPoints=getG4EscapeAccessPoints(4),
         exclusion={"list": ["kill kraid", "kill phantoon", "kill draygon", "kill ridley", "kill one G4", "kill two G4", "kill three G4"]},
         items=["Kraid", "Phantoon", "Draygon", "Ridley"],
         text="{} all golden4",
         expandableList=["kill kraid", "kill phantoon", "kill draygon", "kill ridley"],
         category="Bosses"),
    Goal("kill spore spawn", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'SporeSpawn'), 0xF9C5,
         escapeAccessPoints=getBossEscapeAccessPoint("SporeSpawn"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["SporeSpawn"],
         text="{} spore spawn",
         category="Minibosses"),
    Goal("kill botwoon", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'Botwoon'), 0xF9CD,
         escapeAccessPoints=getBossEscapeAccessPoint("Botwoon"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["Botwoon"],
         text="{} botwoon",
         category="Minibosses"),
    Goal("kill crocomire", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'Crocomire'), 0xF9D5,
         escapeAccessPoints=getBossEscapeAccessPoint("Crocomire"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["Crocomire"],
         text="{} crocomire",
         category="Minibosses"),
    Goal("kill golden torizo", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'GoldenTorizo'), 0xF9DD,
         escapeAccessPoints=getBossEscapeAccessPoint("GoldenTorizo"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["GoldenTorizo"],
         text="{} golden torizo",
         category="Minibosses"),
    Goal("kill one miniboss", "other", lambda sm, ap: Bosses.xMiniBossesDead(sm, 1), 0xFA5E,
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(1),
         exclusion={"list": ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo",
                             "kill all mini bosses", "kill two minibosses", "kill three minibosses"],
                    "type": "miniboss",
                    "limit": 0},
         text="{} one miniboss",
         category="Minibosses"),
    Goal("kill two minibosses", "other", lambda sm, ap: Bosses.xMiniBossesDead(sm, 2), 0xFA67,
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(2),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss", "kill three minibosses"],
                    "type": "miniboss",
                    "limit": 1},
         text="{} two minibosses",
         category="Minibosses"),
    Goal("kill three minibosses", "other", lambda sm, ap: Bosses.xMiniBossesDead(sm, 3), 0xFA70,
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(3),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss", "kill two minibosses"],
                    "type": "miniboss",
                    "limit": 2},
         text="{} three minibosses",
         category="Minibosses"),
    Goal("kill all mini bosses", "other", lambda sm, ap: Bosses.allMiniBossesDead(sm), 0xF9E5,
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(4),
         exclusion={"list": ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo",
                             "kill one miniboss", "kill two minibosses", "kill three minibosses"]},
         items=["SporeSpawn", "Botwoon", "Crocomire", "GoldenTorizo"],
         text="{} all mini bosses",
         expandableList=["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo"],
         category="Minibosses"),
    Goal("shaktool cleared path", "other", None, 0xF9FB,
         escapeAccessPoints=(1, ["Oasis Bottom"]),
         available=False),
    Goal("finish scavenger hunt", "other", lambda sm, ap: SMBool(True), 0xFA03,
         exclusion={"list":
             ["clear crateria", "clear green brinstar", "clear red brinstar", "clear wrecked ship", "clear kraid's lair",
              "clear upper norfair", "clear croc's lair", "clear lower norfair", "clear west maridia", "clear east maridia"]},
         available=False),
    Goal("nothing", "other", lambda sm, ap: Objectives.canAccess(sm, ap, "Landing Site"), 0xFA99,
         escapeAccessPoints=(1, ["Landing Site"])), # with no objectives at all, escape auto triggers only in crateria
    Goal("collect 25% items", "items", lambda sm, ap: SMBool(True), 0xFA79,
         exclusion={"list": ["collect 50% items", "collect 75% items", "collect 100% items"]},
         category="Items"),
    Goal("collect 50% items", "items", lambda sm, ap: SMBool(True), 0xFA81,
         exclusion={"list": ["collect 25% items", "collect 75% items", "collect 100% items"]},
         category="Items"),
    Goal("collect 75% items", "items", lambda sm, ap: SMBool(True), 0xFA89,
         exclusion={"list": ["collect 25% items", "collect 50% items", "collect 100% items"]},
         category="Items"),
    Goal("collect 100% items", "items", lambda sm, ap: SMBool(True), 0xFA91,
         exclusion={"list": ["collect 25% items", "collect 50% items", "collect 75% items", "collect all upgrades"]},
         category="Memes"),
    Goal("tickle the red fish", "other",
         lambda sm, ap: sm.wand(sm.haveItem('Grapple'), Objectives.canAccess(sm, ap, "Red Fish Room Bottom")),
         0xFAC1,
         escapeAccessPoints=(1, ["Red Fish Room Bottom"]),
         category="Memes"),
    Goal("kill the orange geemer", "other",
         lambda sm, ap: sm.wand(Objectives.canAccess(sm, ap, "Bowling"), # XXX this unnecessarily adds canPassBowling as requirement
                                sm.wor(sm.haveItem('Wave'), sm.canUsePowerBombs())),
         0xFAC9,
         escapeAccessPoints=(1, ["Bowling"]),
         text="{} orange geemer",
         category="Memes"),
    Goal("kill shaktool", "other",
         lambda sm, ap: sm.wand(Objectives.canAccess(sm, ap, "Oasis Bottom"),
                                sm.canTraverseSandPits(),
                                sm.canAccessShaktoolFromPantsRoom()),
         0xFAD1,
         escapeAccessPoints=(1, ["Oasis Bottom"]),
         text="{} shaktool",
         category="Memes"),
    Goal("collect all upgrades", "items", lambda sm, ap: SMBool(True), 0xFADD,
         category="Items"),
    Goal("clear crateria", "items", lambda sm, ap: SMBool(True), 0xFAF4,
         category="Items",
         area="Crateria",
         exclusion={"list": ["finish scavenger hunt"]}),
    Goal("clear green brinstar", "items", lambda sm, ap: SMBool(True), 0xFAFC,
         category="Items",
         area="GreenPinkBrinstar",
         exclusion={"list": ["finish scavenger hunt"]}),
    Goal("clear red brinstar", "items", lambda sm, ap: SMBool(True), 0xFB04,
         category="Items",
         area="RedBrinstar",
         exclusion={"list": ["finish scavenger hunt"]}),
    Goal("clear wrecked ship", "items", lambda sm, ap: SMBool(True), 0xFB0C,
         category="Items",
         area="WreckedShip",
         exclusion={"list": ["finish scavenger hunt"]}),
    Goal("clear kraid's lair", "items", lambda sm, ap: SMBool(True), 0xFB14,
         category="Items",
         area="Kraid",
         exclusion={"list": ["finish scavenger hunt"]}),
    Goal("clear upper norfair", "items", lambda sm, ap: SMBool(True), 0xFB1C,
         category="Items",
         area="Norfair",
         exclusion={"list": ["finish scavenger hunt"]}),
    Goal("clear croc's lair", "items", lambda sm, ap: SMBool(True), 0xFB24,
         category="Items",
         area="Crocomire",
         exclusion={"list": ["finish scavenger hunt"]}),
    Goal("clear lower norfair", "items", lambda sm, ap: SMBool(True), 0xFB2C,
         category="Items",
         area="LowerNorfair",
         exclusion={"list": ["finish scavenger hunt"]}),
    Goal("clear west maridia", "items", lambda sm, ap: SMBool(True), 0xFB34,
         category="Items",
         area="WestMaridia",
         exclusion={"list": ["finish scavenger hunt"]}),
    Goal("clear east maridia", "items", lambda sm, ap: SMBool(True), 0xFB3C,
         category="Items",
         area="EastMaridia",
         exclusion={"list": ["finish scavenger hunt"]})
]

_goals = {goal.name:goal for goal in _goalsList}
_goals["nothing"].exclusion["list"] = [goal.name for goal in _goalsList]

class Objectives(object):
    activeGoals = []
    nbActiveGoals = 0
    maxActiveGoals = 5
    totalItemsCount = 100
    goals = _goals
    graph = None

    def __init__(self, tourianRequired=True):
        self.tourianRequired = tourianRequired

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

    def isGoalActive(self, goalName):
        return Objectives.goals[goalName] in Objectives.activeGoals

    # having graph as a global sucks but Objectives instances are all over the place,
    # goals must access it, and it doesn't change often
    @staticmethod
    def setGraph(graph, maxDiff):
        Objectives.graph = graph
        Objectives.maxDiff = maxDiff
        for goalName, goal in Objectives.goals.items():
            if goal.area is not None:
                goal.escapeAccessPoints = getAreaEscapeAccessPoints(goal.area)

    @staticmethod
    def canAccess(sm, src, dst):
        return SMBool(Objectives.graph.canAccess(sm, src, dst, Objectives.maxDiff))

    @staticmethod
    def canAccessLocations(sm, ap, locs):
        availLocs = Objectives.graph.getAvailableLocations(Logic.locations, sm, Objectives.maxDiff, ap)
        for loc in locs:
            if loc not in availLocs:
                return SMBool(False)
        return SMBool(True)

    def setVanilla(self):
        self.addGoal("kill kraid")
        self.addGoal("kill phantoon")
        self.addGoal("kill draygon")
        self.addGoal("kill ridley")

    def setScavengerHunt(self):
        self.addGoal("finish scavenger hunt")

    def updateScavengerEscapeAccess(self, ap):
        assert self.isGoalActive("finish scavenger hunt")
        (_, apList) = Objectives.goals['finish scavenger hunt'].escapeAccessPoints
        apList.append(ap)

    def _replaceEscapeAccessPoints(self, goal, aps):
        (_, apList) = Objectives.goals[goal].escapeAccessPoints
        apList.clear()
        apList += aps

    def updateItemPercentEscapeAccess(self, collectedLocsAccessPoints):
        for pct in [25,50,75,100]:
            goal = 'collect %d%% items' % pct
            self._replaceEscapeAccessPoints(goal, collectedLocsAccessPoints)
        # not exactly accurate, but player has all upgrades to escape
        self._replaceEscapeAccessPoints("collect all upgrades", collectedLocsAccessPoints)

    def setScavengerHuntFunc(self, scavClearFunc):
        Objectives.goals["finish scavenger hunt"].clearFunc = scavClearFunc

    def setItemPercentFuncs(self, totalItemsCount=None, allUpgradeTypes=None):
        for pct in [25,50,75,100]:
            goal = 'collect %d%% items' % pct
            Objectives.goals[goal].clearFunc = lambda sm, ap: sm.hasItemsPercent(pct, totalItemsCount)
        if allUpgradeTypes is not None:
            Objectives.goals["collect all upgrades"].clearFunc = lambda sm, ap: sm.haveItems(allUpgradeTypes)

    def setAreaFuncs(self, funcsByArea):
        goalsByArea = {goal.area:goal for goalName, goal in Objectives.goals.items()}
        for area, func in funcsByArea.items():
            if area in goalsByArea:
                goalsByArea[area].clearFunc = func

    def setSolverMode(self, scavClearFunc, majorUpgrades):
        self.setScavengerHuntFunc(scavClearFunc)
        # in rando we know the number of items after randomizing, so set the functions only for the solver
        self.setItemPercentFuncs(allUpgradeTypes=majorUpgrades)

    def expandGoals(self):
        LOG.debug("Active goals:"+str(Objectives.activeGoals))
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
    def canClearGoals(smbm, ap):
        result = SMBool(True)
        for goal in Objectives.activeGoals:
            result = smbm.wand(result, goal.canClearGoal(smbm, ap))
        return result

    def getGoalFromCheckFunction(self, checkFunction):
        for name, goal in Objectives.goals.items():
            if goal.checkAddr == checkFunction:
                return goal
        assert True, "Goal with check function {} not found".format(hex(checkFunction))

    @staticmethod
    def getTotalItemsCount():
        return Objectives.totalItemsCount

    # call from web
    @staticmethod
    def getAddressesToRead():
        terminator = 1
        objectiveSize = 2
        bytesToRead = (Objectives.maxActiveGoals + terminator) * objectiveSize
        return [Addresses.getOne('objectivesList')+i for i in range(0, bytesToRead+1)] + Addresses.getWeb('totalItems') + Addresses.getWeb("itemsMask") + Addresses.getWeb("beamsMask")

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

    @staticmethod
    def getObjectivesCategories():
        return {goal.name: goal.category for goal in Objectives.goals.values() if goal.category is not None}

    # call from rando check pool and solver
    @staticmethod
    def getMandatoryBosses():
        r = [goal.items for goal in Objectives.activeGoals]
        return [item for items in r for item in items]

    @staticmethod
    def checkLimitObjectives(beatableBosses):
        # check that there's enough bosses/minibosses for limit objectives
        from logic.smboolmanager import SMBoolManager
        smbm = SMBoolManager()
        smbm.addItems(beatableBosses)
        for goal in Objectives.activeGoals:
            if not goal.isLimit():
                continue
            if not goal.canClearGoal(smbm):
                return False
        return True

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

    # call from solver
    def readGoals(self, romReader):
        self.resetGoals()
        romReader.romFile.seek(Addresses.getOne('objectivesList'))
        checkFunction = romReader.romFile.readWord()
        while checkFunction != 0x0000:
            goal = self.getGoalFromCheckFunction(checkFunction)
            Objectives.activeGoals.append(goal)
            checkFunction = romReader.romFile.readWord()

        # read number of available items for items % objectives
        Objectives.totalItemsCount = romReader.romFile.readByte(Addresses.getOne('totalItems'))

        for goal in Objectives.activeGoals:
            LOG.debug("active goal: {}".format(goal.name))

        self.tourianRequired = not romReader.patchPresent('Escape_Trigger')
        LOG.debug("tourianRequired: {}".format(self.tourianRequired))

    # call from rando
    def writeGoals(self, romFile):
        # write check functions
        romFile.seek(Addresses.getOne('objectivesList'))
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
        baseAddr = Addresses.getOne('objectivesText') + lineLength * 8 + firstChar
        # space between two lines of text
        space = 3 if Objectives.nbActiveGoals == 5 else 4
        for i, goal in enumerate(Objectives.activeGoals):
            addr = baseAddr + i * lineLength * space
            text = goal.getText()
            romFile.seek(addr)
            for c in text:
                if c not in char2tile:
                    continue
                romFile.writeWord(0x3800 + char2tile[c])

        # write goal completed positions y in sprites OAM
        baseY = 0x40
        addr = Addresses.getOne('objectivesSpritesOAM')
        spritemapSize = 5 + 2
        for i, goal in enumerate(Objectives.activeGoals):
            y = baseY + i * space * 8
            # sprite center is at 128
            y = (y - 128) & 0xFF
            romFile.writeByte(y, addr+4 + i*spritemapSize)

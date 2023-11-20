import random, copy
from rom.addresses import Addresses, MAX_OBJECTIVES
from rom.rom import pc_to_snes
from rom.map import ObjectiveMapIcon
from logic.helpers import Bosses
from logic.smbool import SMBool
from logic.logic import Logic
from utils.parameters import Knows, Settings
from graph.graph_utils import graphAreas
from graph.vanilla.map_tiles import objectives as map_icons
from utils.utils import randGaussBounds
import utils.log, logging

LOG = utils.log.get('Objectives')

class Synonyms(object):
    killSynonyms = [
        "Defeat",
        "Massacre",
        "Slay",
        "Wipe out",
        "Erase",
        "Finish",
        "Destroy",
        "Wreck",
        "Smash",
        "Crush",
        "End",
        "Kill"
    ]
    alreadyUsed = []
    @staticmethod
    def getVerb(maxLen):
        possibleVerbs = [syn for syn in Synonyms.killSynonyms if len(syn) <= maxLen]
        assert len(possibleVerbs) > 0, "could not find short enough synonym"
        verb = random.choice(possibleVerbs)
        while len(possibleVerbs) == len(Synonyms.killSynonyms) and verb in Synonyms.alreadyUsed:
            verb = random.choice(Synonyms.killSynonyms)
        Synonyms.alreadyUsed.append(verb)
        return verb

class Goal(object):
    def __init__(self, name, gtype, logicClearFunc, romClearFunc, romInProgressFunc=None,
                 escapeAccessPoints=None, objCompletedFuncAPs=lambda ap: [ap],
                 exclusion=None, items=None, text=None, introText=None, mapIcons=None,
                 available=True, expandableList=None, category=None, area=None,
                 conflictFunc=None):
        self.name = name
        self.available = available
        self.clearFunc = logicClearFunc
        self.objCompletedFuncAPs = objCompletedFuncAPs
        self.symbol = "objectives_%s" % romClearFunc
        self.inProgressSymbol = None
        if romInProgressFunc is not None:
            self.inProgressSymbol = "objectives_%s" % romInProgressFunc
        self.escapeAccessPoints = escapeAccessPoints
        if self.escapeAccessPoints is None:
            self.escapeAccessPoints = (1, [])
        self.rank = -1
        # possible values:
        #  - items
        #  - boss
        #  - miniboss
        #  - map
        #  - enemies
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
        self.introText = introText
        self.useSynonym = text is not None and '{}' in text
        self.expandableList = expandableList
        if self.expandableList is None:
            self.expandableList = []
        self.expandable = len(self.expandableList) > 0
        self.category = category
        self.area = area
        self.conflictFunc = conflictFunc
        self.mapIcons = mapIcons
        if self.mapIcons == None:
            self.mapIcons = []
        # used by solver/isolver to know if a goal has been completed
        self.completed = False

    def setClearFunc(self, value):
#        print(f"SET {self.name}: {value}")
        self.clearFunc = value

    @property
    def checkAddr(self):
        return pc_to_snes(Addresses.getOne(self.symbol)) & 0xffff

    @property
    def inProgressAddr(self):
        if self.inProgressSymbol is None:
            return 0
        return pc_to_snes(Addresses.getOne(self.inProgressSymbol)) & 0xffff

    def setRank(self, rank):
        self.rank = rank

    def canClearGoal(self, smbm, ap=None):
#        print(f"CALL {self.name}: {self.clearFunc}")
        # not all objectives require an ap (like limit objectives)
        return self.clearFunc(smbm, ap)

    def getText(self):
        idxTxt = "{}.".format(self.rank).ljust(3, ' ')
        out = idxTxt
        outLen = 0
        maxLen = 27
        try:
            if self.useSynonym:
                out += self.text.format(Synonyms.getVerb(maxLen - len(out) - len(self.text) + 2)) # 2 for the "{}"
            else:
                out += self.text
            outLen = len(out)
        except AssertionError as e:
            print(e)
            outLen = maxLen + 1
        assert outLen <= maxLen, "Goal '{}' text is too long: '{}'".format(self.name, out)
        out = out.rstrip()        
        if self.introText is not None:
            self.introText = idxTxt + self.introText
        else:
            self.introText = out
        return out

    def getIntroText(self):
        assert self.introText is not None
        return self.introText

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
    return (1, list({list(loc.AccessFrom.keys())[0] for loc in Logic.locations() if loc.GraphArea == area}))

def getEnemiesMapIcons(enemy):
    return [name for name in map_icons if name.startswith(enemy)]

_crocViaIceHellRun = Settings.hellRunsTable['Ice']['Norfair Entrance -> Croc via Ice']

enemiesLogic = {
    "Space Pirates": [
        {"Blue Brinstar Elevator Bottom": lambda sm: SMBool(True)},
        {"Green Pirates Shaft Bottom Right": lambda sm: sm.canPassCrateriaGreenPirates()},
        {"KraidRoomOut": lambda sm: sm.canPassCrateriaGreenPirates()},
        {"Business Center": lambda sm: sm.wand(sm.traverse('BusinessCenterTopLeft'),
                                               sm.canUsePowerBombs(),
                                               sm.wor(sm.wand(sm.haveItem('SpeedBooster'),
                                                              sm.canHellRun(**_crocViaIceHellRun)),
                                                      sm.wand(sm.canHellRun('Ice', _crocViaIceHellRun["mult"]/3, 3),
                                                              sm.canKillRedPirates())))},
        {"Crocomire Speedway Bottom": lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['Ice']['Croc -> Bubble Mountain']),
                                                         sm.canKillRedPirates())},
        {"LN Entrance": lambda sm: sm.canKillWorstRoomPirates()},
        {"Worst Room Top": lambda sm: sm.canKillWorstRoomPirates()},
        {"Ridley Zone": lambda sm: sm.canPassNinjaPirates()},
        {"Main Street Bottom": lambda sm: sm.wand(sm.canDoOuterMaridia(),
                                                  sm.wor(sm.haveItem('Plasma'),
                                                         sm.wand(sm.haveItem('Gravity'),
                                                                 sm.wor(sm.haveItem('ScrewAttack'),
                                                                        sm.canPseudoScrewPinkPirates(1)))))},
        {"Toilet Top": lambda sm: sm.wand(Bosses.bossDead(sm, "Draygon"),
                                          sm.canKillPlasmaPirates())}
    ],
    "Ki Hunters": [
        {"Keyhunter Room Bottom": lambda sm: SMBool(True)},
        {"Big Pink": lambda sm: sm.traverse("BigPinkTopRight")},
        {"KraidRoomOut": lambda sm: SMBool(True)},
        {"Firefleas": lambda sm: sm.canKillRedKiHunters(3)},
        {"Three Muskateers Room Left": lambda sm: sm.canKillRedKiHunters(3)},
        {"Wrecked Ship Main": lambda sm: Bosses.bossDead(sm, "Phantoon")}
    ],
    "Beetoms": [
        {"Gauntlet Top": lambda sm: sm.canKillBeetoms()},
        {'Etecoons Bottom': lambda sm: sm.canKillBeetoms()},
        {'Red Tower Top Left': lambda sm: sm.canKillBeetoms()},
        {'Warehouse Zeela Room Left': lambda sm: sm.wand(Bosses.bossDead(sm, "Kraid"),
                                                         sm.canKillBeetoms())},
        {
            "Business Center": lambda sm: sm.wand(sm.canPassFrogSpeedwayLeftToRight(),
                                                  sm.canKillBeetoms()),
            "Bubble Mountain Bottom": lambda sm: sm.wand(sm.canPassFrogSpeedwayRightToLeft(),
                                                         sm.canKillBeetoms())
        }
    ],
    "Cacatacs": [
        {"Noob Bridge Right": lambda sm: SMBool(True)},
        {"Red Brinstar Elevator": lambda sm: SMBool(True)},
        {"East Tunnel Right": lambda sm: SMBool(True)},
        {"Crocomire Speedway Bottom": lambda sm: SMBool(True)},
        {"Bubble Mountain Top": lambda sm: SMBool(True)},
        {"Post Botwoon": lambda sm: sm.wand(sm.canReachCacatacAlleyFromBotowoon(),
                                            sm.canPassCacatacAlleyEastToWest())}
    ],
    "Kagos": [
        {
            "Wrecked Ship Back": lambda sm: sm.canPassForgottenHighway(True),
            "Crab Maze Left": lambda sm: sm.haveItem("Morph")
        },
        {"Lower Mushrooms Left": lambda sm: SMBool(True)},
        {"Bubble Mountain Top": lambda sm: sm.wand(sm.haveItem("Morph"),
                                                   sm.canAccessDoubleChamberItems())}
    ],
    "Yapping Maws": [
        {"Landing Site": lambda sm: sm.wand(sm.canDoGauntletFromLandingSite(),
                                            sm.haveItem("Super"))},
        {"Red Tower Top Left": lambda sm: sm.wand(sm.canAccessXRayFromRedTower(),
                                                  sm.haveItem("Super"))},
        {"Red Brinstar Elevator": lambda sm: sm.wand(sm.traverse('RedTowerElevatorTopLeft'),
                                                     sm.canUsePowerBombs(),
                                                     sm.haveItem("Super"))},
        {'Crocomire Speedway Bottom': lambda sm: sm.wand(sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Kronic Boost Room <-> Croc']),
                                                         sm.haveItem("Super"))}
    ]
}

def getEnemiesLogicFunc(nmyType):
    nmyEntry = enemiesLogic[nmyType]
    def f(sm, ap):
        nonlocal nmyEntry, nmyType
        ret = SMBool(True)
        for apDict in nmyEntry:
            nmy = None
            for nmyApName, logicFunc in apDict.items():
                if not any(apObj.Name == nmyApName for apObj in Objectives.accessibleAPs):
                    continue
                if nmy is None:
                    nmy = SMBool(False)
                nmy = sm.wor(nmy, sm.wand(Objectives.canAccess(sm, ap, nmyApName), logicFunc(sm)))
            if nmy is not None:
                ret = sm.wand(ret, nmy)
        return ret
    return f

def getEnemiesAccessPoints(nmyType):
    allAPs = set()
    for apDict in enemiesLogic[nmyType]:
        allAPs.union(set(apDict.keys()))
    return list(allAPs)

def getEnemiesEscapeAccessPoints(nmyType):
    return (1, getEnemiesAccessPoints(nmyType))

GTsettingsConflict = lambda settings: settings.qty['energy'] == 'ultra sparse' and (not Knows.LowStuffGT or (Knows.LowStuffGT.difficulty > settings.maxDiff))

exploreSettingsConflict = lambda settings: settings.qty['energy'] == 'ultra sparse'

_goalsList = [
    # bosses
    Goal("kill kraid", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Kraid'), "kraid_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Kraid"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Kraid"],
         text="{} Kraid",
         mapIcons=["Kraid"],
         category="Bosses"),
    Goal("kill phantoon", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Phantoon'), "phantoon_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Phantoon"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Phantoon"],
         text="{} Phantoon",
         mapIcons=["Phantoon"],
         category="Bosses"),
    Goal("kill draygon", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Draygon'), "draygon_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Draygon"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Draygon"],
         text="{} Draygon",
         mapIcons=["Draygon"],
         category="Bosses"),
    Goal("kill ridley", "boss", lambda sm, ap: Bosses.bossDead(sm, 'Ridley'), "ridley_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Ridley"),
         exclusion={"list": ["kill all G4", "kill one G4"]},
         items=["Ridley"],
         text="{} Ridley",
         mapIcons=["Ridley"],
         category="Bosses"),
    Goal("kill one G4", "other", lambda sm, ap: Bosses.xBossesDead(sm, 1), "boss_1_killed",
         escapeAccessPoints=getG4EscapeAccessPoints(1),
         exclusion={"list": ["kill kraid", "kill phantoon", "kill draygon", "kill ridley",
                             "kill all G4", "kill two G4", "kill three G4"],
                    "type": "boss",
                    "limit": 0},
         text="{} one G4",
         mapIcons=Bosses.Golden4(),
         category="Bosses"),
    Goal("kill two G4", "other", lambda sm, ap: Bosses.xBossesDead(sm, 2),
         "boss_2_killed", romInProgressFunc="in_progress_boss_2_killed",
         escapeAccessPoints=getG4EscapeAccessPoints(2),
         exclusion={"list": ["kill all G4", "kill one G4", "kill three G4"],
                    "type": "boss",
                    "limit": 1},
         text="{} two G4      ",
         mapIcons=Bosses.Golden4(),
         category="Bosses"),
    Goal("kill three G4", "other", lambda sm, ap: Bosses.xBossesDead(sm, 3),
         "boss_3_killed", romInProgressFunc="in_progress_boss_3_killed",
         escapeAccessPoints=getG4EscapeAccessPoints(3),
         exclusion={"list": ["kill all G4", "kill one G4", "kill two G4"],
                    "type": "boss",
                    "limit": 2},
         text="{} three G4      ",
         mapIcons=Bosses.Golden4(),
         category="Bosses"),
    Goal("kill all G4", "other", lambda sm, ap: Bosses.allBossesDead(sm),
         "all_g4_dead", romInProgressFunc="in_progress_boss_4_killed",
         escapeAccessPoints=getG4EscapeAccessPoints(4),
         exclusion={"list": ["kill kraid", "kill phantoon", "kill draygon", "kill ridley", "kill one G4", "kill two G4", "kill three G4"]},
         items=["Kraid", "Phantoon", "Draygon", "Ridley"],
         text="{} all G4      ",
         expandableList=["kill kraid", "kill phantoon", "kill draygon", "kill ridley"],
         mapIcons=Bosses.Golden4(),
         category="Bosses"),
    # minibosses
    Goal("kill spore spawn", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'SporeSpawn'), "spore_spawn_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("SporeSpawn"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["SporeSpawn"],
         text="{} Spore Spawn",
         mapIcons=["SporeSpawn"],
         category="Minibosses"),
    Goal("kill botwoon", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'Botwoon'), "botwoon_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Botwoon"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["Botwoon"],
         text="{} Botwoon",
         mapIcons=["Botwoon"],
         category="Minibosses"),
    Goal("kill crocomire", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'Crocomire'), "crocomire_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("Crocomire"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["Crocomire"],
         text="{} Crocomire",
         mapIcons=["Crocomire"],
         category="Minibosses"),
    Goal("kill golden torizo", "miniboss", lambda sm, ap: Bosses.bossDead(sm, 'GoldenTorizo'), "golden_torizo_is_dead",
         escapeAccessPoints=getBossEscapeAccessPoint("GoldenTorizo"),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss"]},
         items=["GoldenTorizo"],
         text="{} Golden Torizo",
         mapIcons=["GoldenTorizo"],
         category="Minibosses",
         conflictFunc=GTsettingsConflict),
    Goal("kill one miniboss", "other", lambda sm, ap: Bosses.xMiniBossesDead(sm, 1), "miniboss_1_killed",
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(1),
         exclusion={"list": ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo",
                             "kill all mini bosses", "kill two minibosses", "kill three minibosses"],
                    "type": "miniboss",
                    "limit": 0},
         text="{} one miniboss",
         mapIcons=Bosses.miniBosses(),
         category="Minibosses"),
    Goal("kill two minibosses", "other", lambda sm, ap: Bosses.xMiniBossesDead(sm, 2),
         "miniboss_2_killed", romInProgressFunc="in_progress_miniboss_2_killed",
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(2),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss", "kill three minibosses"],
                    "type": "miniboss",
                    "limit": 1},
         text="{} two minibosses      ",
         mapIcons=Bosses.miniBosses(),
         category="Minibosses"),
    Goal("kill three minibosses", "other", lambda sm, ap: Bosses.xMiniBossesDead(sm, 3),
         "miniboss_3_killed", romInProgressFunc="in_progress_miniboss_3_killed",
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(3),
         exclusion={"list": ["kill all mini bosses", "kill one miniboss", "kill two minibosses"],
                    "type": "miniboss",
                    "limit": 2},
         text="{} 3 minibosses      ",
         mapIcons=Bosses.miniBosses(),
         category="Minibosses"),
    Goal("kill all mini bosses", "other", lambda sm, ap: Bosses.allMiniBossesDead(sm),
         "all_mini_bosses_dead", romInProgressFunc="in_progress_miniboss_4_killed",
         escapeAccessPoints=getMiniBossesEscapeAccessPoints(4),
         exclusion={"list": ["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo",
                             "kill one miniboss", "kill two minibosses", "kill three minibosses"]},
         items=["SporeSpawn", "Botwoon", "Crocomire", "GoldenTorizo"],
         text="{} all minibosses      ",
         expandableList=["kill spore spawn", "kill botwoon", "kill crocomire", "kill golden torizo"],
         mapIcons=Bosses.miniBosses(),
         category="Minibosses",
         conflictFunc=GTsettingsConflict),
    # other
    Goal("finish scavenger hunt", "other", lambda sm, ap: SMBool(True),
         "scavenger_hunt_completed", romInProgressFunc="scav_started",
         text="Finish Scavenger Hunt",
         exclusion={"list": []}, # will be auto-completed
         available=False),
    Goal("nothing", "other", lambda sm, ap: Objectives.canAccess(sm, ap, "Landing Site"), "nothing_objective",
         escapeAccessPoints=(1, ["Landing Site"])), # with no objectives at all, escape auto triggers only in crateria
    # items. no logic function because all items are placed by the rando. the functions are properly set for solver only.
    Goal("collect 25% items", "items", lambda sm, ap: SMBool(True),
         "collect_25_items", romInProgressFunc="items_percent",
         text="Collect 25% items",
         exclusion={"list": ["collect 50% items", "collect 75% items", "collect 100% items"]},
         category="Items",
         introText="collect 25 percent of items"),
    Goal("collect 50% items", "items", lambda sm, ap: SMBool(True),
         "collect_50_items", romInProgressFunc="items_percent",
         text="Collect 50% items",
         exclusion={"list": ["collect 25% items", "collect 75% items","collect 100% items"]},
         category="Items",
         introText="collect 50 percent of items"),
    Goal("collect 75% items", "items", lambda sm, ap: SMBool(True),
         "collect_75_items", romInProgressFunc="items_percent",
         text="Collect 75% items",
         exclusion={"list": ["collect 25% items", "collect 50% items", "collect 100% items"]},
         category="Items",
         introText="collect 75 percent of items"),
    Goal("collect 100% items", "items", lambda sm, ap: SMBool(True),
         "collect_100_items", romInProgressFunc="items_percent",
         text="Collect 100% items",
         exclusion={"list": ["collect 25% items", "collect 50% items", "collect 75% items", "collect all upgrades"]},
         category="Items",
         introText="collect all items"),
    Goal("collect all upgrades", "items", lambda sm, ap: SMBool(True),
         "all_major_items", romInProgressFunc="upgrades_collected",
         text="Get all upgrades",
         introText="collect all upgrades",
         category="Items"),
    Goal("clear crateria", "items", lambda sm, ap: SMBool(True),
         "crateria_cleared", romInProgressFunc="crateria_clear_progress",
         text="Clear Crateria",
         category="Items",
         area="Crateria"),
    Goal("clear green brinstar", "items", lambda sm, ap: SMBool(True),
         "green_brin_cleared", romInProgressFunc="green_brin_clear_progress",
         text="Clear Green Brin",
         introText="clear green brinstar",
         category="Items",
         area="GreenPinkBrinstar"),
    Goal("clear red brinstar", "items", lambda sm, ap: SMBool(True),
         "red_brin_cleared", romInProgressFunc="red_brin_clear_progress",
         text="Clear Red Brin",
         category="Items",
         area="RedBrinstar"),
    Goal("clear wrecked ship", "items", lambda sm, ap: SMBool(True),
         "ws_cleared", romInProgressFunc="ws_clear_progress",
         text="Clear Wreck Ship",
         introText="clear wrecked ship",
         category="Items",
         area="WreckedShip"),
    Goal("clear kraid's lair", "items", lambda sm, ap: SMBool(True),
         "kraid_cleared", romInProgressFunc="kraid_clear_progress",
         text="Clear Kraid's lair",
         category="Items",
         area="Kraid"),
    Goal("clear upper norfair", "items", lambda sm, ap: SMBool(True),
         "upper_norfair_cleared", romInProgressFunc="upper_norfair_clear_progress",
         text="Clear Up Norfair",
         introText="clear upper norfair",
         category="Items",
         area="Norfair"),
    Goal("clear croc's lair", "items", lambda sm, ap: SMBool(True),
         "croc_cleared", romInProgressFunc="croc_clear_progress",
         text="Clear Croc's lair",
         category="Items",
         area="Crocomire"),
    Goal("clear lower norfair", "items", lambda sm, ap: SMBool(True),
         "lower_norfair_cleared", romInProgressFunc="lower_norfair_clear_progress",
         text="Clear Low Norfair",
         introText="clear lower norfair",
         category="Items",
         area="LowerNorfair"),
    Goal("clear west maridia", "items", lambda sm, ap: SMBool(True),
         "west_maridia_cleared", romInProgressFunc="west_maridia_clear_progress",
         text="Clear West Maridia",
         category="Items",
         area="WestMaridia"),
    Goal("clear east maridia", "items", lambda sm, ap: SMBool(True),
         "east_maridia_cleared", romInProgressFunc="east_maridia_clear_progress",
         text="Clear East Marid",
         introText="clear east maridia",
         category="Items",
         area="EastMaridia"),
    # map
    Goal("explore 25% map", "map", lambda sm, ap: Objectives.canExploreMapPercent(sm, ap, 25), # assume this will always be possible, even with super fun
         "explored_map_25", romInProgressFunc="explored_all_map_percent",
         text="Explore 25% map",
         exclusion={"list": ["explore 50% map", "explore 75% map",  "explore 100% map"]},
         introText="explore 25 percent of map",
         category="Map"),
    Goal("explore 50% map", "map", lambda sm, ap: Objectives.canExploreMapPercent(sm, ap, 50), # assume this will always be possible, even with super fun
         "explored_map_50", romInProgressFunc="explored_all_map_percent",
         text="Explore 50% map",
         exclusion={"list": ["explore 25% map", "explore 75% map",  "explore 100% map"]},
         introText="explore 50 percent of map",
         category="Map"),
    Goal("explore 75% map", "map", lambda sm, ap: Objectives.canExploreMapPercent(sm, ap, 75), # assume this will always be possible, even with super fun
         "explored_map_75", romInProgressFunc="explored_all_map_percent",
         text="Explore 75% map",
         exclusion={"list": ["explore 50% map", "explore 25% map",  "explore 100% map"]},
         introText="explore 75 percent of map",
         category="Map"),
    Goal("explore 100% map", "map", lambda sm, ap: sm.wand(Objectives.canExploreMap(sm, ap),
                                                           sm.canExploreAmphitheater(), # requires SJ, so covers Croc 
                                                           sm.canGoUpMtEverest(),
                                                           sm.canPassCacatacAlleyEastToWest()),
         "explored_map_100", romInProgressFunc="explored_all_map_percent",
         exclusion={"list": ["explore 50% map", "explore 75% map",  "explore 25% map"]},
         text="Explore 100% map",
         introText="explore the entire map",
         conflictFunc=exploreSettingsConflict,
         category="Map"),
    Goal("explore crateria", "map", lambda sm, ap: Objectives.canExploreArea(sm, ap, "Crateria"),
         "crateria_explored", romInProgressFunc="crateria_explored_percent",
         conflictFunc=exploreSettingsConflict,
         text="Explore Crateria",
         category="Map",
         area="Crateria"),
    Goal("explore green brinstar", "map", lambda sm, ap: Objectives.canExploreArea(sm, ap, "GreenPinkBrinstar"),
         "green_brin_explored", romInProgressFunc="green_brin_explored_percent",
         text="Explore Green Brin",
         introText="explore green brinstar",
         category="Map",
         area="GreenPinkBrinstar"),
    Goal("explore red brinstar", "map", lambda sm, ap: Objectives.canExploreArea(sm, ap, "RedBrinstar"),
         "red_brin_explored", romInProgressFunc="red_brin_explored_percent",
         text="Explore Red Brin",
         introText="explore red brinstar",
         category="Map",
         area="RedBrinstar"),
    Goal("explore wrecked ship", "map", lambda sm, ap: Objectives.canExploreArea(sm, ap, "WreckedShip"),
         "ws_explored", romInProgressFunc="ws_explored_percent",
         text="Explore Wreck Ship",
         introText="explore wrecked ship",
         category="Map",
         area="WreckedShip"),
    Goal("explore kraid's lair", "map", lambda sm, ap: Objectives.canExploreArea(sm, ap, "Kraid"),
         "kraid_explored", romInProgressFunc="kraid_explored_percent",
         text="Explore Kraid Lair",
         introText="explore kraid's lair",
         category="Map",
         area="Kraid"),
    Goal("explore upper norfair", "map", lambda sm, ap: Objectives.canExploreArea(sm, ap, "Norfair"),
         "upper_norfair_explored", romInProgressFunc="upper_norfair_explored_percent",
         text="Explore Up Norfair",
         introText="explore upper norfair",
         category="Map",
         area="Norfair"),
    Goal("explore croc's lair", "map", lambda sm, ap: sm.wand(Objectives.canExploreArea(sm, ap, "Crocomire"),
                                                              sm.wor(sm.haveItem("SpeedBooster"), sm.haveItem("SpaceJump"))), # don't explore Post-Croc Jump Room w/ Bombs...
         "croc_explored", romInProgressFunc="croc_explored_percent",
         text="Explore Croc Lair",
         introText="explore croc's lair",
         category="Map",
         area="Crocomire"),
    Goal("explore lower norfair", "map", lambda sm, ap: sm.wand(Objectives.canExploreArea(sm, ap, "LowerNorfair"),
                                                                sm.canExploreAmphitheater()),
         "lower_norfair_explored", romInProgressFunc="lower_norfair_explored_percent",
         text="Explore Lower Norf",
         introText="explore lower norfair",
         conflictFunc=exploreSettingsConflict,
         category="Map",
         area="LowerNorfair"),
    Goal("explore west maridia", "map", lambda sm, ap: sm.wand(Objectives.canExploreArea(sm, ap, "WestMaridia"),
                                                               sm.canGoUpMtEverest()),
         "west_maridia_explored", romInProgressFunc="west_maridia_explored_percent",
         text="Explore West Marid",
         introText="explore west maridia",
         category="Map",
         area="WestMaridia"),
    Goal("explore east maridia", "map", lambda sm, ap: sm.wand(Objectives.canExploreArea(sm, ap, "EastMaridia"),
                                                               sm.canPassCacatacAlleyEastToWest()),
         "east_maridia_explored", romInProgressFunc="east_maridia_explored_percent",
         text="Explore East Marid",
         introText="explore east maridia",
         category="Map",
         area="EastMaridia"),
    # memes
    Goal("tickle the red fish", "other",
         lambda sm, ap: sm.wand(sm.haveItem('Grapple'), Objectives.canAccess(sm, ap, "Red Fish Room Bottom")),
         "fish_tickled",
         text="Tickle the Red Fish",
         escapeAccessPoints=(1, ["Red Fish Room Bottom"]),
         objCompletedFuncAPs=lambda ap: ["Red Fish Room Bottom"],
         mapIcons=["RedFish"],
         category="Memes"),
    Goal("kill the orange geemer", "other",
         lambda sm, ap: sm.wand(Objectives.canAccess(sm, ap, "Bowling"), # XXX this unnecessarily adds canPassBowling as requirement
                                sm.wor(sm.haveItem('Wave'), sm.canUsePowerBombs())),
         "orange_geemer",
         escapeAccessPoints=(1, ["Bowling"]),
         objCompletedFuncAPs=lambda ap: ["Bowling"],
         text="{} Orange Geemer",
         mapIcons=["OrangeGeemer"],
         category="Memes"),
    Goal("kill shaktool", "other",
         lambda sm, ap: sm.wand(Objectives.canAccess(sm, ap, "Oasis Bottom"),
                                sm.canTraverseSandPits(),
                                sm.canAccessShaktoolFromPantsRoom()),
         "shak_dead",
         escapeAccessPoints=(1, ["Oasis Bottom"]),
         objCompletedFuncAPs=lambda ap: ["Oasis Bottom"],
         text="{} Shaktool",
         mapIcons=["Shaktool"],
         category="Memes"),
    Goal("activate chozo robots", "other", lambda sm, ap: sm.wand(Objectives.canAccessLocation(sm, ap, "Bomb"),
                                                                  Objectives.canAccessLocation(sm, ap, "Gravity Suit"),
                                                                  sm.haveItem("GoldenTorizo"),
                                                                  sm.canPassLowerNorfairChozo()), # graph access implied by GT loc
         "all_chozo_robots", romInProgressFunc="in_progress_chozo_robots",
         category="Memes",
         text="Trigger Chozo bots      ",
         mapIcons=["BombTorizo", "GoldenTorizo", "WreckedShipChozo", "LowerNorfairChozo"],
         escapeAccessPoints=(3, ["Landing Site", "Screw Attack Bottom", "Bowling"]),
         objCompletedFuncAPs=lambda ap: ["Landing Site", "Screw Attack Bottom", "Bowling"],
         conflictFunc=GTsettingsConflict),
    Goal("visit the animals", "other", lambda sm, ap: sm.wand(Objectives.canAccess(sm, ap, "Big Pink"), sm.haveItem("SpeedBooster"), # dachora
                                                              Objectives.canAccess(sm, ap, "Etecoons Bottom")), # Etecoons
         "visited_animals", romInProgressFunc="in_progress_animals",
         text="Visit the animals      ",
         mapIcons=["Etecoons", "Dachora"],
         category="Memes",
         escapeAccessPoints=(2, ["Big Pink", "Etecoons Bottom"]),
         objCompletedFuncAPs=lambda ap: ["Big Pink", "Etecoons Bottom"]),
    Goal("kill king cacatac", "other",
         lambda sm, ap: Objectives.canAccess(sm, ap, 'Bubble Mountain Top'),
         "king_cac_dead",
         text="{} King Cacatac",
         mapIcons=["KingCacatac"],
         category="Memes",
         escapeAccessPoints=(1, ['Bubble Mountain Top']),
         objCompletedFuncAPs=lambda ap: ['Bubble Mountain Top']),
    # "kill all <enemy>" objectives
    Goal("kill all space pirates", "enemies",
         getEnemiesLogicFunc("Space Pirates"),
         "kill_all_space_pirates", romInProgressFunc="kill_all_space_pirates_progress",
         text="{} SpacePirates        ",
         introText="kill all space pirates",
         mapIcons=getEnemiesMapIcons("SpacePirates"),
         category="Enemies",
         escapeAccessPoints=getEnemiesEscapeAccessPoints("Space Pirates"),
         objCompletedFuncAPs=lambda ap: getEnemiesAccessPoints("Space Pirates")),
    Goal("kill all ki hunters", "enemies",
         getEnemiesLogicFunc("Ki Hunters"),
         "kill_all_ki_hunters", romInProgressFunc="kill_all_ki_hunters_progress",
         text="{} Ki Hunters        ",
         introText="kill all ki hunters",
         mapIcons=getEnemiesMapIcons("KiHunters"),
         category="Enemies",
         escapeAccessPoints=getEnemiesEscapeAccessPoints("Ki Hunters"),
         objCompletedFuncAPs=lambda ap: getEnemiesAccessPoints("Ki Hunters")),
    Goal("kill all beetoms", "enemies",
         getEnemiesLogicFunc("Beetoms"),
         "kill_all_beetoms", romInProgressFunc="kill_all_beetoms_progress",
         text="{} all Beetoms        ",
         mapIcons=getEnemiesMapIcons("Beetoms"),
         category="Enemies",
         escapeAccessPoints=getEnemiesEscapeAccessPoints("Beetoms"),
         objCompletedFuncAPs=lambda ap: getEnemiesAccessPoints("Beetoms")),
    Goal("kill all cacatacs", "enemies",
         getEnemiesLogicFunc("Cacatacs"),
         "kill_all_cacatacs", romInProgressFunc="kill_all_cacatacs_progress",
         text="{} all Cacatacs        ",
         mapIcons=getEnemiesMapIcons("Cacatacs"),
         category="Enemies",
         escapeAccessPoints=getEnemiesEscapeAccessPoints("Cacatacs"),
         objCompletedFuncAPs=lambda ap: getEnemiesAccessPoints("Cacatacs")),
    Goal("kill all kagos", "enemies",
         getEnemiesLogicFunc("Kagos"),
         "kill_all_kagos", romInProgressFunc="kill_all_kagos_progress",
         text="{} all Kagos      ",
         mapIcons=getEnemiesMapIcons("Kagos"),
         category="Enemies",
         escapeAccessPoints=getEnemiesEscapeAccessPoints("Kagos"),
         objCompletedFuncAPs=lambda ap: getEnemiesAccessPoints("Kagos")),
    Goal("kill all yapping maws", "enemies",
         getEnemiesLogicFunc("Yapping Maws"),
         "kill_all_yapping_maws", romInProgressFunc="kill_all_yapping_maws_progress",
         text="{} Yapping Maws        ",
         introText="kill all yapping maws",
         mapIcons=getEnemiesMapIcons("YappingMaws"),
         category="Enemies",
         escapeAccessPoints=getEnemiesEscapeAccessPoints("Yapping Maws"),
         objCompletedFuncAPs=lambda ap: getEnemiesAccessPoints("Yapping Maws"))
]

_goals = {goal.name:goal for goal in _goalsList}

goalCategories = sorted(list({obj.category for obj in _goalsList if obj.category is not None}))

def completeGoalData():
    # "nothing" is incompatible with everything
    _goals["nothing"].exclusion["list"] = [goal.name for goal in _goalsList]
    areaGoals = [goal for goal in _goalsList if goal.area is not None]
    itemAreaGoals = [goal.name for goal in areaGoals if goal.gtype == "items"]
    # if we need 100% items, don't require "clear area", as it covers those
    _goals["collect 100% items"].exclusion["list"] += itemAreaGoals[:]
    # if we have scav hunt, don't require "clear area" (HUD behaviour incompatibility)
    _goals["finish scavenger hunt"].exclusion["list"] += itemAreaGoals[:]
    # remove clear area goals if disabled tourian, as escape can trigger as soon as an area is cleared,
    # even if ship is not currently reachable
    for goal in itemAreaGoals:
        _goals[goal].exclusion['tourian'] = "Disabled"
    # if we need 100% map, don't require "explore area", as it covers those
    mapAreaGoals = [goal.name for goal in areaGoals if goal.gtype == "map"]
    _goals["explore 100% map"].exclusion["list"] += mapAreaGoals[:]

completeGoalData()

class Objectives(object):
    activeGoals = []
    nbActiveGoals = 0
    nbRequiredGoals = 0
    maxRequiredGoals = 9
    maxActiveGoals = MAX_OBJECTIVES
    totalItemsCount = 100
    goals = _goals
    graph = None
    tourianRequired = None
    hidden = False
    accessibleAPs = []
    # objectives are really needed when initiliazing rando, computing escape for disabled Tourian, and solver/tracker
    # we don't need them when placing items since the seed has to be completable 100% if generated, and objectives are
    # checked with 100% items during rando setup.
    permissive = False
    vanillaGoals = ["kill kraid", "kill phantoon", "kill draygon", "kill ridley"]
    scavHuntGoal = ["finish scavenger hunt"]

    def __init__(self, tourianRequired=None, randoSettings=None, reset=False):
        if tourianRequired is not None:
            Objectives.tourianRequired = tourianRequired
        self.randoSettings = randoSettings
        if reset:
            self.resetGoals()

    @property
    def tourianRequired(self):
        assert Objectives.tourianRequired is not None
        return Objectives.tourianRequired

    def resetGoals(self):
        Objectives.activeGoals = []
        Objectives.nbActiveGoals = 0
        for goal in Objectives.goals.values():
            goal.completed = False

    def conflict(self, newGoal):
        if newGoal.exclusion.get('tourian') == "Disabled" and self.tourianRequired == False:
            LOG.debug("new goal %s conflicts with disabled Tourian" % newGoal.name)
            return True
        LOG.debug("check if new goal {} conflicts with existing active goals".format(newGoal.name))
        count = 0
        for goal in Objectives.activeGoals:
            if newGoal.name in goal.exclusion["list"]:
                LOG.debug("new goal {} in exclusion list of active goal {}".format(newGoal.name, goal.name))
                return True
            if goal.name in newGoal.exclusion["list"]:
                LOG.debug("active goal {} in exclusion list of new goal {}".format(goal.name, newGoal.name))
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

        if self.randoSettings is not None and newGoal.conflictFunc is not None:
            if newGoal.conflictFunc(self.randoSettings):
                LOG.debug("new Goal {} is conflicting with rando settings".format(newGoal.name))
                return True
            LOG.debug("no conflict with rando settings detected for new goal {}".format(newGoal.name))

        return False

    def addGoal(self, goalName, completed=False):
        LOG.debug("addGoal: {}".format(goalName))
        goal = Objectives.goals[goalName]
        if self.conflict(goal):
            return
        Objectives.nbActiveGoals += 1
        assert Objectives.nbActiveGoals <= Objectives.maxActiveGoals, "Too many active goals. active: {} max: {}".format(Objectives.nbActiveGoals, Objectives.maxActiveGoals)
        goal.setRank(Objectives.nbActiveGoals)
        goal.completed = completed
        Objectives.activeGoals.append(goal)

    def removeGoal(self, goal):
        Objectives.nbActiveGoals -= 1
        Objectives.activeGoals.remove(goal)

    def clearGoals(self):
        Objectives.nbActiveGoals = 0
        Objectives.nbRequiredGoals = 0
        Objectives.activeGoals.clear()

    # call after objective list is built
    @staticmethod
    def setNbRequiredGoals(n):
        Objectives.nbRequiredGoals = min(Objectives.nbActiveGoals, max(0, min(n, Objectives.maxRequiredGoals)))

    @staticmethod
    def isGoalActive(goalName):
        return Objectives.goals[goalName] in Objectives.activeGoals

    @staticmethod
    def getNbRandomObjectives(nbAvailObj):
        maxObj = min(Objectives.maxActiveGoals, nbAvailObj)
        # make extreme values less likely
        return 1 + randGaussBounds(maxObj - 1, slope=3.5)

    @staticmethod
    def getNbRandomRequiredObjectives():
        # skewed towards more than half of the obj
        maxObj = min(Objectives.nbActiveGoals, Objectives.maxRequiredGoals)
        return min(1 + randGaussBounds(maxObj*1.25, slope=4.5), maxObj)

    # having graph as a global sucks but Objectives instances are all over the place,
    # goals must access it, and it doesn't change often
    @staticmethod
    def setGraph(graph, startAP, maxDiff):
        Objectives.accessibleAPs = graph.getAccessibleAccessPoints(startAP)
        Objectives.graph = graph
        Objectives.maxDiff = maxDiff
        for goal in Objectives.goals.values():
            if goal.area is not None:
                goal.escapeAccessPoints = getAreaEscapeAccessPoints(goal.area)

    @staticmethod
    def canAccess(sm, src, dst):
        return SMBool(Objectives.graph.canAccess(sm, src, dst, Objectives.maxDiff))

    @staticmethod
    def canAccessLocation(sm, ap, locName):
        loc = Logic.locationsDict()[locName]
        availLocs = Objectives.graph.getAvailableLocations([loc], sm, Objectives.maxDiff, ap)
        return SMBool(loc in availLocs)

    @staticmethod
    def canReachArea(sm, rootApName, area):
        graph, maxDiff = Objectives.graph, Objectives.maxDiff
        availAPs = graph.getAvailableAccessPoints(graph.accessPoints[rootApName], sm, maxDiff)
        return SMBool(any(ap.GraphArea == area for ap in availAPs))

    # XXX consider "explore map" equivalent to "access all locations and APs"

    @staticmethod
    def canExploreArea(sm, rootApName, area):
        graph, maxDiff = Objectives.graph, Objectives.maxDiff

        availAPs = graph.getAvailableAccessPoints(graph.accessPoints[rootApName], sm, maxDiff)
        areaAPs = [ap for ap in Objectives.accessibleAPs if ap.GraphArea == area]

        if not areaAPs:
            LOG.debug(f"canExploreArea {area} no ap available")
            return SMBool(False)

        for ap in areaAPs:
            if ap not in availAPs:
                LOG.debug(f"canExploreArea {area} {ap} not available")
                return SMBool(False)

        accessibleLocs = graph.getAccessibleLocations(Logic.locationsDict().values(), rootApName)
        # in solver we don't want to recompute already visited locations difficulty, so copy them first
        areaLocs = [copy.copy(loc) for loc in accessibleLocs if loc.GraphArea == area]
        availLocs = graph.getAvailableLocations(areaLocs, sm, maxDiff, rootApName)
        if not areaLocs:
            LOG.debug(f"canExploreArea {area} no loc available")
            return SMBool(False)

        if len(availLocs) != len(areaLocs):
            if LOG.getEffectiveLevel() == logging.DEBUG:
                missingLocs = [loc for loc in areaLocs if loc not in availLocs]
                LOG.debug(f"canExploreArea {area}, cannot access locs: {str(missingLocs)}")
            return SMBool(False)

        return SMBool(True)

    @staticmethod
    def canExploreMap(sm, rootApName):
        graph, maxDiff = Objectives.graph, Objectives.maxDiff
        allAPs = [ap for ap in Objectives.accessibleAPs if ap.GraphArea != "Tourian" and ap.GraphArea != "Ceres"]
        availAPs = graph.getAvailableAccessPoints(graph.accessPoints[rootApName], sm, maxDiff)
        for ap in allAPs:
            if ap not in availAPs:
                LOG.debug(f"canExploreMap {ap} not available")
                return SMBool(False)

        accessibleLocs = graph.getAccessibleLocations(Logic.locationsDict().values(), rootApName)
        allLocs = [copy.copy(loc) for loc in accessibleLocs if loc.GraphArea != "Tourian"]
        availLocs = graph.getAvailableLocations(allLocs, sm, maxDiff, rootApName)
        if len(availLocs) != len(allLocs):
            if LOG.getEffectiveLevel() == logging.DEBUG:
                missingLocs = [loc for loc in allLocs if loc not in availLocs]
                LOG.debug(f"canExploreMap, cannot access locs: {str(missingLocs)}")
            return SMBool(False)

        return SMBool(True)

    @staticmethod
    def canExploreMapPercent(sm, rootApName, percent):
        graph, maxDiff = Objectives.graph, Objectives.maxDiff
        # questionable heuristic: consider "access x% items" equivalent to "can reach x% locations"
        accessibleLocs = graph.getAccessibleLocations(Logic.locationsDict().values(), rootApName)
        allLocs = [copy.copy(loc) for loc in accessibleLocs if loc.GraphArea != "Tourian"]
        availLocs = graph.getAvailableLocations(allLocs, sm, maxDiff, rootApName)
        pct = 100*float(len(availLocs)) / float(len(allLocs))
        return SMBool(pct >= percent)

    def setVanilla(self):
        for goal in Objectives.vanillaGoals:
            self.addGoal(goal)
        Objectives.nbActiveGoals = len(Objectives.activeGoals)
        Objectives.nbRequiredGoals = len(Objectives.activeGoals)

    def isVanilla(self):
        # kill G4 and/or scav hunt
        if Objectives.nbActiveGoals == 1:
            for goal in Objectives.activeGoals:
                if goal.name not in Objectives.scavHuntGoal + ["kill all g4"]:
                    return False
            return True
        elif Objectives.nbActiveGoals == 4:
            for goal in Objectives.activeGoals:
                if goal.name not in Objectives.vanillaGoals:
                    return False
            return True
        elif Objectives.nbActiveGoals == 5:
            for goal in Objectives.activeGoals:
                if goal.name not in Objectives.vanillaGoals + Objectives.scavHuntGoal:
                    return False
            return True
        else:
            return False

    def setScavengerHunt(self):
        self.addGoal("finish scavenger hunt")

    def updateScavengerEscapeAccess(self, ap):
        assert Objectives.isGoalActive("finish scavenger hunt")
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
            goal = 'explore %d%% map' % pct
            self._replaceEscapeAccessPoints(goal, collectedLocsAccessPoints)
        # not exactly accurate, but player has all upgrades to escape
        self._replaceEscapeAccessPoints("collect all upgrades", collectedLocsAccessPoints)

    def setScavengerHuntFunc(self, scavClearFunc):
        Objectives.goals["finish scavenger hunt"].setClearFunc(scavClearFunc)

    def setItemPercentFuncs(self, totalItemsCount=None, allUpgradeTypes=None):
        def getPctFunc(pct, totalItemsCount):
            def f(sm, ap):
                nonlocal pct, totalItemsCount
                return sm.hasItemsPercent(pct, totalItemsCount)
            return f

        for pct in [25,50,75,100]:
            goal = 'collect %d%% items' % pct
            Objectives.goals[goal].setClearFunc(getPctFunc(pct, totalItemsCount))
        if allUpgradeTypes is not None:
            Objectives.goals["collect all upgrades"].setClearFunc(lambda sm, ap: sm.haveItems(allUpgradeTypes))

    def setAreaFuncs(self, funcsByArea):
        goalsByArea = {goal.area:goal for goalName, goal in Objectives.goals.items() if goal.area is not None and goal.gtype == "items"}
        for area, func in funcsByArea.items():
            if area in goalsByArea:
                goalsByArea[area].setClearFunc(func)

    def setSolverMode(self, solver):
        self.setScavengerHuntFunc(solver.scavengerHuntComplete)
        # in rando we know the number of items after randomizing, so set the functions only for the solver
        self.setItemPercentFuncs(allUpgradeTypes=solver.majorUpgrades)

        def getObjAreaFunc(area):
            def f(sm, ap):
                nonlocal solver, area
                visitedLocs = set([loc.Name for loc in solver.visitedLocations])
                allVisited = SMBool(all(locName in visitedLocs for locName in solver.splitLocsByArea[area]))
                return sm.wand(Objectives.canReachArea(sm, ap, area), allVisited)
            return f
        self.setAreaFuncs({area:getObjAreaFunc(area) for area in graphAreas})

    def expandGoals(self):
        LOG.debug("Active goals:"+str(Objectives.activeGoals))
        # try to replace 'kill all G4' with the four associated objectives.
        # we need at least 3 empty objectives out of the max (-1 +4)
        if Objectives.maxActiveGoals - Objectives.nbActiveGoals < 3:
            return

        expandables = [goal for goal in Objectives.activeGoals if goal.expandableList]

        if len(expandables) == 0:
            return

        for expandable in expandables:
            if Objectives.nbActiveGoals + len(expandable.expandableList) > Objectives.maxRequiredGoals:
                continue
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
        if Objectives.permissive == True:
            return result
        for goal in Objectives.activeGoals:
            result = smbm.wand(result, goal.canClearGoal(smbm, ap))
        return result

    # call from solver
    def checkGoals(self, smbm, ap):
        ret = {}

        for goal in Objectives.activeGoals:
            if goal.completed is True:
                continue
            # check if goal can be completed
            ret[goal.name] = goal.canClearGoal(smbm, ap)

        return ret

    def setGoalCompleted(self, goalName, completed):
        for goal in Objectives.activeGoals:
            if goal.name == goalName:
                goal.completed = completed
                return
        assert False, "Can't set goal {} completion to {}, goal not active".format(goalName, completed)

    def enoughGoalsCompleted(self):
        nCompleted = len([goal for goal in Objectives.activeGoals if goal.completed])
        return nCompleted >= Objectives.nbRequiredGoals

    def getGoalFromCheckFunction(self, checkFunction):
        for goal in Objectives.goals.values():
            if goal.checkAddr == checkFunction:
                return goal
        LOG.debug("Goal with check function {} not found".format(hex(checkFunction)))
        raise Exception("Goal not found")

    @staticmethod
    def getTotalItemsCount():
        return Objectives.totalItemsCount

    # call from web
    @staticmethod
    def getAddressesToRead():
        objectiveSize = 2
        bytesToRead = Objectives.maxActiveGoals * objectiveSize
        otherAddrs = ['totalItems', 'itemsMask', 'beamsMask', 'objectives_n_objectives', 'objectives_n_objectives_required']
        ret = [Addresses.getOne('objectivesList')+i for i in range(0, bytesToRead+1)]
        for addr in otherAddrs:
            ret += Addresses.getWeb(addr)
        return ret

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

    # call from interactivesolver
    def getState(self):
        return {
            "goals": {goal.name: goal.completed for goal in Objectives.activeGoals},
            "nbActiveGoals": Objectives.nbActiveGoals,
            "nbRequiredGoals": Objectives.nbRequiredGoals
        }

    def setState(self, state, tourianRequired):
        rank = 1
        for goalName, completed in state["goals"].items():
            goal = Objectives.goals[goalName]
            goal.completed = completed
            goal.rank = rank
            Objectives.activeGoals.append(goal)
            rank += 1
        Objectives.nbActiveGoals = state["nbActiveGoals"]
        Objectives.nbRequiredGoals = state["nbRequiredGoals"]
        Objectives.tourianRequired = tourianRequired

    def setTotalItemsCount(self, totalItemsCount):
        Objectives.totalItemsCount = totalItemsCount

    def resetCompletedGoals(self):
        for goal in Objectives.activeGoals:
            goal.completed = False

    # call from rando
    # exclude: excludes nothing
    @staticmethod
    def getAllGoals(exclude=False):
        excludeList = [] if not exclude else ["nothing"]
        return [goal.name for goal in Objectives.goals.values() if goal.available and goal.name not in excludeList]

    # call from rando
    def setRandom(self, nbGoals, availableGoals, distribute=False):
        LOG.debug(f"obj random, {len(availableGoals)} available goals: {str(availableGoals)}")
        def pickFromAll():
            while Objectives.nbActiveGoals < nbGoals and availableGoals:
                goalName = random.choice(availableGoals)
                self.addGoal(goalName)
                availableGoals.remove(goalName)
                LOG.debug(f"obj random {Objectives.nbActiveGoals}/{nbGoals}")
        def pickDistributed():
            availableGoalsObj = [Objectives.goals[goalName] for goalName in availableGoals]
            goalsByCategory = {cat:[obj.name for obj in availableGoalsObj if obj.category == cat] for cat in goalCategories}
            catList = []
            remainingGoals = sum(len(goals) for goals in goalsByCategory.values())
            while Objectives.nbActiveGoals < nbGoals and remainingGoals > 0:
                if not catList:
                    catList = goalCategories[:]
                    random.shuffle(catList)
                    LOG.debug(f"new catList: {catList}")
                category = None
                while category is None and catList:
                    category = catList.pop()
                    objList = goalsByCategory[category]
                    LOG.debug(f"goals for cat {category}: {objList}")
                    if objList:
                        goalName = random.choice(objList)
                        self.addGoal(goalName)
                        objList.remove(goalName)
                        remainingGoals -= 1
                        LOG.debug(f"obj random {Objectives.nbActiveGoals}/{nbGoals}")
                        break
        if distribute:
            pickDistributed()
        else:
            pickFromAll()

    # call from solver
    def readGoals(self, romReader):
        self.resetGoals()
        # read objective quantities
        Objectives.nbActiveGoals = romReader.romFile.readByte(Addresses.getOne('objectives_n_objectives'))
        Objectives.nbRequiredGoals = romReader.romFile.readByte(Addresses.getOne('objectives_n_objectives_required'))
        # in previous releases this info wasn't present in ROM, freespace default to 0xff
        Objectives.previousReleaseFallback = Objectives.nbActiveGoals == 0xff

        if Objectives.previousReleaseFallback:
            Objectives.nbActiveGoals = 0
            Objectives.nbRequiredGoals = 0
            self.setVanilla()
        else:
            # read objectives list
            romReader.romFile.seek(Addresses.getOne('objectivesList'))
            for i in range(Objectives.nbActiveGoals):
                checkFunction = romReader.romFile.readWord()
                goal = self.getGoalFromCheckFunction(checkFunction)
                Objectives.activeGoals.append(goal)

        # read number of available items for items % objectives
        totalItems = romReader.romFile.readByte(Addresses.getOne('totalItems'))
        # compatibility with previous releases
        Objectives.totalItemsCount = 100 if totalItems in [0x00, 0xff] else totalItems

        for goal in Objectives.activeGoals:
            LOG.debug("active goal: {}".format(goal.name))

        Objectives.tourianRequired = not romReader.isEscapeTrigger()
        LOG.debug("tourianRequired: {}".format(self.tourianRequired))

        LOG.debug(f"nbActiveGoals: {Objectives.nbActiveGoals}, nbRequiredGoals: {Objectives.nbRequiredGoals}")

    # call from rando
    def writeGoals(self, romFile, tourian):
        # write check functions
        romFile.seek(Addresses.getOne('objectivesList'))
        for goal in Objectives.activeGoals:
            romFile.writeWord(goal.checkAddr)
        # write "in progress" check functions
        romFile.seek(Addresses.getOne('objectives_in_progress_funcs'))
        for goal in Objectives.activeGoals:
            romFile.writeWord(goal.inProgressAddr)

        if Objectives.nbRequiredGoals == 0:
            Objectives.nbRequiredGoals = min(Objectives.nbActiveGoals, Objectives.maxRequiredGoals)
        else:
            Objectives.nbRequiredGoals = min(Objectives.nbRequiredGoals, Objectives.nbActiveGoals)

        # write number of objectives
        romFile.writeWord(Objectives.nbActiveGoals, Addresses.getOne('objectives_n_objectives'))
        romFile.writeWord(Objectives.nbRequiredGoals, Addresses.getOne('objectives_n_objectives_required'))

        # compute chars
        char2tile = {
            '.': 0x4A,
            '/': 0x4B,
            ' ': 0x00,
            '%': 0x150,
            '0': 0x160,
            'A': 0x30,
            '?': 0x1ab,
            "'": 0x1b9,
            "!": 0x1ba,
            ",": 0x1bb,
            "a": 0x87,
            "b": 0x88,
            "c": 0x95,
            "d": 0xa5,
            "e": 0x9e,
            "f": 0xbc,
            "g": 0xce,
            "h": 0x10c,
            "i": 0x10d,
            "j": 0x10e,
            "k": 0x11c,
            "l": 0x11d,
            "m": 0x11e,
            "n": 0x12c,
            "o": 0x12d,
            "p": 0x12e,
            "q": 0x144,
            "r": 0x1bf,
            "s": 0x14f,
            "t": 0x15f,
            "u": 0x1d8,
            "v": 0x1d9,
            "w": 0x1f4,
            "x": 0x1f5,
            "y": 0x1f6,
            "z": 0x1f7
        }
        for i in range(1, ord('Z')-ord('A')+1):
            char2tile[chr(ord('A')+i)] = char2tile['A']+i
        for i in range(1, ord('9')-ord('0')+1):
            char2tile[chr(ord('0')+i)] = char2tile['0']+i
        def writeString(text, addr=None):
            if addr is not None:
                romFile.seek(addr)
            for c in text:
                if c not in char2tile:
                    continue
                romFile.writeWord(0x2800 + char2tile[c])
        # write Tourian status
        writeString(tourian[:8].rjust(8, ' '), Addresses.getOne('objectives_obj_bg1_tilemap_tourian'))
        # write objectives text
        romFile.seek(Addresses.getOne('objectives_objs_txt'))
        addrs = []
        for i, goal in enumerate(Objectives.activeGoals):
            addrs.append(romFile.tell())
            writeString(goal.getText())
            romFile.writeWord(0xffff) # string terminator
            assert romFile.tell() < Addresses.getOne("objectives_objs_txt_limit"), "Objectives text too long"
        romFile.seek(Addresses.getOne("objectives_obj_txt_ptrs"))
        for addr in addrs:
            romFile.writeWord(pc_to_snes(addr) & 0xffff)
        # if objectives are hidden, write the name of the room to visit
        roomName = self._getHiddenObjRoomName(tourian)
        if roomName is not None:
            writeString(" %s." % roomName, Addresses.getOne("objectives_obj_bg1_tilemap_reveal_room"))
        self.writeIntroObjectives(romFile, tourian)

    def _getHiddenObjRoomName(self, tourian):
        roomName = None
        if Objectives.hidden == True:
            roomName = "Golden Statues Room"
            if tourian == "Fast":
                roomName = "Tourian Eye Door Room"
            noTourian = Objectives.graph.accessPoints["Golden Four"].ConnectedTo == "Golden Four"
            if noTourian:
                roomName = "Climb Escape Room"
        return roomName

    def writeIntroObjectives(self, rom, tourian):
        nActive, nReq = Objectives.nbActiveGoals, Objectives.nbRequiredGoals
        if self.isVanilla() and tourian == "Vanilla" and nActive == nReq:
            return
        # objectives or tourian are not vanilla, prepare intro text
        # two \n for an actual newline
        roomName = self._getHiddenObjRoomName(tourian)
        if roomName is None:
            maxDisplay = 6
            if nActive == nReq:
                text = "MISSION OBJECTIVES\n"
            else:
                text = "COMPLETE %d OUT OF\n" % nReq
            for i, goal in enumerate(Objectives.activeGoals):
                if i + 1 == maxDisplay and Objectives.nbActiveGoals > maxDisplay:
                    text += "\n\n... %d MORE ..." % (nActive - maxDisplay + 1)
                    break
                text += "\n\n%s" % goal.getIntroText()
        else:
            if nActive == nReq:
                text = "COMPLETE %d OBJECTIVE%s\n" % (nActive, "S" if nActive > 1 else "")
            else:
                text = "COMPLETE %d OUT OF %d POSSIBLE\n\nOBJECTIVES.\n" % (nReq, nActive)
            text += "\n\nTO REVEAL %s YOU MUST VISIT\n\n%s." % ("THEM" if nActive > 1 else "IT", roomName)
        text += "\n\n\nTOURIAN IS %s.\n\n\n" % tourian
        text += "CHECK OBJECTIVES STATUS IN\n\n"
        text += "THE PAUSE SCREEN."
        # actually write text in ROM
        self._writeIntroText(rom, text.upper())

    def _writeIntroText(self, rom, text, startX=1, startY=2):
        # for character translation
        charCodes = {
            ' ': 0xD67D,
            '.': 0xD75D,
            '!': 0xD77B,
            "'": 0xD76F,
            '0': 0xD721,
            'A': 0xD685
        }
        def addCharRange(start, end, base): # inclusive range
            for c in range(ord(start), ord(end)+1):
                offset = c - ord(base)
                charCodes[chr(c)] = charCodes[base]+offset*6
        addCharRange('B', 'Z', 'A')
        addCharRange('1', '9', '0')
        # actually write chars
        x, y = startX, startY
        def writeChar(c, frameDelay=2):
            nonlocal rom, x, y
            assert x <= 0x1F and y <= 0x18, "Intro text formatting error (x=0x%x, y=0x%x):\n%s" % (x, y, text)
            if c == '\n':
                x = startX
                y += 1
            else:
                assert c in charCodes, "Invalid intro char "+c
                rom.writeWord(frameDelay)
                rom.writeByte(x)
                rom.writeByte(y)
                rom.writeWord(charCodes[c])
                x += 1
        rom.seek(Addresses.getOne('introText'))
        for c in text:
            writeChar(c)
        # write trailer, see intro_text.asm
        rom.writeWord(0xAE5B)
        rom.writeWord(0x9698)

objective_mapicons = [ObjectiveMapIcon(i) for i in range(Objectives.maxActiveGoals)]

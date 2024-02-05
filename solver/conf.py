from utils.parameters import easy, medium
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, getAccessPoint

# split solver conf and rom conf into two separate objects
class SolverConf:
    defaultDifficultyTarget = medium
    defaultPickupStrategy = 'any'

    def __init__(self, mode, interactive):
        self.mode = mode
        self.interactive = interactive
        self.magic = None

        # keep getting majors of at most this difficulty before going for minors or changing area
        self.difficultyTarget = SolverConf.defaultDifficultyTarget

        # choose how many items are required (possible value: all (100%)/any (any%)).
        # for rando solver only: all_strict to fail if 100% is not possible.
        self.pickupStrategy = SolverConf.defaultPickupStrategy

        # display the generated path (spoilers!)
        self.displayGeneratedPath = False

        # the list of items to not pick up
        self.itemsForbidden = []

class StandardSolverConf(SolverConf):
    def __init__(self, args):
        super().__init__(mode='standard', interactive=False)
        if args.difficultyTarget is not None:
            self.difficultyTarget = args.difficultyTarget
        if args.pickupStrategy is not None:
            self.pickupStrategy = args.pickupStrategy
        self.displayGeneratedPath = args.displayGeneratedPath
        self.itemsForbidden = args.itemsForbidden

        self.romFileName = args.romFileName
        self.presetFileName = args.presetFileName
        self.magic = args.raceMagic

class RandoSolverConf(SolverConf):
    def __init__(self):
        super().__init__(mode='standard', interactive=False)
        self.difficultyTarget = easy
        self.pickupStrategy = 'all_strict'
        self.displayGeneratedPath = False
        self.itemsForbidden = []

class InteractiveSolverConf(SolverConf):
    def __init__(self, mode, romFileName, presetFileName):
        super().__init__(mode=mode, interactive=True)
        self.debug = mode == "debug"
        self.romFileName = romFileName
        self.presetFileName = presetFileName

class RomConf:
    def __init__(self):
        self.scavengerOrder = []
        self.plandoScavengerOrder = []
        self.additionalETanks = 0
        self.escapeRandoRemoveEnemies = True
        self.revealMap = False
        self.objectivesHidden = False
        self.objectivesHiddenOption = False
        self.eventsBitMasks = {}

    def initSeedless(self, extraSettings):
        self.majorsSplit = 'Full'
        self.masterMajorsSplit = 'Full'
        self.areaRando = True
        self.bossRando = True
        self.escapeRando = False
        self.escapeTimer = "03:00"

        self.startLocation = extraSettings.get('startLocation')
        self.startArea = getAccessPoint(self.startLocation).Start['solveArea']

        self.doorsRando = extraSettings.get('doorsRando')

        self.hasNothing = False
        self.tourian = 'Vanilla'
        self.majorUpgrades = []
        self.splitLocsByArea = {}

        # in seedless load all the vanilla transitions
        self.areaTransitions = vanillaTransitions[:]
        self.bossTransitions = vanillaBossesTransitions[:]
        self.escapeTransition = [vanillaEscapeTransitions[0]]
        # in seedless we allow mixing of area and boss transitions
        self.hasMixedTransitions = True

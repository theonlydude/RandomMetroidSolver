from copy import copy
from utils.parameters import easy, medium
from graph.graph_utils import vanillaTransitions, vanillaBossesTransitions, vanillaEscapeTransitions, getAccessPoint

# split solver conf and rom conf into two separate objects
class SolverConf:
    defaultDifficultyTarget = medium
    defaultPickupStrategy = 'any'

    def __init__(self, mode, interactive):
        self.debug = False
        # solver/standard (tracker)/seedless/plando/race/debug
        self.mode = mode
        self.interactive = interactive
        self.magic = None
        # set to true when the auto tracker starts, then to false when it ends
        self.autotracker = False

        # keep getting majors of at most this difficulty before going for minors or changing area
        self.difficultyTarget = SolverConf.defaultDifficultyTarget

        # choose how many items are required (possible value: all (100%)/any (any%)).
        # for rando solver only: all_strict to fail if 100% is not possible.
        self.pickupStrategy = SolverConf.defaultPickupStrategy

        # display the generated path (spoilers!)
        self.displayGeneratedPath = False

        # the list of items to not pick up
        self.itemsForbidden = []

    def getState(self):
        return self.__dict__.copy()

    def setState(self, state):
        self.__dict__.update(state)

class StandardSolverConf(SolverConf):
    def __init__(self, args):
        super().__init__(mode='solver', interactive=False)
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
        super().__init__(mode='solver', interactive=False)
        self.difficultyTarget = easy
        self.pickupStrategy = 'all_strict'
        self.displayGeneratedPath = False
        self.itemsForbidden = []

class InteractiveSolverConf(SolverConf):
    #  params: mode, romFileName, presetFileName
    def __init__(self, **kwargs):
        super().__init__(mode=kwargs["mode"], interactive=True)
        self.debug = kwargs["mode"] == "debug"
        self.romFileName = kwargs["romFileName"]
        self.presetFileName = kwargs["presetFileName"]

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

        self.majorsSplit = 'Full'
        self.masterMajorsSplit = 'Full'
        self.areaRando = False
        self.bossRando = False
        self.escapeRando = False
        self.escapeTimer = "03:00"

        self.startLocation = "Landing Site"
        self.startArea = "Crateria Landing Site"

        self.doorsRando = False
        self.hasNothing = False
        self.tourian = 'Vanilla'
        self.majorUpgrades = []
        self.splitLocsByArea = {}

        # to re-apply patches in plando
        self.hud = False
        self.round_robin_cf = False
        self.disable_spark_damage = False

        # vanilla transitions
        self.areaTransitions = vanillaTransitions[:]
        self.bossTransitions = vanillaBossesTransitions[:]
        self.escapeTransition = [vanillaEscapeTransitions[0]]
        self.hasMixedTransitions = False

    def initSeedless(self, extraSettings):
        # seedless allows area/boss rando
        self.areaRando = True
        self.bossRando = True

        self.startLocation = extraSettings.get('startLocation')
        self.startArea = getAccessPoint(self.startLocation).Start['solveArea']

        self.doorsRando = extraSettings.get('doorsRando')

        # in seedless we allow mixing of area and boss transitions
        self.hasMixedTransitions = True

    # serialize the solver state for the tracker
    def getState(self):
        state = self.__dict__.copy()
        # keep only locs names in scavenger order
        state["scavengerOrder"] = [loc.Name for loc in self.scavengerOrder]
        return state

    def setState(self, state):
        self.__dict__.update(state)

    # we first unserialize the rom conf, then the container
    def postSetState(self, container):
        # convert scavenger order back to locations
        self.scavengerOrder = [container.getLoc(locName) for locName in self.scavengerOrder]

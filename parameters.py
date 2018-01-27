from smbool import SMBool

# the different difficulties available
easy = 1
medium = 5
hard = 10
harder = 25
hardcore = 50
mania = 100

class Conf:
    # keep getting majors of at most this difficulty before going for minors or changing area
    difficultyTarget=medium

    # display the generated path (spoilers!)
    displayGeneratedPath = False

    # choose how many items are required
    #majorsPickup = 'minimal'
    #majorsPickup = 'all'
    majorsPickup = 'any'
    #minorsPickup = {
    #    'Missile' : 10,
    #    'Super' : 5,
    #    'PowerBomb' : 2
    #}
    #minorsPickup = 'all'
    minorsPickup = 'any'
class Knows:
    # the different technics to know (cf. http://deanyd.net/sm/index.php?title=Item_Randomizer)
    # and the personnal perceived difficulty.
    # False means: I can't do this technic or I don't know it.

    # universal
    # assume everyone knows wall jump & shinespark.
    #WallJump = (True, easy)
    #Shinespark = (True, easy)

    # used across the game
    Mockball = SMBool(True, easy, ['Mockball']) # early super and ice beam
    SimpleShortCharge = SMBool(True, easy, ['SimpleShortCharge']) # Waterway ETank without gravity, and Wrecked Ship access
    InfiniteBombJump = SMBool(True, medium, ['InfiniteBombJump']) # to access certain locations without high jump or space jump
    GreenGateGlitch = SMBool(True, medium, ['GreenGateGlitch']) # to access screw attack and crocomire
    ShortCharge = SMBool(False, 0, ['ShortCharge']) # to kill draygon
    GravityJump = SMBool(True, hard, ['GravityJump'])
    SpringBallJump = SMBool(True, hard, ['SpringBallJump']) # access to wrecked ship etank without anything else and suitless maridia navigation (precious room exit)
    GetAroundWallJump = SMBool(True, hard, ['GetAroundWallJump']) # tricky wall jumps where you have to get around the platform you want to wall jump on (access norfair reserve, go through worst room in the game, exit plasma room)

    # bosses
    DraygonGrappleKill = SMBool(True, medium, ['DraygonGrappleKill']) # easy kill for draygon
    MicrowaveDraygon = SMBool(True, easy, ['MicrowaveDraygon'])
    MicrowavePhantoon = SMBool(True, medium, ['MicrowavePhantoon'])

    # end game
    IceZebSkip = SMBool(False, 0, ['IceZebSkip']) # change minimal ammo count
    SpeedZebSkip = SMBool(False, 0, ['SpeedZebSkip']) # change minimal ammo count

    # Area difficulties

    # Brinstar
    CeilingDBoost = SMBool(True, easy, ['CeilingDBoost']) # for brinstar ceiling
    AlcatrazEscape = SMBool(True, harder, ['AlcatrazEscape']) # alcatraz without bomb
    ReverseGateGlitch = SMBool(True, medium, ['ReverseGateGlitch']) # ETank in Brinstar Gate
    ReverseGateGlitchHiJumpLess = SMBool(False, 0, ['ReverseGateGlitchHiJumpLess']) # Same but without high jump
    EarlyKraid = SMBool(True, easy, ['EarlyKraid']) # to access kraid without hi jump boots
    XrayDboost = SMBool(False, 0, ['XrayDboost'])  # Xray without grapple or space jump
    XrayIce = SMBool(True, hard, ['XrayIce']) # Xray with icing enemies
    RedTowerClimb = SMBool(True, harder, ['RedTowerClimb']) # brinstar red tower without ice or screw

    # gauntlet
    HiJumpLessGauntletAccess = SMBool(False, 0, ['HiJumpLessGauntletAccess'])
    HiJumpGauntletAccess = SMBool(True, harder, ['HiJumpGauntletAccess'])
    GauntletWithBombs = SMBool(True, hard, ['GauntletWithBombs'])
    GauntletWithPowerBombs = SMBool(True, medium, ['GauntletWithPowerBombs'])
    GauntletEntrySpark = SMBool(True, medium, ['GauntletEntrySpark']) # implies Knows.SimpleShortCharge

    # upper norfair
    NorfairReserveIce = SMBool(True, hard, ['NorfairReserveIce']) # climb to norfair reserve area by freezing a Waver
    WaveBeamWallJump = SMBool(True, easy, ['WaveBeamWallJump']) # climb to wave with wall jump
    ClimbToGrappleWithIce = SMBool(False, 0, ['ClimbToGrappleWithIce']) # just learn green gate glitch, it's easier

    # lower norfair
    LavaDive = SMBool(True, harder, ['LavaDive']) # ridley without gravity
    WorstRoomIceCharge = SMBool(True, mania, ['WorstRoomIceCharge']) # can pass worst room JUST by freezing pirates
    ScrewAttackExit = SMBool(True, medium, ['ScrewAttackExit']) # gain momentum from Golden Torizo Energy Recharge room, then wall jump in Screw Attack room

    # wrecked ship
    ContinuousWallJump = SMBool(False, 0, ['ContinuousWallJump']) # access wrecked ship
    DiagonalBombJump = SMBool(True, mania, ['DiagonalBombJump']) # access wrecked ship
    MockballWs = SMBool(True, hardcore, ['MockballWs']) # early wrecked ship access using a mock ball
    # wrecked ship etank access ("sponge bath" room)
    SpongeBathBombJump = SMBool(True, mania, ['SpongeBathBombJump'])
    SpongeBathHiJump = SMBool(True, easy, ['SpongeBathHiJump'])
    SpongeBathSpeed = SMBool(True, medium, ['SpongeBathSpeed'])

    # maridia
    # suitless
    SuitlessOuterMaridia = SMBool(True, hardcore, ['SuitlessOuterMaridia'])
    SuitlessOuterMaridiaNoGuns = SMBool(True, mania, ['SuitlessOuterMaridiaNoGuns']) # suitless maridia without even wave, spazer or plasma...
    # suitless draygon
    DraygonRoomGrappleExit = SMBool(False, 0, ['DraygonRoomGrappleExit'])
    DraygonRoomCrystalExit = SMBool(False, 0, ['DraygonRoomCrystalExit']) # give a free shine spark
    PreciousRoomXRayExit = SMBool(False, 0, ['PreciousRoomXRayExit'])
    # clips
    MochtroidClip = SMBool(True, medium, ['MochtroidClip']) # to access botwoon without speedbooster
    PuyoClip = SMBool(False, 0, ['PuyoClip']) # to access spring ball without grapple beam
    # plasma room
    KillPlasmaPiratesWithSpark = SMBool(False, 0, ['KillPlasmaPiratesWithSpark']) # kill plasma pirates with spark echoes. implies Knows.ShortCharge
    KillPlasmaPiratesWithCharge = SMBool(True, hard, ['KillPlasmaPiratesWithCharge'])
    # sandpit
    SuitlessSandpit = SMBool(False, 0, ['SuitlessSandpit']) # access the item in the sandpit suitless

class Settings:
    # boss difficulty tables :
    #
    # key is boss name. value is a dictionary where you define:
    #
    # 1. Rate : the rate of time in which you can land shots. For example
    # : 0.5 means you can land shots half the time in the boss (30secs in
    # a given minute). It represents a combination of the fraction of the
    # time you can hit the boss and your general accuracy against the boss.
    # If no information is given here, the fight will be
    # considered to be 2 minutes, regardless of anything else.
    #
    # 2. Energy : a dictionary where key is etanks+reserves you have,
    # value is estimated difficulty *for a 2-minute fight*. If etanks entry
    # is not defined, the one below will be chosen, or the minimum one if
    # no below entry is defined. You can give any difficulty number
    # instead of the fixed values defined above. The amount of energy you
    # have is to be considered with one suit only : it will be considered
    # *2 if you have both suits, and /2 if you have no suits.
    #
    # Actual difficulty calculation will also take into account estimated
    # fight duration. Difficulty will be multiplied with the ratio against
    # 2-minutes value entered here. The ammo margin will also be
    # considered if you do not have charge.
    #
    # If not enough info is provided here, base difficulty will be medium.
    bossesDifficulty = {
        'Kraid' : {
            'Rate' : 0.05,
            'Energy' : {
                1 : medium,
                2 : easy
            }
        },
        'Phantoon' : {
            'Rate' : 0.02,
            'Energy' : {
                1 : mania,
                3 : hardcore,
                4 : harder,
                5 : hard,
                7 : medium,
                10 : easy
            }
        },
        'Draygon' : {
            'Rate' : 0.08,
            'Energy' : {
                1 : mania,
                6 : hardcore,
                8 : harder,
                11 : hard,
                14 : medium,
                20 : easy
            },
        },
        'Ridley' : {
            'Rate' : 0.15,
            'Energy' : {
                1 : mania,
                7 : hardcore,
                11 : harder,
                14 : hard,
                20 : medium
            },
        },
        'Mother Brain' : {
            'Rate' : 0.5,
            'Energy' : {
                3 : mania, # less than 3 is actually impossible
                8 : hardcore,
                12 : harder,
                16 : hard,
                20 : medium,
                24 : easy
            }
        }
    }

    # hell run table (set to none for
    hellRuns = {
        # Ice Beam hell run
        'Ice' : [(2, hardcore), (3, hard), (4, medium), (6, easy)],
        # rest of upper norfair
        'MainUpperNorfair' : [(3, mania), (4, hardcore), (6, hard), (10, medium)]
    }

    # various settings used in difficulty computation
    algoSettings = {
        # Boss Fights

        # number of missiles fired per second during boss battles
        # (used along with Rate)
        'missilesPerSecond' : 3,
        # number of supers fired per second during boss battles
        # (used along with Rate)
        'supersPerSecond' : 1.85,
        # number of power bombs fired per second during boss battles
        # (used along with Rate)
        'powerBombsPerSecond' : 0.33,
        # number of charged shots per second (at most 1)
        'chargedShotsPerSecond' : 0.75,
        # firepower grabbed by picking up drops during boss battles
        # in missiles per minute (1 super = 3 missiles)
        'missileDropsPerMinute' : 12,
        # if no charge beam, amount of ammo margin to consider the boss
        # fight as 'normal' (1.5 = 50% more for instance)
        # boss fight difficulty will be linearly increased between this value
        # and 1
        'ammoMarginIfNoCharge' : 1.5,
        # divide the difficulty by this amount if charge or screw attack
        'phantoonFlamesAvoidBonus' : 1.2,
        # multiply the difficulty by this amount if no charge and few missiles
        'phantoonLowMissileMalus' : 1.2
    }

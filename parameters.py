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
    Mockball = (True, easy) # early super and ice beam
    SimpleShortCharge = (True, easy) # Waterway ETank without gravity, and Wrecked Ship access
    InfiniteBombJump = (True, medium) # to access certain locations without high jump or space jump
    GreenGateGlitch = (True, medium) # to access screw attack and crocomire
    ShortCharge = (False, 0) # to kill draygon
    GravityJump = (True, hard)
    SpringBallJump = (True, hard) # access to wrecked ship etank without anything else and suitless maridia navigation (precious room exit)

    # bosses
    DraygonGrappleKill = (True, medium) # easy kill for draygon
    MicrowaveDraygon = (True, easy)
    MicrowavePhantoon = (True, medium)

    # end game
    IceZebSkip = (False, 0) # change minimal ammo count
    SpeedZebSkip = (False, 0) # change minimal ammo count

    # Area difficulties

    # Brinstar
    CeilingDBoost = (True, easy) # for brinstar ceiling
    AlcatrazEscape = (True, harder) # alcatraz without bomb
    ReverseGateGlitch = (True, medium) # ETank in Brinstar Gate
    ReverseGateGlitchHiJumpLess = (False, 0) # Same but without high jump
    EarlyKraid = (True, easy) # to access kraid without hi jump boots
    XrayDboost = (False, 0)  # Xray without grapple or space jump
    XrayIce = (True, hard) # Xray with icing enemies
    RedTowerClimb = (True, harder) # brinstar red tower without ice or screw

    # gauntlet
    HiJumpLessGauntletAccess = (False, 0)
    HiJumpGauntletAccess = (True, harder)
    GauntletWithBombs = (True, hard)
    GauntletWithPowerBombs = (True, medium)
    GauntletEntrySpark = (True, medium) # implies Knows.SimpleShortCharge

    # upper norfair
    NorfairReserveHiJump = (True, hard) # climb to norfair reserve area by walljumping
    NorfairReserveIce = (True, hard) # climb to norfair reserve area by freezing a Waver
    WaveBeamWallJump = (True, easy) # climb to wave with wall jump
    ClimbToGrappleWithIce = (False, 0) # just learn green gate glitch, it's easier

    # lower norfair
    LavaDive = (True, harder) # ridley without gravity
    WorstRoomIceCharge = (True, mania) # can pass worst room JUST by freezing pirates
    WorstRoomHiJump = (True, hard) # can go up worst room with HiJump and wall jumps
    ScrewAttackExit = (True, medium) # gain momentum from Golden Torizo Energy Recharge room, then wall jump in Screw Attack room

    # wrecked ship
    ContinuousWallJump = (False, 0) # access wrecked ship
    DiagonalBombJump = (True, mania) # access wrecked ship
    MockballWs = (True, hardcore) # early wrecked ship access using a mock ball
    # wrecked ship etank access ("sponge bath" room)
    SpongeBathBombJump = (True, mania)
    SpongeBathHiJump = (True, easy)
    SpongeBathSpeed = (True, medium)

    # maridia
    # suitless
    SuitlessOuterMaridia = (True, hardcore)
    SuitlessOuterMaridiaNoGuns = (True, mania) # suitless maridia without even wave, spazer or plasma...
    # suitless draygon
    DraygonRoomGrappleExit = (False, 0)
    DraygonRoomCrystalExit = (False, 0) # give a free shine spark
    PreciousRoomXRayExit = (False, 0)
    # clips
    MochtroidClip = (True, medium) # to access botwoon without speedbooster
    PuyoClip = (False, 0) # to access spring ball without grapple beam
    # plasma room
    KillPlasmaPiratesWithSpark = (False, 0) # kill plasma pirates with spark echoes. implies Knows.ShortCharge
    KillPlasmaPiratesWithCharge = (True, hard)
    ExitPlasmaRoomHiJump = (True, medium)
    # sandpit
    SuitlessSandpit = (False, 0) # access the item in the sandpit suitless

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

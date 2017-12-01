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
    displayGeneratedPath = True

    # choose how many items are required

    # 100%:
    #  need them all (major & minor)
    #itemsPickup = '100%'

    # minimal:
    #  need only the minimal required major and minor items
    #   Morphing Ball (1)
    #   Charge (or enough minors to finish without)
    #   Missiles (enough to finish the game)
    #   Energy Tanks (4)
    #   Super Missiles (enough to finish the game)
    #   Varia Suit (1)
    #   Speed Boots (1) or Ice Beam (1)
    #   Power Bombs (1)
    #   Gravity Suit (1)
    itemsPickup = 'minimal'

    # normal:
    #  take all the majors as many missiles/supers as in minimal and 4 power bomb packs
    #itemsPickup = 'normal'

    # ultra minimal:
    #  take only the required items to end the game, just them, nothing more.
    #  just a test, not production ready
    #itemsPickup = 'ultra minimal'

class Knows:
    # the different technics to know (cf. http://deanyd.net/sm/index.php?title=Item_Randomizer)
    # and the personnal perceived difficulty.
    # False means: I can't do this technic or I don't know it.

    # universal
    # assume everyone knows wall jump & shinespark.
    #WallJump = (True, easy)
    #Shinespark = (True, easy)
    Mockball = (False, 0) # early super and ice beam

    # common
    CeilingDBoost = (False, 0) # for brinstar ceiling
    AlcatrazEscape = (False, 0) # alcatraz without bomb
    LavaDive = (False, 0) # ridley without gravity
    SimpleShortCharge = (False, 0) # Waterway ETank without gravity, and Wrecked Ship access
    InfiniteBombJump = (False, 0) # to access certain locations without high jump or space jump
    GreenGateGlitch = (False, 0) # to access screw attack and crocomire

    # uncommon
    MochtroidClip = (False, 0) # to access botwoon without speedbooster
    PuyoClip = (False, 0) # to access spring ball without grapple beam
    ReverseGateGlitch = (False, 0) # ETank in Brinstar Gate
    ShortCharge = (False, 0) # to kill draygon
    SuitlessOuterMaridia = (False, 0)
    SuitlessOuterMaridiaNoGuns = (False, 0) # suitless maridia without even wave, spazer or plasma...
    EarlyKraid = (False, 0) # to access kraid without hi jump boots
    DraygonGrappleKill = (False, 0) # easy kill for draygon

    # rare
    GravityJump = (False, 0)
    ContinuousWallJump = (False, 0) # access wrecked ship
    SpringBallJump = (False, 0) # access to wrecked ship etank without anything else and suitless maridia navigation
    XrayDboost = (False, 0)  # Xray without grapple or space jump

    # rarest
    DiagonalBombJump = (False, 0) # access wrecked ship

    # end game
    IceZebSkip = (False, 0) # change minimal ammo count
    SpeedZebSkip = (False, 0) # change minimal ammo count

    # Difficulties of specific parts

    # brinstar red tower without ice or screw
    RedTowerClimb = (False, 0)

    # gauntlet
    HiJumpGauntletAccess = (False, 0)
    GauntletWithBombs = (False, 0)
    GauntletWithPowerBombs = (False, 0)
    GauntletEntrySpark = (False, 0) # implies Knows.SimpleShortCharge

    # upper norfair
    NorfairReserveHiJump = (False, 0) # cilmb to norfair reserve area by walljumping
    WaveBeamWallJump = (False, 0) # climb to wave with wall jump 
    
    # worst room in the game
    WorstRoomIceCharge = (False, 0) # can pass worst room JUST by freezing pirates
    WorstRoomHiJump = (False, 0) # can go up worst room with HiJump and wall jumps

    # grapple
    ClimbToGrappleWithIce = (False, 0) # just learn green gate glitch, it's easier

    # wrecked ship etank access ("sponge bath" room)
    SpongeBathBombJump = (False, 0)
    SpongeBathHiJump = (False, 0)
    SpongeBathSpeed = (False, 0)

    # plasma room
    KillPlasmaPiratesWithSpark = (False, 0) # kill plasma pirates with spark echoes. implies Knows.ShortCharge
    KillPlasmaPiratesWithCharge = (False, 0)
    ExitPlasmaRoomHiJump = (False, 0)

    # sandpit
    SuitlessSandpit = (False, 0) # access the item in the sandpit suitless

    # wrecked ship
    MockballWs = (False, 0) # early wrecked ship access using a mock ball

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
    # value is estimated difficulty for a 2-minute fight. If etanks entry
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
                4 : hard,
                6 : medium,
                8 : easy
            }
        },
        'Draygon' : {
            'Rate' : 0.05,
            'Energy ' : {
                1 : mania,
                3 : hardcore,
                4 : harder,
                5 : hard,
                7 : medium,
                10 : easy
            },
        },
        'Ridley' : {
            'Rate' : 0.25,
            'Energy' : {
                1 : mania,
                6 : hardcore,
                8 : harder,
                10 : hard,
                14 : medium  # I'll never say Ridley is easy! ;)
            },
        },
        'Mother Brain' : {
            'Rate' : 0.5,
            'Energy' : {
                3 : mania, # less than 3 is actually impossible
                4 : hardcore,
                6 : harder,
                8 : hard,
                10 : medium,
                12 : easy
            }
        }
    }

    # hell run table
    hellRuns = {
        # Ice Beam hell run
        'Ice' : [(2, hardcore), (3, harder), (4, hard), (6, medium)],
        # rest of upper norfair
        'MainUpperNorfair' : [(3, mania), (4, hardcore), (6, hard), (8, medium)]
    }

    # various settings used in difficulty computation
    algoSettings = {
        # Boss Fights

        # number of missiles fired per second during boss battles
        # (used along with Rate)
        'missilesPerSecond' : 3,
        # number of supers fired per second during boss battles
        # (used along with Rate)
        'supersPerSecond' : 1.5,
        # number of power bombs fired per second during boss battles
        # (used along with Rate)
        'powerBombsPerSecond' : 1/3,
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

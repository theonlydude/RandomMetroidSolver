# the different difficulties available
easy = 1
medium = 5
hard = 10
harder = 25
hardcore = 50
mania = 100

# the different technics to know (cf. http://deanyd.net/sm/index.php?title=Item_Randomizer)
# and the personnal perceived difficulty.
# False means: I can't do this technic or I don't know it.

# universal
# assume everyone knows wall jump & shinespark.
#knowsWallJump = (True, easy)
#knowsShinespark = (True, easy)
knowsMockball = (True, easy) # early super and ice beam

# common
knowsCeilingDBoost = (True, easy) # for brinstar ceiling
knowsAlcatrazEscape = (False, 0) # alcatraz without bomb
knowsLavaDive = (True, harder) # ridley without gravity
knowsSimpleShortCharge = (True, easy) # Waterway ETank without gravity, and Wrecked Ship access
knowsInfiniteBombJump = (True, medium) # to access certain locations without high jump or space jump
knowsGreenGateGlitch = (True, medium) # to access screw attack and crocomire

# uncommon
knowsMochtroidClip = (True, medium) # to access botwoon without speedbooster
knowsPuyoClip = (False, 0) # to access spring ball without grapple beam
knowsReverseGateGlitch = (True, medium) # ETank in Brinstar Gate
knowsShortCharge = (False, 0) # to kill draygon
knowsSuitlessOuterMaridia = (True, hardcore)
knowsEarlyKraid = (True, easy) # to access kraid without hi jump boots
knowsDraygonGrappleKill = (True, medium) # easy kill for draygon

# rare
knowsGravityJump = (True, hard) 
knowsContinuousWallJump = (False, 0) # access wrecked ship
knowsSpringBallJump = (True, hard) 
knowsXrayDboost = (False, 0) 

# rarest
knowsDiagonalBombJump = (False, 0) # access wrecked ship

# end game
knowsZebSkip = (False, 0) # change minimal ammo count TODO FLO : not used yet

# choose how many items are required
# 100%:
#  need them all (major & minor)
# minimal:
#  need only the minimal required major and minor items
#   Morphing Ball (1)
#   Missiles (3)
#   Bombs (1)
#   Energy Tanks (3)
#   Charge Beam (1)
#   Super Missiles (2)
#   Varia Suit (1)
#   Speed Boots (1)
#   Power Bombs (1)
#   Gravity Suit (1)
# normal:
#  take all the majors and enough stuff, 60 super (12), 10 bomb (2), 5 missile (1)
#itemsPickup = 'normal'
#itemsPickup = '100%'
itemsPickup = 'minimal'

# display the generated path
displayGeneratedPath = True

# boss difficulty tables :
#
# key is boss name. value is a dictionary where you define:
#
# 1. Rate : the rate of time in which you can land shots. For example
# : 0.5 means you can land shots half the time in the boss (30secs in
# a given minute). If no information is given here, the fight will be
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
            9 : easy        
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

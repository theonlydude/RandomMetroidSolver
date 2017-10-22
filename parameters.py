# the different difficulties available
easy = 1
medium = 3
hard = 5
harder = 7
hardcore = 10
mania = 15

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
knowsAlcatrazEscape = (True, hardcore) # alcatraz without bomb
knowsLavaDive = (True, hardcore) # ridley without gravity
knowsSimpleShortCharge = (True, easy) # Waterway ETank without gravity, and Wrecked Ship access
knowsInfiniteBombJump = (True, hard) # to access certain locations without high jump or space jump
knowsGreenGateGlitch = (True, medium) # to access screw attack and crocomire

# uncommon
knowsMochtroidClip = (True, medium) # to access botwoon without speedbooster
knowsPuyoClip = (False, 0) # to access spring ball without grapple beam
knowsReverseGateGlitch = (True, medium) # ETank in Brinstar Gate
knowsShortCharge = (False, 0) 
knowsSuitlessOuterMaridia = (True, hardcore)
knowsEarlyKraid = (True, easy) # to access kraid without hi jump boots

# rare
knowsGravityJump = (False, 0) 
knowsContinuousWallJump = (False, 0) # access wrecked ship
knowsSpringBallJump = (False, 0) 
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
itemsPickup = 'normal'
#itemsPickup = '100%'
#itemsPickup = 'minimal'

# display the generated path
displayGeneratedPath = False

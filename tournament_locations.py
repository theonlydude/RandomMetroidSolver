# the canXXX functions
from helpers import *

# all the items locations with the prerequisites to access them

locations = [
{
    'Area': "Crateria",
    'Name': "Energy Tank, Gauntlet",
    'Class': "Major",
    'Address': 0x78264,
    'Visibility': "Visible",
    # EXPLAINED: difficulty already handled in the canEnterAndLeaveGauntlet function
    'Available': lambda items: canEnterAndLeaveGauntlet(items)
},
{
    'Area': "Crateria",
    'Name': "Bomb",
    'Address': 0x78404,
    'Class': "Major",
    'Visibility': "Chozo",
    # EXPLAINED: need to morph to enter Alcatraz. red door at Flyway.
    #            we may not have bombs or power bomb to get out of Alcatraz.
    'Available': lambda items: wand(haveItem(items, 'Morph'),
                                    canOpenRedDoors(items)),
    'PostAvailable': lambda items: wor(knowsAlcatrazEscape, 
                                       canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'Name': "Energy Tank, Terminator",
    'Class': "Major",
    'Address': 0x78432,
    'Visibility': "Visible",
    'Available': lambda items: wor(haveItem(items, 'SpeedBooster'), # FIXME getting through here with SpeedBooster is not easy...
                                   canDestroyBombWalls(items))
},
{
    'Area': "Brinstar",
    'Name': "Reserve Tank, Brinstar",
    'Class': "Major",
    'Address': 0x7852C,
    'Visibility': "Chozo",
    # EXPLAINED: break the bomb wall at left of Parlor and Alcatraz,
    #            open red door at Green Brinstar Main Shaft,
    #            mock ball for early retreval or speed booster
    'Available': lambda items: wand(wor(haveItem(items, 'SpeedBooster'),
                                        canDestroyBombWalls(items)),
                                    canOpenRedDoors(items),
                                    wor(wand(knowsMockball,
                                             haveItem(items, 'Morph')),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'Name': "Charge Beam",
    'Class': "Major",
    'Address': 0x78614,
    'Visibility': "Chozo",
    # EXPLAINED: open red door at Green Brinstar Main Shaft (down right),
    #            break the bomb wall at left of Parlor and Alcatraz
    'Available': lambda items: wand(canOpenRedDoors(items),
                                    wor(canPassBombPassages(items),
                                        canUsePowerBombs(items)))
},
{
    'Area': "Brinstar",
    'Name': "Morphing Ball",
    'Class': "Major",
    'Address': 0x786DE,
    'Visibility': "Visible",
    # EXPLAINED: no difficulty
    'Available': lambda items: (True, 0)
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Brinstar Ceiling",
    'Class': "Major",
    'Address': 0x7879E,
    'Visibility': "Hidden",
    # EXPLAINED: to get this major item the different technics are:
    #  -can fly (continuous bomb jump or space jump)
    #  -have the high jump boots
    #  -freeze the Reo to jump on it
    #  -do a damage boost with one of the two Geemers
    'Available': lambda items: wor(knowsCeilingDBoost,
                                   canFly(items),
                                   haveItem(items, 'HiJump'),
                                   haveItem(items, 'Ice'))
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Etecoons",
    'Class': "Major",
    'Address': 0x787C2,
    'Visibility': "Visible",
    # EXPLAINED: break the bomb wall at left of Parlor and Alcatraz,
    #            power bomb down of Green Brinstar Main Shaft
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Waterway",
    'Class': "Major",
    'Address': 0x787FA,
    'Visibility': "Visible",
    # EXPLAINED: break the bomb wall at left of Parlor and Alcatraz with power bombs,
    #            open red door at Green Brinstar Main Shaft (down right),
    #            power bomb at bottom of Big Pink (Charge Beam),
    #            open red door leading to waterway,
    #            at waterway, either do:
    #  -with gravity do a speed charge
    #  -a simple short charge from the blocks above the water
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    canOpenRedDoors(items),
                                    haveItem(items, 'SpeedBooster'),
                                    wor(haveItem(items, 'Gravity'),
                                        knowsSimpleShortCharge))
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Brinstar Gate",
    'Class': "Major",
    'Address': 0x78824,
    'Visibility': "Visible",
    # DONE: use knowsReverseGateGlitch
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    wor(haveItem(items, 'Wave'),
                                        wand(haveItem(items, 'Super'),
                                             haveItem(items, 'HiJump'),
                                             knowsReverseGateGlitch)))
},
{
    'Area': "Brinstar",
    'Name': "X-Ray Scope",
    'Class': "Major",
    'Address': 0x78876,
    'Visibility': "Chozo",
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    canUsePowerBombs(items),
                                    wor(haveItem(items, 'Grapple'),
                                        haveItem(items, 'SpaceJump'),
                                        wand(haveItem(items, 'Varia'),
                                             energyReserveCountOk(items, 4),
                                             knowsXrayDboost),
                                        wand(energyReserveCountOk(items, 6),
                                             knowsXrayDboost)))
},
{
    'Area': "Brinstar",
    'Name': "Spazer",
    'Class': "Major",
    'Address': 0x7896E,
    'Visibility': "Chozo",
    # DONE: no difficulty
    'Available': lambda items: canAccessRedBrinstar(items)
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Kraid",
    'Class': "Major",
    'Address': 0x7899C,
    'Visibility': "Hidden",
    # DONE: no difficulty
    'Available': lambda items: wand(canAccessKraid(items), bossDead('Kraid'))
},
{
    'Area': "Brinstar",
    'Name': "Varia Suit",
    'Class': "Major",
    'Address': 0x78ACA,
    'Visibility': "Chozo",
    # DONE: no difficulty
    'Available': lambda items: wand(canAccessKraid(items),                                    
                                    enoughStuffsKraid(items)),
    'Pickup': lambda: beatBoss('Kraid')
},
{
    'Area': "Norfair",
    'Name': "Ice Beam",
    'Class': "Major",
    'Address': 0x78B24,
    'Visibility': "Chozo",
    # DONE: harder without varia
    'Available': lambda items: wand(canAccessKraid(items),
                                    wor(heatProof(items),
                                        energyReserveCountOkList(items, hellRuns['Ice'])),
                                    wor(wand(haveItem(items, 'Morph'),
                                             knowsMockball),
                                        haveItem(items, 'SpeedBooster'))) # FIXME : knowsEarlyKraid has nothing to do with this and is implied by canAccessKraid
},
{
    'Area': "Norfair",
    'Name': "Energy Tank, Crocomire",
    'Class': "Major",
    'Address': 0x78BA4,
    'Visibility': "Visible",
    # DONE: difficulty already set in canHellRun
    'Available': lambda items: canAccessCrocomire(items)
},
{
    'Area': "Norfair",
    'Name': "Hi-Jump Boots",
    'Class': "Major",
    'Address': 0x78BAC,
    'Visibility': "Chozo",
    # DONE: no difficulty
    'Available': lambda items: canAccessRedBrinstar(items)
},
{
    'Area': "Norfair",
    'Name': "Grapple Beam",
    'Class': "Major",
    'Address': 0x78C36,
    'Visibility': "Chozo",
    'Available': lambda items: wand(canAccessCrocomire(items),
                                    wor(canFly(items),
                                        wand(haveItem(items, 'Ice'),
                                             knowsClimbToGrappleWithIce),
                                        haveItem(items, 'SpeedBooster'),
                                        knowsGreenGateGlitch))
},
{
    'Area': "Norfair",
    'Name': "Reserve Tank, Norfair",
    'Class': "Major",
    'Address': 0x78C3E,
    'Visibility': "Chozo",
    # TODO: also Ice to freeze a Waver
    'Available': lambda items: wand(canAccessHeatedNorfair(items),
                                    wor(canFly(items),
                                        haveItem(items, 'Grapple'),
                                        haveItem(items, 'HiJump', difficulty=hard)))
},
{
    'Area': "Norfair",
    'Name': "Speed Booster",
    'Class': "Major",
    'Address': 0x78C82,
    'Visibility': "Chozo",
    # DONE: difficulty already done in the function
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Wave Beam",
    'Class': "Major",
    'Address': 0x78CCA,
    'Visibility': "Chozo",
    # DONE: this one is not easy without grapple beam nor space jump, with hijump medium wall jump is required
    # FLO : no need of high jump for this, just wall jumping
    'Available': lambda items: wand(canAccessHeatedNorfair(items),
                                    wor(haveItem(items, 'Grapple'),
                                        haveItem(items, 'SpaceJump'),
                                        (True, medium)))
},
{
    'Area': "LowerNorfair",
    'Name': "Energy Tank, Ridley",
    'Class': "Major",
    'Address': 0x79108,
    'Visibility': "Hidden",
    # DONE: already set in function
    'Available': lambda items: wand(canPassWorstRoom(items),
                                    enoughStuffsRidley(items)),
    'Pickup': lambda: beatBoss('Ridley')
},
{
    'Area': "LowerNorfair",
    'Name': "Screw Attack",
    'Class': "Major",
    'Address': 0x79110,
    'Visibility': "Chozo",
    # DONE: easy with green gate glitch
    'Available': lambda items: wand(canAccessLowerNorfair(items),
                                    wor(haveItem(items, 'SpaceJump'),
                                        knowsGreenGateGlitch))
},
{
    'Area': "LowerNorfair",
    'Name': "Energy Tank, Firefleas",
    'Class': "Major",
    'Address': 0x79184,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "WreckedShip",
    'Name': "Reserve Tank, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C2E9,
    'Visibility': "Chozo",
    # DONE: easy
    'Available': lambda items: wand(canAccessWs(items),
                                    haveItem(items, 'SpeedBooster'),
                                    wor(haveItem(items, 'Varia'),
                                        energyReserveCountOk(items, 1)),
                                    bossDead('Phantoon'))
},
{
    'Area': "WreckedShip",
    'Name': "Energy Tank, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C337,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessWs(items),
                                    bossDead('Phantoon'),
                                    wor(wor(haveItem(items, 'Bomb'),
                                            haveItem(items, 'PowerBomb')),
                                        knowsSpongeBathBombJump,
                                        wand(haveItem(items, 'HiJump'),
                                             knowsSpongeBathHiJump),
                                        wor(haveItem(items, 'SpaceJump', difficulty=easy),
                                            wand(haveItem(items, 'SpeedBooster'),
                                                 knowsSpongeBathSpeed),
                                            wand(haveItem(items, 'SpringBall'),
                                                 knowsSpringBallJump))))
},
{
    'Area': "WreckedShip",
    'Name': "Right Super, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C365,
    'Visibility': "Visible",
    # DONE: easy once WS is accessible
    'Available': lambda items: wand(canAccessWs(items),
                                    enoughStuffsPhantoon(items)),
    'Pickup': lambda: beatBoss('Phantoon')
},
{
    'Area': "WreckedShip",
    'Name': "Gravity Suit",
    'Class': "Major",
    'Address': 0x7C36D,
    'Visibility': "Chozo",
    # DONE: easy
    'Available': lambda items: wand(canAccessWs(items),
                                    bossDead('Phantoon'),
                                    wor(haveItem(items, 'Varia'),
                                        energyReserveCountOk(items, 1)))
},
{
    'Area': "Maridia",
    'Name': "Energy Tank, Mama turtle",
    'Class': "Major",
    'Address': 0x7C47D,
    'Visibility': "Visible",
    # DONE: difficulty already handled in canAccessOuterMaridia
    # to acces the ETank in higher part of the room:
    #  -use grapple to attach to the block
    #  -use speedbooster ??
    #  FIXME: is SpeedBooster possible without gravity in this room ? is it a simple short or short charge ?
    #  -can fly (space jump or infinite bomb jump)
    #  FIXME: is it possible to infinite bomb jump from the mama turtle when it's up ?
    'Available': lambda items: wand(canAccessOuterMaridia(items),
                                    wor(canFly(items),
                                        haveItem(items, 'SpeedBooster'),
                                        haveItem(items, 'Grapple')))
},
{
    'Area': "Maridia",
    'Name': "Plasma Beam",
    'Class': "Major",
    'Address': 0x7C559,
    'Visibility': "Chozo",
    # DONE: to leave the Plasma Beam room you have to kill the space pirates and return to the door
    # to unlock the door:
    #  -can access draygon room to kill him
    # to kill the space pirates:
    #  -do short charges with speedbooster
    #  -do beam charges with spin jump attacks
    #  -have screw attack
    #  -have plasma beam
    # to go back to the door:
    #  -have high jump boots
    #  -can fly (space jump or infinite bomb jump)
    #  -use short charge with speedbooster
    'Available': lambda items: wand(canDefeatDraygon(items),
                                    bossDead('Draygon'),
                                    wor(wand(haveItem(items, 'SpeedBooster'),
                                             knowsShortCharge,
                                             knowsKillPlasmaPiratesWithSpark),
                                        wand(haveItem(items, 'Charge'),
                                             knowsKillPlasmaPiratesWithCharge),
                                        haveItem(items, 'ScrewAttack', difficulty=easy),
                                        haveItem(items, 'Plasma', difficulty=easy)),
                                    wor(canFly(items),
                                        wand(haveItem(items, 'HiJump'),
                                             knowsExitPlasmaRoomHiJump),
                                        wand(haveItem(items, 'SpeedBooster'),
                                             knowsShortCharge)))
},
{
    'Area': "Maridia",
    'Name': "Reserve Tank, Maridia",
    'Class': "Major",
    'Address': 0x7C5E3,
    'Visibility': "Chozo",
    # DONE: this item can be taken without gravity, but it's super hard because of the quick sands...
    'Available': lambda items: wand(canAccessOuterMaridia(items),
                                    wor(haveItem(items, 'Gravity'),
                                        wand(canDoSuitlessMaridia(items),
                                             knowsSuitlessSandpit)))
},
{
    'Area': "Maridia",
    'Name': "Spring Ball",
    'Class': "Major",
    'Address': 0x7C6E5,
    'Visibility': "Chozo",
    # DONE: handle puyo clip and diagonal bomb jump
    # to access the spring ball you can either:
    #  -use the puyo clip with ice
    #  -use the grapple to destroy the block and then:
    #    -use high boots jump
    #    -fly (with space jump or diagonal bomb jump
    'Available': lambda items: wand(canAccessInnerMaridia(items),
                                    wor(wand(haveItem(items, 'Ice'),
                                             knowsPuyoClip),
                                        wand(haveItem(items, 'Grapple'),
                                             wor(canFlyDiagonally(items),
                                                 haveItem(items, 'HiJump')))))
},
{
    'Area': "Maridia",
    'Name': "Energy Tank, Botwoon",
    'Class': "Major",
    'Address': 0x7C755,
    'Visibility': "Visible",
    # DONE: difficulty already handled in the functions
    'Available': lambda items: canDefeatBotwoon(items)
},
{
    'Area': "Maridia",
    'Name': "Space Jump",
    'Class': "Major",
    'Address': 0x7C7A7,
    'Visibility': "Chozo",
    # DONE: difficulty already handled in the function,
    # we need to have access to the boss and enough stuff to kill him
    'Available': lambda items: wand(canDefeatDraygon(items),
                                    enoughStuffsDraygon(items)),
    'Pickup': lambda: beatBoss('Draygon')
},
{
    'Area': "Crateria",
    'Name': "Power Bomb (Crateria surface)",
    'Class': "Minor",
    'Address': 0x781CC,
    'Visibility': "Visible",
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    wor(haveItem(items, 'SpeedBooster'),
                                        canFly(items)))
},
{
    'Area': "Crateria",
    'Name': "Missile (outside Wrecked Ship bottom)",
    'Class': "Minor",
    'Address': 0x781E8,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (outside Wrecked Ship top)",
    'Class': "Minor",
    'Address': 0x781EE,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (outside Wrecked Ship middle)",
    'Class': "Minor",
    'Address': 0x781F4,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria moat)",
    'Class': "Minor",
    'Address': 0x78248,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria bottom)",
    'Class': "Minor",
    'Address': 0x783EE,
    'Visibility': "Visible",
    'Available': lambda items: canDestroyBombWalls(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria gauntlet right)",
    'Class': "Minor",
    'Address': 0x78464,
    'Visibility': "Visible",
    'Available': lambda items: wand(canEnterAndLeaveGauntlet(items),
                                    canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria gauntlet left)",
    'Class': "Minor",
    'Address': 0x7846A,
    'Visibility': "Visible",
    'Available': lambda items: wand(canEnterAndLeaveGauntlet(items),
                                    canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'Name': "Super Missile (Crateria)",
    'Class': "Minor",
    'Address': 0x78478,
    'Visibility': "Visible",
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    haveItem(items, 'SpeedBooster'),
                                    wor(wand(haveItem(items, 'Ice'),
                                             (True, easy)),
                                        wand(haveItem(items, 'ETank'),
                                             haveItem(items, 'Varia'),
                                             haveItem(items, 'Gravity'), difficulty=hardcore))) # hardcore dboost...
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria middle)",
    'Class': "Minor",
    'Address': 0x78486,
    'Visibility': "Visible",
    'Available': lambda items: canPassBombPassages(items)
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (green Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x784AC,
    'Visibility': "Chozo",
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Super Missile (pink Brinstar)",
    'Class': "Minor",
    'Address': 0x784E4,
    'Visibility': "Chozo",
    'Available': lambda items: wand(canPassBombPassages(items),
                                    haveItem(items, 'Super'))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar below super missile)",
    'Class': "Minor",
    'Address': 0x78518,
    'Visibility': "Visible",
    'Available': lambda items: wand(canPassBombPassages(items),
                                    canOpenRedDoors(items))
},
{
    'Area': "Brinstar",
    'Name': "Super Missile (green Brinstar top)",
    'Class': "Minor",
    'Address': 0x7851E,
    'Visibility': "Visible",
    'Available': lambda items: wand(wor(haveItem(items, 'SpeedBooster'),
                                        canDestroyBombWalls(items)),
                                    canOpenRedDoors(items),
                                    wor(haveItem(items, 'Morph'),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar behind missile)",
    'Class': "Minor",
    'Address': 0x78532,
    'Visibility': "Hidden",
    'Available': lambda items: wand(canPassBombPassages(items),
                                    canOpenRedDoors(items))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar behind reserve tank)",
    'Class': "Minor",
    'Address': 0x78538,
    'Visibility': "Visible",
    'Available': lambda items: wand(canDestroyBombWalls(items),
                                    canOpenRedDoors(items),
                                    haveItem(items, 'Morph'))
},
{
    'Area': "Brinstar",
    'Name': "Missile (pink Brinstar top)",
    'Class': "Minor",
    'Address': 0x78608,
    'Visibility': "Visible",
    'Available': lambda items: wor(wand(canDestroyBombWalls(items),
                                        canOpenRedDoors(items)),
                                   canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Missile (pink Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x7860E,
    'Visibility': "Visible",
    'Available': lambda items: wor(wand(canDestroyBombWalls(items),
                                        canOpenRedDoors(items)),
                                   canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (pink Brinstar)",
    'Class': "Minor",
    'Address': 0x7865C,
    'Visibility': "Visible",
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    haveItem(items, 'Super'))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar pipe)",
    'Class': "Minor",
    'Address': 0x78676,
    'Visibility': "Visible",
    'Available': lambda items: wor(wand(canPassBombPassages(items),
                                        canOpenGreenDoors(items)),
                                   canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (blue Brinstar)",
    'Class': "Minor",
    'Address': 0x7874C,
    'Visibility': "Visible",
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar middle)",
    'Address': 0x78798,
    'Class': "Minor",
    'Visibility': "Visible",
    'Available': lambda items: haveItem(items, 'Morph')
},
{
    'Area': "Brinstar",
    'Name': "Super Missile (green Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x787D0,
    'Visibility': "Visible",
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    canOpenGreenDoors(items))
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x78802,
    'Visibility': "Chozo",
    'Available': lambda items: haveItem(items, 'Morph')
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar top)",
    'Class': "Minor",
    'Address': 0x78836,
    'Visibility': "Visible",
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar behind missile)",
    'Class': "Minor",
    'Address': 0x7883C,
    'Visibility': "Hidden",
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (red Brinstar sidehopper room)",
    'Class': "Minor",
    'Address': 0x788CA,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (red Brinstar spike room)",
    'Class': "Minor",
    'Address': 0x7890E,
    'Visibility': "Chozo",
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Missile (red Brinstar spike room)",
    'Class': "Minor",
    'Address': 0x78914,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Missile (Kraid)",
    'Class': "Minor",
    'Address': 0x789EC,
    'Visibility': "Hidden",
    'Available': lambda items: wand(canAccessKraid(items),
                                    canUsePowerBombs(items))
},
{
    'Area': "Norfair",
    'Name': "Missile (lava room)",
    'Class': "Minor",
    'Address': 0x78AE4,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (below Ice Beam)",
    'Class': "Minor",
    'Address': 0x78B46,
    'Visibility': "Hidden",
    'Available': lambda items: wand(canAccessKraid(items),
                                    canUsePowerBombs(items),
                                    canHellRun(items))
},
{
    'Area': "Norfair",
    'Name': "Missile (above Crocomire)",
    'Class': "Minor",
    'Address': 0x78BC0,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessCrocomire(items),
                                    wor(canFly(items), haveItem(items, 'Grapple'),
                                        wand(haveItem(items, 'HiJump'),
                                             haveItem(items, 'SpeedBooster'))))
},
{
    'Area': "Norfair",
    'Name': "Missile (Hi-Jump Boots)",
    'Class': "Minor",
    'Address': 0x78BE6,
    'Visibility': "Visible",
    'Available': lambda items: canAccessRedBrinstar(items)
},
{
    'Area': "Norfair",
    'Name': "Energy Tank (Hi-Jump Boots)",
    'Class': "Minor",
    'Address': 0x78BEC,
    'Visibility': "Visible",
    'Available': lambda items: canAccessRedBrinstar(items)
},
{
    'Area': "Norfair",
    'Name': "Power Bomb (Crocomire)",
    'Class': "Minor",
    'Address': 0x78C04,
    'Visibility': "Visible",
    'Available': lambda items: canAccessCrocomire(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (below Crocomire)",
    'Class': "Minor",
    'Address': 0x78C14,
    'Visibility': "Visible",
    'Available': lambda items: canAccessCrocomire(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (Grapple Beam)",
    'Class': "Minor",
    'Address': 0x78C2A,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessCrocomire(items),
                                    wor(canFly(items), haveItem(items, 'Grapple'),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Norfair",
    'Name': "Missile (Norfair Reserve Tank)",
    'Class': "Minor",
    'Address': 0x78C44,
    'Visibility': "Hidden",
    'Available': lambda items: wand(canAccessHeatedNorfair(items),
                                    wor(canFly(items), haveItem(items, 'Grapple'),
                                        haveItem(items, 'HiJump')))
},
{
    'Area': "Norfair",
    'Name': "Missile (bubble Norfair green door)",
    'Class': "Minor",
    'Address': 0x78C52,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessHeatedNorfair(items),
                                    wor(canFly(items), haveItem(items, 'Grapple'),
                                        haveItem(items, 'HiJump')))
},
{
    'Area': "Norfair",
    'Name': "Missile (bubble Norfair)",
    'Class': "Minor",
    'Address': 0x78C66,
    'Visibility': "Visible",
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (Speed Booster)",
    'Class': "Minor",
    'Address': 0x78C74,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (Wave Beam)",
    'Class': "Minor",
    'Address': 0x78CBC,
    'Visibility': "Visible",
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (Gold Torizo)",
    'Class': "Minor",
    'Address': 0x78E6E,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessLowerNorfair(items),
                                    haveItem(items, 'SpaceJump'))
},
{
    'Area': "LowerNorfair",
    'Name': "Super Missile (Gold Torizo)",
    'Class': "Minor",
    'Address': 0x78E74,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessLowerNorfair(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (Mickey Mouse room)",
    'Class': "Minor",
    'Address': 0x78F30,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (lower Norfair above fire flea room)",
    'Class': "Minor",
    'Address': 0x78FCA,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Power Bomb (lower Norfair above fire flea room)",
    'Class': "Minor",
    'Address': 0x78FD2,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Power Bomb (Power Bombs of shame)",
    'Class': "Minor",
    'Address': 0x790C0,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (lower Norfair near Wave Beam)",
    'Class': "Minor",
    'Address': 0x79100,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "WreckedShip",
    'Name': "Missile (Wrecked Ship middle)",
    'Class': "Minor",
    'Address': 0x7C265,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "WreckedShip",
    'Name': "Missile (Gravity Suit)",
    'Class': "Minor",
    'Address': 0x7C2EF,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessWs(items),
                                    wor(haveItem(items, 'Varia'),
                                        energyReserveCountOk(items, 1)))
},
{
    'Area': "WreckedShip",
    'Name': "Missile (Wrecked Ship top)",
    'Class': "Minor",
    'Address': 0x7C319,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "WreckedShip",
    'Name': "Super Missile (Wrecked Ship left)",
    'Class': "Minor",
    'Address': 0x7C357,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (green Maridia shinespark)",
    'Class': "Minor",
    'Address': 0x7C437,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    canUsePowerBombs(items),
                                    haveItem(items, 'Gravity'),
                                    haveItem(items, 'SpeedBooster'))
},
{
    'Area': "Maridia",
    'Name': "Super Missile (green Maridia)",
    'Class': "Minor",
    'Address': 0x7C43D,
    'Visibility': "Visible",
    'Available': lambda items: canAccessOuterMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (green Maridia tatori)",
    'Class': "Minor",
    'Address': 0x7C483,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessOuterMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Super Missile (yellow Maridia)",
    'Class': "Minor",
    'Address': 0x7C4AF,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (yellow Maridia super missile)",
    'Class': "Minor",
    'Address': 0x7C4B5,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (yellow Maridia false wall)",
    'Class': "Minor",
    'Address': 0x7C533,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (left Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5DD,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (right Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5EB,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Power Bomb (right Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5F1,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessOuterMaridia(items),
                                    haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'Name': "Missile (pink Maridia)",
    'Address': 0x7C603,
    'Class': "Minor",
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessOuterMaridia(items),
                                    haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'Name': "Super Missile (pink Maridia)",
    'Class': "Minor",
    'Address': 0x7C609,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessOuterMaridia(items),
                                    haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'Name': "Missile (Draygon)",
    'Class': "Minor",
    'Address': 0x7C74D,
    'Visibility': "Hidden",
    'Available': lambda items: canDefeatBotwoon(items)
}
]

from parameters import Knows, Settings, easy, medium, hard, harder, hardcore, mania
# the canXXX functions
from helpers import canEnterAndLeaveGauntlet, wand, wor, haveItem, canOpenRedDoors
from helpers import canPassBombPassages, canDestroyBombWalls, canUsePowerBombs, SMBool
from helpers import canFly, canAccessRedBrinstar, energyReserveCountOk, canAccessKraid
from helpers import Bosses, enoughStuffsKraid, heatProof, energyReserveCountOk
from helpers import energyReserveCountOkHellRun, canAccessCrocomire, canAccessHeatedNorfair
from helpers import canPassWorstRoom, enoughStuffsRidley, canAccessLowerNorfair
from helpers import canAccessWs, enoughStuffsPhantoon, enoughStuffsDraygon
from helpers import canAccessOuterMaridia, canDefeatDraygon, canPassMtEverest
from helpers import canAccessInnerMaridia, canFlyDiagonally, canDefeatBotwoon
from helpers import canCrystalFlash, canOpenGreenDoors, canHellRun

from rom import RomPatches

# all the items locations with the prerequisites to access them

locations = [
{
    'Area': "Crateria",
    'Name': "Energy Tank, Gauntlet",
    'Class': "Major",
    'Address': 0x78264,
    'Visibility': "Visible",
    'Room': 'Gauntlet Energy Tank Room',
    # EXPLAINED: difficulty already handled in the canEnterAndLeaveGauntlet function
    'Available': lambda items: canEnterAndLeaveGauntlet(items)
},
{
    'Area': "Crateria",
    'Name': "Bomb",
    'Address': 0x78404,
    'Class': "Major",
    'Visibility': "Chozo",
    'Room': 'Bomb Torizo Room',
    # EXPLAINED: need to morph to enter Alcatraz. red door at Flyway.
    #            we may not have bombs or power bomb to get out of Alcatraz.
    'Available': lambda items: wand(haveItem(items, 'Morph'),
                                    canOpenRedDoors(items)),
    'PostAvailable': lambda items: wor(Knows.AlcatrazEscape,
                                       canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'Name': "Energy Tank, Terminator",
    'Class': "Major",
    'Address': 0x78432,
    'Visibility': "Visible",
    'Room': 'Terminator Room',
    'Available': lambda items: wor(wand(haveItem(items, 'SpeedBooster'), Knows.SimpleShortCharge), 
                                   canDestroyBombWalls(items))
},
{
    'Area': "Brinstar",
    'Name': "Reserve Tank, Brinstar",
    'Class': "Major",
    'Address': 0x7852C,
    'Visibility': "Chozo",
    'Room': 'Brinstar Reserve Tank Room',
    # EXPLAINED: break the bomb wall at left of Parlor and Alcatraz,
    #            open red door at Green Brinstar Main Shaft,
    #            mock ball for early retreval or speed booster
    'Available': lambda items: wand(wor(haveItem(items, 'SpeedBooster'),
                                        canDestroyBombWalls(items)),
                                    canOpenRedDoors(items),
                                    wor(wand(Knows.Mockball,
                                             haveItem(items, 'Morph')),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'Name': "Charge Beam",
    'Class': "Major",
    'Address': 0x78614,
    'Visibility': "Chozo",
    'Room': 'Big Pink',
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
    'Room': 'Morph Ball Room',
    # EXPLAINED: no difficulty
    'Available': lambda items: SMBool(True, 0)
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Brinstar Ceiling",
    'Class': "Major",
    'Address': 0x7879E,
    'Visibility': "Hidden",
    'Room': 'Blue Brinstar Energy Tank Room',
    # EXPLAINED: to get this major item the different technics are:
    #  -can fly (continuous bomb jump or space jump)
    #  -have the high jump boots
    #  -freeze the Reo to jump on it
    #  -do a damage boost with one of the two Geemers
    'Available': lambda items: wand(wor(canOpenRedDoors(items), RomPatches.has(RomPatches.BlueBrinstarBlueDoor)),
                                    wor(Knows.CeilingDBoost,
                                        canFly(items),
                                        haveItem(items, 'HiJump'),
                                        haveItem(items, 'Ice')))
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Etecoons",
    'Class': "Major",
    'Address': 0x787C2,
    'Visibility': "Visible",
    'Room': 'Etecoon Energy Tank Room',
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
    'Room': 'Waterway Energy Tank Room',
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
                                        Knows.SimpleShortCharge))
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Brinstar Gate",
    'Class': "Major",
    'Address': 0x78824,
    'Visibility': "Visible",
    'Room': 'Hopper Energy Tank Room',
    # DONE: use Knows.ReverseGateGlitch
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    wor(haveItem(items, 'Wave'),
                                        wand(haveItem(items, 'Super'),
                                             haveItem(items, 'HiJump'),
                                             Knows.ReverseGateGlitch),
                                        wand(haveItem(items, 'Super'),
                                             Knows.ReverseGateGlitchHiJumpLess)))
},
{
    'Area': "Brinstar",
    'Name': "X-Ray Scope",
    'Class': "Major",
    'Address': 0x78876,
    'Visibility': "Chozo",
    'Room': 'X-Ray Scope Room',
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    canUsePowerBombs(items),
                                    wor(wor(haveItem(items, 'Grapple'),
                                            haveItem(items, 'SpaceJump')),
                                        wand(haveItem(items, 'Varia'),
                                             energyReserveCountOk(items, 4),
                                             Knows.XrayDboost),
                                        wand(energyReserveCountOk(items, 6),
                                             Knows.XrayDboost),
                                        wand(haveItem(items, 'Ice'),
                                             Knows.XrayIce,
                                             wor(energyReserveCountOk(items, 6),
                                                 wand(haveItem(items, 'Varia'),
                                                      energyReserveCountOk(items, 4))))))
},
{
    'Area': "Brinstar",
    'Name': "Spazer",
    'Class': "Major",
    'Address': 0x7896E,
    'Visibility': "Chozo",
    'Room': 'Spazer Room',
    # DONE: no difficulty
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    wor(canPassBombPassages(items), RomPatches.has(RomPatches.SpazerShotBlock)))
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Kraid",
    'Class': "Major",
    'Address': 0x7899C,
    'Visibility': "Hidden",
    'Room': 'Warehouse Energy Tank Room',
    # DONE: no difficulty
    'Available': lambda items: wand(canAccessKraid(items), Bosses.bossDead('Kraid'))
},
{
    'Area': "Brinstar",
    'Name': "Varia Suit",
    'Class': "Major",
    'Address': 0x78ACA,
    'Visibility': "Chozo",
    'Room': 'Varia Suit Room',
    # DONE: no difficulty
    'Available': lambda items: wand(canAccessKraid(items),
                                    enoughStuffsKraid(items)),
    'Pickup': lambda: Bosses.beatBoss('Kraid')
},
{
    'Area': "Norfair",
    'Name': "Ice Beam",
    'Class': "Major",
    'Address': 0x78B24,
    'Visibility': "Chozo",
    'Room': 'Ice Beam Room',
    # DONE: harder without varia
    'Available': lambda items: wand(canAccessKraid(items),
                                    canHellRun(items, 'Ice'),
                                    wor(wand(haveItem(items, 'Morph'),
                                             Knows.Mockball),
                                        haveItem(items, 'SpeedBooster'))) # FIXME : Knows.EarlyKraid has nothing to do with this and is implied by canAccessKraid
},
{
    'Area': "Norfair",
    'Name': "Energy Tank, Crocomire",
    'Class': "Major",
    'Address': 0x78BA4,
    'Visibility': "Visible",
    'Room': "Crocomire's Room",
    # DONE: difficulty already set in canHellRun
    'Available': lambda items: canAccessCrocomire(items)
},
{
    'Area': "Norfair",
    'Name': "Hi-Jump Boots",
    'Class': "Major",
    'Address': 0x78BAC,
    'Visibility': "Chozo",
    'Room': 'Hi Jump Boots Room',
    # DONE: no difficulty
    'Available': lambda items: canAccessRedBrinstar(items),
    'PostAvailable': lambda items: wor(canPassBombPassages(items),
                                       RomPatches.has(RomPatches.HiJumpShotBlock))
},
{
    'Area': "Norfair",
    'Name': "Grapple Beam",
    'Class': "Major",
    'Address': 0x78C36,
    'Visibility': "Chozo",
    'Room': 'Grapple Beam Room',
    'Available': lambda items: wand(canAccessCrocomire(items),
                                    wor(canFly(items),
                                        wand(haveItem(items, 'Ice'),
                                             Knows.ClimbToGrappleWithIce),
                                        haveItem(items, 'SpeedBooster'),
                                        Knows.GreenGateGlitch))
},
{
    'Area': "Norfair",
    'Name': "Reserve Tank, Norfair",
    'Class': "Major",
    'Address': 0x78C3E,
    'Visibility': "Chozo",
    'Room': 'Norfair Reserve Tank Room',
    'Available': lambda items: wand(canAccessHeatedNorfair(items),
                                    wor(wor(canFly(items),
                                            haveItem(items, 'Grapple'),
                                            wand(haveItem(items, 'HiJump'),
                                                 Knows.GetAroundWallJump)),
                                        wor(wand(haveItem(items, 'Ice'),
                                                 Knows.NorfairReserveIce),
                                            wand(haveItem(items, 'SpringBall'),
                                                 Knows.SpringBallJumpFromWall))))
},
{
    'Area': "Norfair",
    'Name': "Speed Booster",
    'Class': "Major",
    'Address': 0x78C82,
    'Visibility': "Chozo",
    'Room': 'Speed Booster Room',
    # DONE: difficulty already done in the function
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Wave Beam",
    'Class': "Major",
    'Address': 0x78CCA,
    'Visibility': "Chozo",
    'Room': 'Wave Beam Room',
    # DONE: this one is not easy without grapple beam nor space jump,
    #       with hijump medium wall jump is required
    'Available': lambda items: wand(canAccessHeatedNorfair(items),
                                    wor(haveItem(items, 'Grapple'),
                                        haveItem(items, 'SpaceJump'),
                                        Knows.WaveBeamWallJump))
},
{
    'Area': "LowerNorfair",
    'Name': "Energy Tank, Ridley",
    'Class': "Major",
    'Address': 0x79108,
    'Visibility': "Hidden",
    'Room': 'Ridley Tank Room',
    # DONE: already set in function
    'Available': lambda items: wand(canPassWorstRoom(items),
                                    enoughStuffsRidley(items)),
    'Pickup': lambda: Bosses.beatBoss('Ridley')
},
{
    'Area': "LowerNorfair",
    'Name': "Screw Attack",
    'Class': "Major",
    'Address': 0x79110,
    'Visibility': "Chozo",
    'Room': 'Screw Attack Room',
    # DONE: easy with green gate glitch
    'Available': lambda items: wand(canAccessLowerNorfair(items),
                                    wor(haveItem(items, 'SpaceJump'),
                                        Knows.GreenGateGlitch)),
    'PostAvailable': lambda items: wor(canFly(items),
                                       wand(haveItem(items, 'HiJump'),
                                            haveItem(items, 'ScrewAttack'),
                                            haveItem(items, 'SpeedBooster'),
                                            Knows.ScrewAttackExit),
                                       wand(haveItem(items, 'SpringBall'), Knows.SpringBallJumpFromWall))
},
{
    'Area': "LowerNorfair",
    'Name': "Energy Tank, Firefleas",
    'Class': "Major",
    'Address': 0x79184,
    'Visibility': "Visible",
    'Room': 'Lower Norfair Fireflea Room',
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "WreckedShip",
    'Name': "Reserve Tank, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C2E9,
    'Visibility': "Chozo",
    'Room': 'Bowling Alley',
    # DONE: easy
    'Available': lambda items: wand(canAccessWs(items),
                                    haveItem(items, 'SpeedBooster'),
                                    wor(haveItem(items, 'Varia'),
                                        energyReserveCountOk(items, 1)),
                                    Bosses.bossDead('Phantoon'))
},
{
    'Area': "WreckedShip",
    'Name': "Energy Tank, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C337,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship Energy Tank Room',
    'Available': lambda items: wand(canAccessWs(items),
                                    Bosses.bossDead('Phantoon'),
                                    wor(wand(wor(haveItem(items, 'Bomb'),
                                                 haveItem(items, 'PowerBomb')),
                                             Knows.SpongeBathBombJump),
                                        wand(haveItem(items, 'HiJump'),
                                             Knows.SpongeBathHiJump),
                                        wor(haveItem(items, 'SpaceJump', difficulty=easy),
                                            wand(haveItem(items, 'SpeedBooster'),
                                                 Knows.SpongeBathSpeed),
                                            wand(haveItem(items, 'SpringBall'),
                                                 Knows.SpringBallJump))))
},
{
    'Area': "WreckedShip",
    'Name': "Right Super, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C365,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship East Super Room',
    # DONE: easy once WS is accessible
    'Available': lambda items: wand(canAccessWs(items),
                                    enoughStuffsPhantoon(items)),
    'Pickup': lambda: Bosses.beatBoss('Phantoon')
},
{
    'Area': "WreckedShip",
    'Name': "Gravity Suit",
    'Class': "Major",
    'Address': 0x7C36D,
    'Visibility': "Chozo",
    'Room': 'Gravity Suit Room',
    # DONE: easy
    'Available': lambda items: wand(canAccessWs(items),
                                    Bosses.bossDead('Phantoon'),
                                    wor(haveItem(items, 'Varia'),
                                        energyReserveCountOk(items, 1)))
},
{
    'Area': "Maridia",
    'Name': "Energy Tank, Mama turtle",
    'Class': "Major",
    'Address': 0x7C47D,
    'Visibility': "Visible",
    'Room': 'Mama Turtle Room',
    # DONE: difficulty already handled in canAccessOuterMaridia
    # to acces the ETank in higher part of the room:
    #  -use grapple to attach to the block
    #  -use speedbooster ??
    #  -can fly (space jump or infinite bomb jump)
    'Available': lambda items: wand(canAccessOuterMaridia(items),
                                    wor(canFly(items),
                                        wand(haveItem(items, 'Gravity'), haveItem(items, 'SpeedBooster')),
                                        wand(haveItem(items, 'HiJump'), haveItem(items, 'SpringBall'), Knows.SpringBallJump),
                                        wand(haveItem(items, 'Grapple'),
                                             wor(haveItem(items, 'HiJump'), Knows.MamaGrappleWithWallJump))))
},
{
    'Area': "Maridia",
    'Name': "Plasma Beam",
    'Class': "Major",
    'Address': 0x7C559,
    'Visibility': "Chozo",
    'Room': 'Plasma Room',
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
                                    Bosses.bossDead('Draygon')),
    'PostAvailable': lambda items: wand(wor(wand(haveItem(items, 'SpeedBooster'),
                                                 Knows.ShortCharge,
                                                 Knows.KillPlasmaPiratesWithSpark),
                                            wand(haveItem(items, 'Charge'),
                                                 Knows.KillPlasmaPiratesWithCharge),
                                            haveItem(items, 'ScrewAttack', difficulty=easy),
                                            haveItem(items, 'Plasma', difficulty=easy)),
                                        wor(canFly(items),
                                            wand(haveItem(items, 'HiJump'),
                                                 Knows.GetAroundWallJump),
                                            wand(haveItem(items, 'SpeedBooster'),
                                                 Knows.ShortCharge)))
},
{
    'Area': "Maridia",
    'Name': "Reserve Tank, Maridia",
    'Class': "Major",
    'Address': 0x7C5E3,
    'Visibility': "Chozo",
    'Room': 'West Sand Hole',
    # DONE: this item can be taken without gravity, but it's super hard because of the quick sands...
    'Available': lambda items: wand(canPassMtEverest(items),
                                    wor(haveItem(items, 'Gravity'),
                                        Knows.SuitlessSandpit)) # suitless maridia conditions are in canPassMtEverest
},
{
    'Area': "Maridia",
    'Name': "Spring Ball",
    'Class': "Major",
    'Address': 0x7C6E5,
    'Visibility': "Chozo",
    'Room': 'Spring Ball Room',
    # DONE: handle puyo clip and diagonal bomb jump
    # to access the spring ball you can either:
    #  -use the puyo clip with ice
    #  -use the grapple to destroy the block and then:
    #    -use high boots jump
    #    -fly (with space jump or diagonal bomb jump
    'Available': lambda items: wand(canAccessInnerMaridia(items),
                                    wor(wand(haveItem(items, 'Ice'),
                                             Knows.PuyoClip),
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
    'Room': 'Botwoon Energy Tank Room',
    # DONE: difficulty already handled in the functions
    'Available': lambda items: canDefeatBotwoon(items)
},
{
    'Area': "Maridia",
    'Name': "Space Jump",
    'Class': "Major",
    'Address': 0x7C7A7,
    'Visibility': "Chozo",
    'Room': 'Space Jump Room',
    # DONE: difficulty already handled in the function,
    # we need to have access to the boss and enough stuff to kill him.
    # to get out of draygon room:
    #   with gravity but without highjump/bomb/space jump: gravity jump
    #   dessyreqt randomizer in machosist can have suitless draygon:
    #     to exit draygon room: grapple or crystal flash (for free shine spark)
    #     to exit precious room: spring ball jump, xray scope glitch or stored spark
    'Available': lambda items: wand(canDefeatDraygon(items),
                                    enoughStuffsDraygon(items)),
    'Pickup': lambda: Bosses.beatBoss('Draygon'),
    'PostAvailable': lambda items: wor(wand(haveItem(items, 'Gravity'),
                                            wor(canFly(items),
                                                Knows.GravityJump,
                                                wand(haveItem(items, 'HiJump'),
                                                     haveItem(items, 'SpeedBooster')))),
                                       wand(wand(canCrystalFlash(items),
                                                 Knows.DraygonRoomCrystalFlash),
                                            # use the spark either to exit draygon room or precious room
                                            wor(wand(haveItem(items, 'Grapple'),
                                                     Knows.DraygonRoomGrappleExit),
                                                wand(haveItem(items, 'XRayScope'),
                                                     Knows.PreciousRoomXRayExit),
                                                wand(haveItem(items, 'SpringBall'),
                                                     Knows.SpringBallJump))),
                                       # spark-less exit (no CF)
                                       wand(wand(haveItem(items, 'Grapple'),
                                                 Knows.DraygonRoomGrappleExit),
                                            wor(wand(haveItem(items, 'XRayScope'),
                                                     Knows.PreciousRoomXRayExit),
                                                wand(haveItem(items, 'SpringBall'),
                                                     Knows.SpringBallJump))))
},
{
    'Area': "Crateria",
    'Name': "Power Bomb (Crateria surface)",
    'Class': "Minor",
    'Address': 0x781CC,
    'Visibility': "Visible",
    'Room': 'Crateria Power Bomb Room',
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
    'Room': 'West Ocean',
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (outside Wrecked Ship top)",
    'Class': "Minor",
    'Address': 0x781EE,
    'Visibility': "Hidden",
    'Room': 'West Ocean',
    'Available': lambda items: wand(canAccessWs(items), Bosses.bossDead('Phantoon'))
},
{
    'Area': "Crateria",
    'Name': "Missile (outside Wrecked Ship middle)",
    'Class': "Minor",
    'Address': 0x781F4,
    'Visibility': "Visible",
    'Room': 'West Ocean',
    'Available': lambda items: wand(canAccessWs(items), Bosses.bossDead('Phantoon'))
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria moat)",
    'Class': "Minor",
    'Address': 0x78248,
    'Visibility': "Visible",
    'Room': 'The Moat',
    # it's before actual wrecked ship access
    'Available': lambda items: wand(haveItem(items, 'Super'),
                                    haveItem(items, 'PowerBomb'))
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria bottom)",
    'Class': "Minor",
    'Address': 0x783EE,
    'Visibility': "Visible",
    'Room': 'Pit Room',
    'Available': lambda items: canDestroyBombWalls(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria gauntlet right)",
    'Class': "Minor",
    'Address': 0x78464,
    'Visibility': "Visible",
    'Room': 'Green Pirates Shaft',
    'Available': lambda items: wand(canEnterAndLeaveGauntlet(items),
                                    canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria gauntlet left)",
    'Class': "Minor",
    'Address': 0x7846A,
    'Visibility': "Visible",
    'Room': 'Green Pirates Shaft',
    'Available': lambda items: wand(canEnterAndLeaveGauntlet(items),
                                    canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'Name': "Super Missile (Crateria)",
    'Class': "Minor",
    'Address': 0x78478,
    'Visibility': "Visible",
    'Room': 'Crateria Super Room',
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    haveItem(items, 'SpeedBooster'),
                                    wor(haveItem(items, 'Ice'),
                                        Knows.ShortCharge))
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria middle)",
    'Class': "Minor",
    'Address': 0x78486,
    'Visibility': "Visible",
    'Room': 'The Final Missile',
    'Available': lambda items: canPassBombPassages(items)
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (green Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x784AC,
    'Visibility': "Chozo",
    'Room': 'Green Brinstar Main Shaft',
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Super Missile (pink Brinstar)",
    'Class': "Minor",
    'Address': 0x784E4,
    'Visibility': "Chozo",
    'Room': 'Spore Spawn Super Room',
    # brinstar access, and
    # either you go the back way, using a super and the camera glitch,
    # or just beat spore spawn (so no Knows* setting needed for the glitch)
    'Available': lambda items: wand(wor(haveItem(items, 'SpeedBooster'),
                                        canDestroyBombWalls(items)),
                                    canOpenRedDoors(items),
                                    wor(wand(canPassBombPassages(items),
                                             haveItem(items, 'Super')),
                                        SMBool(True, easy)))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar below super missile)",
    'Class': "Minor",
    'Address': 0x78518,
    'Visibility': "Visible",
    'Room': 'Early Supers Room',
    'Available': lambda items: wand(canPassBombPassages(items),
                                    canOpenRedDoors(items))
},
{
    'Area': "Brinstar",
    'Name': "Super Missile (green Brinstar top)",
    'Class': "Minor",
    'Address': 0x7851E,
    'Visibility': "Visible",
    'Room': 'Early Supers Room',
    'Available': lambda items: wand(wor(haveItem(items, 'SpeedBooster'),
                                        canDestroyBombWalls(items)),
                                    canOpenRedDoors(items),
                                    wor(wand(haveItem(items, 'Morph'), Knows.Mockball),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar behind missile)",
    'Class': "Minor",
    'Address': 0x78532,
    'Visibility': "Hidden",
    'Room': 'Brinstar Reserve Tank Room',
    'Available': lambda items: wand(canPassBombPassages(items),
                                    canOpenRedDoors(items),
                                    wor(wand(haveItem(items, 'Morph'), Knows.Mockball),
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar behind reserve tank)",
    'Class': "Minor",
    'Address': 0x78538,
    'Visibility': "Visible",
    'Room': 'Brinstar Reserve Tank Room',
    # TODO::condition is weird, morph is required
    'Available': lambda items: wand(wor(haveItem(items, 'SpeedBooster'),
                                        canDestroyBombWalls(items)),
                                    canOpenRedDoors(items),
                                    haveItem(items, 'Morph'),
                                    wor(Knows.Mockball,
                                        haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'Name': "Missile (pink Brinstar top)",
    'Class': "Minor",
    'Address': 0x78608,
    'Visibility': "Visible",
    'Room': 'Big Pink',
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
    'Room': 'Big Pink',
    'Available': lambda items: wor(wand(wor(haveItem(items, 'SpeedBooster'),
                                            canDestroyBombWalls(items)),
                                        canOpenRedDoors(items)),
                                   canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (pink Brinstar)",
    'Class': "Minor",
    'Address': 0x7865C,
    'Visibility': "Visible",
    'Room': 'Pink Brinstar Power Bomb Room',
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    haveItem(items, 'Super'))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar pipe)",
    'Class': "Minor",
    'Address': 0x78676,
    'Visibility': "Visible",
    'Room': 'Green Hill Zone',
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
    'Room': 'Morph Ball Room',
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar middle)",
    'Address': 0x78798,
    'Class': "Minor",
    'Visibility': "Visible",
    'Room': 'Blue Brinstar Energy Tank Room',
    'Available': lambda items: wand(wor(haveItem(items, 'Morph'), RomPatches.has(RomPatches.BlueBrinstarMissile)),
                                    wor(canOpenRedDoors(items),
                                        RomPatches.has(RomPatches.BlueBrinstarBlueDoor)))
},
{
    'Area': "Brinstar",
    'Name': "Super Missile (green Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x787D0,
    'Visibility': "Visible",
    'Room': 'Etecoon Super Room',
    'Available': lambda items: wand(canUsePowerBombs(items),
                                    canOpenGreenDoors(items))
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x78802,
    'Visibility': "Chozo",
    'Room': 'First Missile Room',
    'Available': lambda items: haveItem(items, 'Morph')
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar top)",
    'Class': "Minor",
    'Address': 0x78836,
    'Visibility': "Visible",
    'Room': 'Billy Mays Room',
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar behind missile)",
    'Class': "Minor",
    'Address': 0x7883C,
    'Visibility': "Hidden",
    'Room': 'Billy Mays Room',
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (red Brinstar sidehopper room)",
    'Class': "Minor",
    'Address': 0x788CA,
    'Visibility': "Visible",
    'Room': 'Beta Power Bomb Room',
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (red Brinstar spike room)",
    'Class': "Minor",
    'Address': 0x7890E,
    'Visibility': "Chozo",
    'Room': 'Alpha Power Bomb Room',
    # can access from red brinstar lower or upper
    # from upper: power bomb
    # from lower: ice or screw or climb red tower
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    wor(canUsePowerBombs(items),
                                        Knows.RedTowerClimb,
                                        haveItem(items, 'Ice'),
                                        haveItem(items, 'SpaceJump')))
},
{
    'Area': "Brinstar",
    'Name': "Missile (red Brinstar spike room)",
    'Class': "Minor",
    'Address': 0x78914,
    'Visibility': "Visible",
    'Room': 'Alpha Power Bomb Room',
    # same as "Power Bomb (red Brinstar spike room)"
    'Available': lambda items: wand(canAccessRedBrinstar(items),
                                    wor(canUsePowerBombs(items),
                                        Knows.RedTowerClimb,
                                        haveItem(items, 'Ice'),
                                        haveItem(items, 'SpaceJump')))
},
{
    'Area': "Brinstar",
    'Name': "Missile (Kraid)",
    'Class': "Minor",
    'Address': 0x789EC,
    'Visibility': "Hidden",
    'Room': 'Warehouse Keyhunter Room',
    'Available': lambda items: wand(canAccessKraid(items),
                                    canUsePowerBombs(items))
},
{
    'Area': "Norfair",
    'Name': "Missile (lava room)",
    'Class': "Minor",
    'Address': 0x78AE4,
    'Visibility': "Hidden",
    'Room': 'Cathedral',
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (below Ice Beam)",
    'Class': "Minor",
    'Address': 0x78B46,
    'Visibility': "Hidden",
    'Room': 'Crumble Shaft',
    'Available': lambda items: wand(canAccessKraid(items),
                                    canUsePowerBombs(items),
                                    canHellRun(items, 'Ice'))
},
{
    'Area': "Norfair",
    'Name': "Missile (above Crocomire)",
    'Class': "Minor",
    'Address': 0x78BC0,
    'Visibility': "Visible",
    'Room': 'Crocomire Escape',
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
    'Room': 'Hi Jump Energy Tank Room',
    'Available': lambda items: canAccessRedBrinstar(items),
    'PostAvailable': lambda items: wor(canPassBombPassages(items),
                                       RomPatches.has(RomPatches.HiJumpShotBlock))
},
{
    'Area': "Norfair",
    'Name': "Energy Tank (Hi-Jump Boots)",
    'Class': "Minor",
    'Address': 0x78BEC,
    'Visibility': "Visible",
    'Room': 'Hi Jump Energy Tank Room',
    'Available': lambda items: canAccessRedBrinstar(items)
},
{
    'Area': "Norfair",
    'Name': "Power Bomb (Crocomire)",
    'Class': "Minor",
    'Address': 0x78C04,
    'Visibility': "Visible",
    'Room': 'Post Crocomire Power Bomb Room',
    'Available': lambda items: wand(canAccessCrocomire(items),
                                    wor(canFly(items),
                                        haveItem(items, 'Grapple'),
                                        wand(haveItem(items, 'HiJump'),
                                             haveItem(items, 'SpeedBooster'))))

},
{
    'Area': "Norfair",
    'Name': "Missile (below Crocomire)",
    'Class': "Minor",
    'Address': 0x78C14,
    'Visibility': "Visible",
    'Room': 'Post Crocomire Missile Room',
    'Available': lambda items: canAccessCrocomire(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (Grapple Beam)",
    'Class': "Minor",
    'Address': 0x78C2A,
    'Visibility': "Visible",
    'Room': 'Post Crocomire Jump Room',
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
    'Room': 'Norfair Reserve Tank Room',
    'Available': lambda items: wand(canAccessHeatedNorfair(items),
                                    wor(canFly(items), haveItem(items, 'Grapple'),
                                        wand(haveItem(items, 'HiJump'), Knows.GetAroundWallJump)))
},
{
    'Area': "Norfair",
    'Name': "Missile (bubble Norfair green door)",
    'Class': "Minor",
    'Address': 0x78C52,
    'Visibility': "Visible",
    'Room': 'Green Bubbles Missile Room',
    'Available': lambda items: wand(canAccessHeatedNorfair(items),
                                    wor(canFly(items),
                                        haveItem(items, 'Grapple'),
                                        wand(haveItem(items, 'HiJump'), Knows.GetAroundWallJump)))
},
{
    'Area': "Norfair",
    'Name': "Missile (bubble Norfair)",
    'Class': "Minor",
    'Address': 0x78C66,
    'Visibility': "Visible",
    'Room': 'Bubble Mountain',
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (Speed Booster)",
    'Class': "Minor",
    'Address': 0x78C74,
    'Visibility': "Hidden",
    'Room': 'Speed Booster Hall',
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (Wave Beam)",
    'Class': "Minor",
    'Address': 0x78CBC,
    'Visibility': "Visible",
    'Room': 'Double Chamber',
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (Gold Torizo)",
    'Class': "Minor",
    'Address': 0x78E6E,
    'Visibility': "Visible",
    'Room': "Golden Torizo's Room",
    'Available': lambda items: wand(canAccessLowerNorfair(items),
                                    haveItem(items, 'SpaceJump'))
},
{
    'Area': "LowerNorfair",
    'Name': "Super Missile (Gold Torizo)",
    'Class': "Minor",
    'Address': 0x78E74,
    'Visibility': "Hidden",
    'Room': "Golden Torizo's Room",
    'Available': lambda items: wand(canAccessLowerNorfair(items),
                                    wor(haveItem(items, 'SpaceJump'),
                                        Knows.GreenGateGlitch))
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (Mickey Mouse room)",
    'Class': "Minor",
    'Address': 0x78F30,
    'Visibility': "Visible",
    'Room': 'Mickey Mouse Room',
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (lower Norfair above fire flea room)",
    'Class': "Minor",
    'Address': 0x78FCA,
    'Visibility': "Visible",
    'Room': 'Lower Norfair Spring Ball Maze Room',
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Power Bomb (lower Norfair above fire flea room)",
    'Class': "Minor",
    'Address': 0x78FD2,
    'Visibility': "Visible",
    'Room': 'Lower Norfair Escape Power Bomb Room',
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Power Bomb (Power Bombs of shame)",
    'Class': "Minor",
    'Address': 0x790C0,
    'Visibility': "Visible",
    'Room': 'Wasteland',
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (lower Norfair near Wave Beam)",
    'Class': "Minor",
    'Address': 0x79100,
    'Visibility': "Visible",
    'Room': "Three Muskateers' Room",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "WreckedShip",
    'Name': "Missile (Wrecked Ship middle)",
    'Class': "Minor",
    'Address': 0x7C265,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship Main Shaft',
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "WreckedShip",
    'Name': "Missile (Gravity Suit)",
    'Class': "Minor",
    'Address': 0x7C2EF,
    'Visibility': "Visible",
    'Room': 'Bowling Alley',
    'Available': lambda items: wand(canAccessWs(items),
                                    wor(haveItem(items, 'Varia'),
                                        energyReserveCountOk(items, 1)),
                                    Bosses.bossDead('Phantoon'))
},
{
    'Area': "WreckedShip",
    'Name': "Missile (Wrecked Ship top)",
    'Class': "Minor",
    'Address': 0x7C319,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship East Missile Room',
    'Available': lambda items: wand(canAccessWs(items), Bosses.bossDead('Phantoon'))
},
{
    'Area': "WreckedShip",
    'Name': "Super Missile (Wrecked Ship left)",
    'Class': "Minor",
    'Address': 0x7C357,
    'Visibility': "Visible",
    'Room': 'Wrecked Ship West Super Room',
    'Available': lambda items: wand(canAccessWs(items), Bosses.bossDead('Phantoon'))
},
{
    'Area': "Maridia",
    'Name': "Missile (green Maridia shinespark)",
    'Class': "Minor",
    'Address': 0x7C437,
    'Visibility': "Visible",
    'Room': 'Main Street',
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
    'Room': 'Main Street',
    'Available': lambda items: canAccessOuterMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (green Maridia tatori)",
    'Class': "Minor",
    'Address': 0x7C483,
    'Visibility': "Hidden",
    'Room': 'Mama Turtle Room',
    'Available': lambda items: canAccessOuterMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Super Missile (yellow Maridia)",
    'Class': "Minor",
    'Address': 0x7C4AF,
    'Visibility': "Visible",
    'Room': 'Watering Hole',
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (yellow Maridia super missile)",
    'Class': "Minor",
    'Address': 0x7C4B5,
    'Visibility': "Visible",
    'Room': 'Watering Hole',
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (yellow Maridia false wall)",
    'Class': "Minor",
    'Address': 0x7C533,
    'Visibility': "Visible",
    'Room': 'Pseudo Plasma Spark Room',
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (left Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5DD,
    'Visibility': "Visible",
    'Room': 'West Sand Hole',
    'Available': lambda items: wand(canAccessOuterMaridia(items),
                                    wor(haveItem(items, 'Gravity'),
                                        Knows.SuitlessSandpit))
},
{
    'Area': "Maridia",
    'Name': "Missile (right Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5EB,
    'Visibility': "Visible",
    'Room': 'East Sand Hole',
    'Available': lambda items: wand(canAccessOuterMaridia(items),
                                    wor(haveItem(items, 'Gravity'),
                                        Knows.SuitlessSandpit))
},
{
    'Area': "Maridia",
    'Name': "Power Bomb (right Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5F1,
    'Visibility': "Visible",
    'Room': 'East Sand Hole',
    'Available': lambda items: wand(canAccessOuterMaridia(items),
                                    haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'Name': "Missile (pink Maridia)",
    'Address': 0x7C603,
    'Class': "Minor",
    'Visibility': "Visible",
    'Room': 'Aqueduct',
    'Available': lambda items: wand(canPassMtEverest(items),
                                    haveItem(items, 'SpeedBooster'), # TODO FLO find trick to get this without speed booster and add knows
                                    haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'Name': "Super Missile (pink Maridia)",
    'Class': "Minor",
    'Address': 0x7C609,
    'Visibility': "Visible",
    'Room': 'Aqueduct',
    'Available': lambda items: wand(canPassMtEverest(items),
                                    haveItem(items, 'SpeedBooster'), # TODO FLO find trick to get this without speed booster and add knows
                                    haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'Name': "Missile (Draygon)",
    'Class': "Minor",
    'Address': 0x7C74D,
    'Visibility': "Hidden",
    'Room': 'The Precious Room',
    'Available': lambda items: canDefeatBotwoon(items)
}
]

from functools import reduce

# the difficulties for each technics
from smbool import SMBool
from rom import RomPatches
from helpers import Helpers, Bosses

class HelpersGraph(Helpers):
    def __init__(self, smbm):
        self.smbm = smbm
        # cacheable functions sorted to avoid dependencies
        self.cachedMethods = ['canUseBombs', 'canOpenYellowDoors', 'canUsePowerBombs',
                              'canPassBombPassages', 'canOpenRedDoors', 'heatProof', 'canFly',
                              'canOpenGreenDoors', 'canEnterAndLeaveGauntlet',
                              'enoughStuffCroc', 'canDoSuitlessOuterMaridia', 'canDoSuitlessMaridia',
                              'canPassMtEverest', 'canAccessBotwoonFromMainStreet',
                              'enoughStuffBotwoon', 'canAccessDraygonFromMainStreet',
                              'canPassLavaPit', 'canPassWorstRoom',
                              #'canAccessCrocFromNorfairEntrance',
                              'canEnterNorfairReserveArea',
                              'canPassSpongeBath', 'canPassMoat', 'canGoUpMtEverest']

    def canAccessKraidsLair(self):
        sm = self.smbm
        # EXPLAINED: access the upper right platform with either:
        #             -hijump boots (easy regular way)
        #             -fly (space jump or infinite bomb jump)
        #             -know how to wall jump on the platform without the hijump boots
        #            then we have to break a bomb block at Warehouse Zeela room
        return sm.wand(sm.canOpenGreenDoors(),
                       sm.wor(sm.haveItem('HiJump'),
                              sm.canFly(),
                              sm.knowsEarlyKraid()),
                       sm.canPassBombPassages())

    def canPassMoat(self):
        sm = self.smbm
        # EXPLAINED: In the Moat we can either:
        #             -use grapple or space jump (easy way)
        #             -do a continuous wall jump (https://www.youtube.com/watch?v=4HVhTwwax6g)
        #             -do a diagonal bomb jump from the middle platform (https://www.youtube.com/watch?v=5NRqQ7RbK3A&t=10m58s)
        #             -do a short charge from the Keyhunter room (https://www.youtube.com/watch?v=kFAYji2gFok)
        #             -do a gravity jump from below the right platform
        #             -do a mock ball and a bounce ball (https://www.youtube.com/watch?v=WYxtRF--834)
        return sm.wor(sm.wor(sm.haveItem('Grapple'),
                             sm.haveItem('SpaceJump'),
                             sm.knowsContinuousWallJump()),
                             sm.wor(sm.wand(sm.knowsDiagonalBombJump(), sm.canUseBombs()),
                                    sm.wand(sm.haveItem('SpeedBooster'),
                                            sm.wor(sm.knowsSimpleShortCharge(), sm.knowsShortCharge())),
                                    sm.wand(sm.knowsGravityJump(), sm.haveItem('Gravity')),
                                    sm.wand(sm.knowsMockballWs(), sm.haveItem('Morph'), sm.haveItem('SpringBall'))))

    def canPassMoatReverse(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Grapple'),
                      sm.haveItem('SpaceJump'),
                      sm.haveItem('Gravity'),
                      sm.wand(sm.haveItem('Morph'),
                              sm.wor(RomPatches.has(RomPatches.MoatShotBlock),
                                     sm.canPassBombPassages())))

    def canPassSpongeBath(self):
        sm = self.smbm
        return sm.wand(Bosses.bossDead('Phantoon'),
                       sm.wor(sm.wand(sm.canPassBombPassages(),
                                      sm.knowsSpongeBathBombJump()),
                              sm.wand(sm.haveItem('HiJump'),
                                      sm.knowsSpongeBathHiJump()),
                              sm.wor(sm.haveItem('Gravity'),
                                     sm.haveItem('SpaceJump'),
                                     sm.wand(sm.haveItem('SpeedBooster'),
                                             sm.knowsSpongeBathSpeed()),
                                     sm.wand(sm.haveItem('Morph'),
                                             sm.haveItem('SpringBall'),
                                             sm.knowsSpringBallJump()))))

    def canAccessEtecoons(self):
        sm = self.smbm
        return sm.wor(sm.canUsePowerBombs(),
                      sm.wand(sm.knowsMoondance(), sm.canUseBombs(), sm.canOpenRedDoors()))

    # the water zone east of WS
    def canPassForgottenHighway(self, fromWs):
        sm = self.smbm
        baseSuitLess = sm.wand(sm.haveItem('HiJump'),
                               sm.wor(sm.haveItem('Ice'),
                                      sm.wand(sm.haveItem('SpringBall'), sm.knowsSpringBallJump())),
                               sm.knowsGravLessLevel1())
        if fromWs is True:
            suitlessCondition = sm.wand(baseSuitLess, # to climb on the ledges
                                        sm.haveItem('SpaceJump')) # to go through the door on the right
        else:
            suitlessCondition = baseSuitLess

        return sm.wor(sm.haveItem('Gravity'),
                      suitlessCondition)

    def canExitCrabHole(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), # morph to exit the hole
                       sm.canOpenRedDoors(), # to exit and re-enter if needed
                       sm.wor(sm.wand(sm.haveItem('Gravity'), # even with gravity you need some way to climb...
                                      sm.wor(sm.haveItem('Ice'), # ...on crabs...
                                             sm.haveItem('HiJump'), # ...or by jumping
                                             sm.knowsGravityJump(),
                                             sm.canFly())),
                              sm.canDoSuitlessOuterMaridia())) # climing crabs

    def canPassMaridiaToRedTowerNode(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       sm.wor(RomPatches.has(RomPatches.AreaRandoGatesBase),
                              sm.canOpenGreenDoors()))

    def canPassRedTowerToMaridiaNode(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       RomPatches.has(RomPatches.AreaRandoGatesBase))

    def canGrappleEscape(self):
        sm = self.smbm
        return sm.wor(sm.wor(sm.haveItem('SpaceJump'),
                             sm.wand(sm.haveItem('Bomb'), # IBJ from lava...either have grav or freeze the enemy there
                                     sm.knowsInfiniteBombJump(),
                                     sm.wor(sm.haveItem('Gravity'),
                                            sm.haveItem('Ice')))),
                      sm.haveItem('Grapple'),
                      sm.wand(sm.haveItem('SpeedBooster'),
                              sm.wor(sm.haveItem('HiJump'), # jump from the blocks below
                                     sm.knowsShortCharge())), # spark from across the grapple blocks
                      sm.wand(sm.haveItem('SpringBall'), sm.haveItem('HiJump'), sm.knowsSpringBallJump())) # jump from the blocks below

    def canEnterNorfairReserveArea(self):
        sm = self.smbm
        return sm.wand(sm.canOpenGreenDoors(),
                       sm.wor(sm.wor(sm.canFly(),
                                     sm.haveItem('Grapple'),
                                     sm.wand(sm.haveItem('HiJump'),
                                             sm.knowsGetAroundWallJump())),
                              sm.wor(sm.haveItem('Ice'),
                                     sm.wand(sm.haveItem('SpringBall'),
                                             sm.knowsSpringBallJumpFromWall()))))

    def canPassLavaPit(self):
        sm = self.smbm
        nTanks4Dive = 3
        if sm.getBool(sm.heatProof()) == False:
            nTanks4Dive = 8
        return sm.wor(sm.wand(sm.haveItem('Gravity'), sm.haveItem('SpaceJump')),
                      sm.wand(sm.knowsGravityJump(), sm.haveItem('Gravity')),
                      sm.wand(sm.wor(sm.wand(sm.knowsLavaDive(), sm.haveItem('HiJump')),
                                     sm.knowsLavaDiveNoHiJump()),
                              sm.energyReserveCountOk(nTanks4Dive)))

    def canPassLowerNorfairChozo(self):
        sm = self.smbm
        return sm.wand(sm.canHellRun('LowerNorfair', 1.5), # 1.5 to require one more CF if no heat protection because of distance to cover, wait times, acid...
                       sm.canUsePowerBombs(),
                       sm.haveItem('Super'), # you'll have to exit screw attack area at some point
                       sm.wor(sm.haveItem('SpaceJump'),
                              RomPatches.has(RomPatches.LNChozoSJCheckDisabled)))


    def canPassWorstRoom(self):
        sm = self.smbm
        return sm.wand(sm.canDestroyBombWalls(),
                       sm.wor(sm.canFly(),
                              sm.wand(sm.knowsWorstRoomIceCharge(), sm.haveItem('Ice'), sm.haveItem('Charge')),
                              sm.wand(sm.knowsGetAroundWallJump(), sm.haveItem('HiJump')),
                              sm.wand(sm.knowsSpringBallJumpFromWall(), sm.haveItem('SpringBall'))))

    # go though the pirates room filled with acid
    def canPassAmphitheaterReverse(self):
        sm = self.smbm
        nTanks = 4
        if not sm.heatProof():
            nTanks = 16
        return sm.wand(sm.haveItem('Gravity'),
                       sm.energyReserveCountOk(nTanks))

    def canClimbRedTower(self):
        sm = self.smbm
        return sm.wor(sm.knowsRedTowerClimb(),
                      sm.haveItem('Ice'),
                      sm.haveItem('SpaceJump'))

    def canClimbBottomRedTower(self):
        sm = self.smbm
        return sm.wor(sm.wor(RomPatches.has(RomPatches.RedTowerLeftPassage),
                             sm.haveItem('HiJump'),
                             sm.haveItem('Ice'),
                             sm.canFly()),
                      sm.wand(sm.haveItem('SpeedBooster'), sm.knowsShortCharge()))

    def canGoUpMtEverest(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Gravity'),
                              sm.wor(sm.haveItem('Grapple'),
                                     sm.haveItem('SpeedBooster')),
                              sm.wor(sm.canFly(),
                                     sm.wand(sm.haveItem('HiJump'), sm.knowsGravityJump()))),
                      sm.wand(sm.canDoSuitlessOuterMaridia(),
                              sm.haveItem('Grapple')))

    def canPassMtEverest(self):
        sm = self.smbm
        return  sm.wor(sm.wand(sm.haveItem('Gravity'),
                               sm.wor(sm.wor(sm.haveItem('Grapple'),
                                             sm.haveItem('SpeedBooster')),
                                      sm.wor(sm.canFly(),
                                             sm.knowsGravityJump(),
                                             sm.wand(sm.haveItem('Ice'), sm.knowsTediousMountEverest())))),
                       sm.canDoSuitlessMaridia(),
                       sm.wand(sm.canDoSuitlessOuterMaridia(), sm.knowsTediousMountEverest()))

    def canDoSuitlessOuterMaridia(self):
        sm = self.smbm
        return sm.wand(sm.knowsGravLessLevel1(),
                       sm.haveItem('HiJump'),
                       sm.haveItem('Ice'))

    def canDoSuitlessMaridia(self):
        sm = self.smbm
        return sm.wand(sm.canDoSuitlessOuterMaridia(),
                       sm.haveItem('Grapple'))

    def canAccessBotwoonFromMainStreet(self):
        sm = self.smbm
        return sm.wand(sm.canPassMtEverest(),
                       sm.canOpenGreenDoors(),
                       sm.canUsePowerBombs())

    # from main street only
    def canDefeatBotwoon(self):
        sm = self.smbm
        # EXPLAINED: in Botwoon Hallway, either:
        #             -use regular speedbooster (with gravity)
        #             -do a mochtroidclip (https://www.youtube.com/watch?v=1z_TQu1Jf1I&t=20m28s)
        return sm.wand(sm.canAccessBotwoonFromMainStreet(),
                       sm.enoughStuffBotwoon(),
                       sm.wor(sm.wand(sm.haveItem('SpeedBooster'),
                                      sm.haveItem('Gravity')),
                              sm.wand(sm.knowsMochtroidClip(), sm.haveItem('Ice'))))

    def canAccessDraygonFromMainStreet(self):
        sm = self.smbm
        return sm.wand(sm.canDefeatBotwoon(),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.canDoSuitlessMaridia(), sm.knowsGravLessLevel2())))

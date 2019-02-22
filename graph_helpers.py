from functools import reduce

# the difficulties for each technics
from smbool import SMBool
from rom import RomPatches
from helpers import Helpers, Bosses
from cache import Cache
from math import ceil

class HelpersGraph(Helpers):
    def __init__(self, smbm):
        self.smbm = smbm

    @Cache.decorator
    def canAccessKraidsLair(self):
        sm = self.smbm
        # EXPLAINED: access the upper right platform with either:
        #             -hijump boots (easy regular way)
        #             -fly (space jump or infinite bomb jump)
        #             -know how to wall jump on the platform without the hijump boots
        return sm.wand(sm.canOpenGreenDoors(),
                       sm.wor(sm.haveItem('HiJump'),
                              sm.canFly(),
                              sm.knowsEarlyKraid()))

    @Cache.decorator
    def canPassMoat(self):
        sm = self.smbm
        # EXPLAINED: In the Moat we can either:
        #             -use grapple or space jump (easy way)
        #             -do a continuous wall jump (https://www.youtube.com/watch?v=4HVhTwwax6g)
        #             -do a diagonal bomb jump from the middle platform (https://www.youtube.com/watch?v=5NRqQ7RbK3A&t=10m58s)
        #             -do a short charge from the Keyhunter room (https://www.youtube.com/watch?v=kFAYji2gFok)
        #             -do a gravity jump from below the right platform
        #             -do a mock ball and a bounce ball (https://www.youtube.com/watch?v=WYxtRF--834)
        #             -with gravity, either hijump or IBJ
        return sm.wor(sm.wor(sm.haveItem('Grapple'),
                             sm.haveItem('SpaceJump'),
                             sm.knowsContinuousWallJump()),
                             sm.wor(sm.wand(sm.knowsDiagonalBombJump(), sm.canUseBombs()),
                                    sm.canSimpleShortCharge(),
                                    sm.wand(sm.haveItem('Gravity'),
                                            sm.wor(sm.knowsGravityJump(),
                                                   sm.haveItem('HiJump'),
                                                   sm.canInfiniteBombJump())),
                                    sm.wand(sm.knowsMockballWs(), sm.canUseSpringBall())))

    @Cache.decorator
    def canPassMoatReverse(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Grapple'),
                      sm.haveItem('SpaceJump'),
                      sm.haveItem('Gravity'),
                      sm.wand(sm.haveItem('Morph'),
                              sm.wor(RomPatches.has(RomPatches.MoatShotBlock),
                                     sm.canPassBombPassages())))

    @Cache.decorator
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
                                     sm.canSpringBallJump())))

    @Cache.decorator
    def canPassBowling(self):
        sm = self.smbm
        return sm.wand(Bosses.bossDead('Phantoon'),
                       sm.wor(sm.heatProof(),
                              sm.energyReserveCountOk(1),
                              sm.haveItem("SpaceJump"),
                              sm.haveItem("Grapple")))

    @Cache.decorator
    def canAccessEtecoons(self):
        sm = self.smbm
        return sm.wor(sm.canUsePowerBombs(),
                      sm.wand(sm.knowsMoondance(), sm.canUseBombs(), sm.canOpenRedDoors()))

    # the water zone east of WS
    def canPassForgottenHighway(self, fromWs):
        sm = self.smbm
        suitless = sm.canDoSuitlessOuterMaridia()
        if fromWs is True:
            suitless = sm.wand(suitless, # to climb on the ledges
                               sm.haveItem('SpaceJump')) # to go through the door on the right
        return sm.wand(sm.wor(sm.haveItem('Gravity'),
                              suitless),
                       sm.haveItem('Morph')) # for crab maze

    @Cache.decorator
    def canExitCrabHole(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), # morph to exit the hole
                       sm.wor(sm.wand(sm.haveItem('Gravity'), # even with gravity you need some way to climb...
                                      sm.wor(sm.haveItem('Ice'), # ...on crabs...
                                             sm.haveItem('HiJump'), # ...or by jumping
                                             sm.knowsGravityJump(),
                                             sm.canFly())),
                              sm.wand(sm.haveItem('Ice'), sm.canDoSuitlessOuterMaridia()))) # climbing crabs

    @Cache.decorator
    def canPassMaridiaToRedTowerNode(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       sm.wor(RomPatches.has(RomPatches.AreaRandoGatesBase),
                              sm.canOpenGreenDoors()))

    @Cache.decorator
    def canPassRedTowerToMaridiaNode(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       RomPatches.has(RomPatches.AreaRandoGatesBase))

    def canEnterCathedral(self, mult=1.0):
        sm = self.smbm
        return sm.wand(sm.canOpenRedDoors(),
                       sm.wor(sm.wand(sm.canHellRun('MainUpperNorfair', mult),
                                      sm.wor(sm.wor(RomPatches.has(RomPatches.CathedralEntranceWallJump),
                                                    sm.haveItem('HiJump'),
                                                    sm.canFly()),
                                             sm.wor(sm.haveItem('SpeedBooster'), # spark
                                                    sm.canSpringBallJump()))),
                              sm.wand(sm.canHellRun('MainUpperNorfair', 0.5*mult),
                                      sm.knowsNovaBoost())))

    @Cache.decorator
    def canExitCathedral(self):
        # from top: can use bomb/powerbomb jumps
        # from bottom: can do a shinespark or use space jump
        #              can do it with highjump + wall jump
        #              can do it with only two wall jumps (the first one is delayed like on alcatraz)
        #              can do it with a spring ball jump from wall
        sm = self.smbm
        return sm.wand(sm.wor(sm.canHellRun('MainUpperNorfair', 0.75),
                              sm.heatProof()),
                       sm.wor(sm.wor(sm.canPassBombPassages(),
                                     sm.haveItem("SpeedBooster")),
                              sm.wor(sm.haveItem("SpaceJump"),
                                     sm.haveItem("HiJump"),
                                     sm.knowsWallJumpCathedralExit(),
                                     sm.wand(sm.knowsSpringBallJumpFromWall(), sm.canUseSpringBall()))))

    @Cache.decorator
    def canGrappleEscape(self):
        sm = self.smbm
        return sm.wor(sm.wor(sm.haveItem('SpaceJump'),
                             sm.wand(sm.canInfiniteBombJump(), # IBJ from lava...either have grav or freeze the enemy there if hellrunning (otherwise single DBJ at the end)
                                     sm.wor(sm.heatProof(),
                                            sm.haveItem('Gravity'),
                                            sm.haveItem('Ice')))),
                      sm.haveItem('Grapple'),
                      sm.wand(sm.haveItem('SpeedBooster'),
                              sm.wor(sm.haveItem('HiJump'), # jump from the blocks below
                                     sm.knowsShortCharge())), # spark from across the grapple blocks
                      sm.wand(sm.haveItem('HiJump'), sm.canSpringBallJump())) # jump from the blocks below

    @Cache.decorator
    def canPassFrogSpeedwayRightToLeft(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('SpeedBooster'),
                      sm.wand(sm.knowsFrogSpeedwayWithoutSpeed(),
                              sm.haveItem('Wave'),
                              sm.wor(sm.haveItem('Spazer'),
                                     sm.haveItem('Plasma'))))

    @Cache.decorator
    def canEnterNorfairReserveArea(self):
        sm = self.smbm
        return sm.wand(sm.canOpenGreenDoors(),
                       sm.wor(sm.wor(sm.canFly(),
                                     sm.haveItem('Grapple'),
                                     sm.wand(sm.haveItem('HiJump'),
                                             sm.knowsGetAroundWallJump())),
                              sm.wor(sm.haveItem('Ice'),
                                     sm.wand(sm.canUseSpringBall(),
                                             sm.knowsSpringBallJumpFromWall()),
                                     sm.knowsNorfairReserveDBoost())))

    @Cache.decorator
    def canPassLavaPit(self):
        sm = self.smbm
        nTanks4Dive = 3
        if sm.heatProof().bool == False:
            nTanks4Dive = 8
        if sm.haveItem('HiJump').bool == False:
            nTanks4Dive = ceil(nTanks4Dive * 1.25) # 4 or 10
        return sm.wand(sm.wor(sm.wand(sm.haveItem('Gravity'), sm.haveItem('SpaceJump')),
                              sm.wand(sm.knowsGravityJump(), sm.haveItem('Gravity'), sm.wor(sm.haveItem('HiJump'), sm.knowsLavaDive())),
                              sm.wand(sm.wor(sm.wand(sm.knowsLavaDive(), sm.haveItem('HiJump')),
                                             sm.knowsLavaDiveNoHiJump()),
                                      sm.energyReserveCountOk(nTanks4Dive))),
                       sm.canUsePowerBombs()) # power bomb blocks left and right of LN entrance without any items before

    @Cache.decorator
    def canPassLavaPitReverse(self):
        sm = self.smbm
        nTanks = 2
        if sm.heatProof().bool == False:
            nTanks = 6
        return sm.energyReserveCountOk(nTanks)

    @Cache.decorator
    def canPassLowerNorfairChozo(self):
        sm = self.smbm
        return sm.wand(sm.canHellRun('LowerNorfair', 0.75), # 0.75 to require one more CF if no heat protection because of distance to cover, wait times, acid...
                       sm.canUsePowerBombs(),
                       sm.wor(sm.haveItem('SpaceJump'),
                              RomPatches.has(RomPatches.LNChozoSJCheckDisabled)))

    @Cache.decorator
    def canExitScrewAttackArea(self):
        sm = self.smbm

        return sm.wand(sm.canDestroyBombWalls(),
                       sm.wor(sm.canFly(),
                              sm.wand(sm.haveItem('HiJump'),
                                      sm.haveItem('ScrewAttack'),
                                      sm.haveItem('SpeedBooster'),
                                      sm.knowsScrewAttackExit()),
                              sm.wand(sm.canUseSpringBall(),
                                      sm.knowsSpringBallJumpFromWall()),
                              sm.wand(sm.canSimpleShortCharge(), # fight GT and spark out
                                      sm.enoughStuffGT())))

    @Cache.decorator
    def canPassWorstRoom(self):
        sm = self.smbm
        return sm.wand(sm.canDestroyBombWalls(),
                       sm.wor(sm.canFly(),
                              sm.wand(sm.knowsWorstRoomIceCharge(), sm.haveItem('Ice'), sm.haveItem('Charge')),
                              sm.wand(sm.knowsGetAroundWallJump(), sm.haveItem('HiJump')),
                              sm.wand(sm.knowsSpringBallJumpFromWall(), sm.canUseSpringBall())))

    @Cache.decorator
    def canPassThreeMuskateers(self):
        sm = self.smbm
        destroy = sm.wor(sm.haveItem('Plasma'),
                         sm.haveItem('ScrewAttack'),
                         sm.wand(sm.heatProof(), # this takes a loooong time ...
                                 sm.wor(sm.haveItem('Spazer'),
                                        sm.haveItem('Ice'))))
        if destroy.bool == True:
            return destroy
        # if no adapted beams or screw attack, check if we can go both ways
        # (no easy refill around) with supers and/or health

        # - super only?
        ki = 1800.0
        sup = 300.0
        nbKi = 6.0
        if sm.itemCount('Super')*5*sup >= nbKi*ki:
            return SMBool(True, 0, items=['Super'])

        # - or with taking damage as well?
        dmgKi = 200.0 / sm.getDmgReduction(False)
        if (sm.itemCount('Super')*5*sup)/ki + (sm.energyReserveCount()*100 - 2)/dmgKi >= nbKi:
            return sm.wand(sm.heatProof(), SMBool(True, 0, items=['Super', 'ETank'])) # require heat proof as long as taking damage is necessary

        return SMBool(False, 0)

    # go though the pirates room filled with acid
    @Cache.decorator
    def canPassAmphitheaterReverse(self):
        sm = self.smbm
        nTanks = 4
        if not sm.heatProof():
            nTanks = 16
        return sm.wand(sm.haveItem('Gravity'),
                       sm.energyReserveCountOk(nTanks))

    @Cache.decorator
    def canClimbRedTower(self):
        sm = self.smbm
        return sm.wor(sm.knowsRedTowerClimb(),
                      sm.haveItem('Ice'),
                      sm.haveItem('SpaceJump'))

    @Cache.decorator
    def canClimbBottomRedTower(self):
        sm = self.smbm
        return sm.wor(sm.wor(RomPatches.has(RomPatches.RedTowerLeftPassage),
                             sm.haveItem('HiJump'),
                             sm.haveItem('Ice'),
                             sm.canFly()),
                      sm.canShortCharge())

    @Cache.decorator
    def canGoUpMtEverest(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Gravity'),
                              sm.wor(sm.haveItem('Grapple'),
                                     sm.haveItem('SpeedBooster'),
                                     sm.canFly(),
                                     sm.wand(sm.haveItem('HiJump'), sm.knowsGravityJump()))),
                      sm.wand(sm.canDoSuitlessOuterMaridia(),
                              sm.haveItem('Grapple')))

    @Cache.decorator
    def canPassMtEverest(self):
        sm = self.smbm
        return  sm.wor(sm.wand(sm.haveItem('Gravity'),
                               sm.wor(sm.wor(sm.haveItem('Grapple'),
                                             sm.haveItem('SpeedBooster')),
                                      sm.wor(sm.canFly(),
                                             sm.knowsGravityJump(),
                                             sm.wand(sm.haveItem('Ice'), sm.knowsTediousMountEverest())))),
                       sm.canDoSuitlessMaridia(),
                       sm.wand(sm.haveItem('Ice'), sm.canDoSuitlessOuterMaridia(), sm.knowsTediousMountEverest()))

    @Cache.decorator
    def canDoSuitlessOuterMaridia(self):
        sm = self.smbm
        return sm.wand(sm.knowsGravLessLevel1(),
                       sm.haveItem('HiJump'),
                       sm.wor(sm.haveItem('Ice'),
                              sm.canSpringBallJump()))

    @Cache.decorator
    def canDoSuitlessMaridia(self):
        sm = self.smbm
        return sm.wand(sm.canDoSuitlessOuterMaridia(),
                       sm.haveItem('Grapple'))

    @Cache.decorator
    def canAccessBotwoonFromMainStreet(self):
        sm = self.smbm
        return sm.wand(sm.canPassMtEverest(),
                       sm.canOpenGreenDoors(),
                       sm.canUsePowerBombs())

    # from main street only
    @Cache.decorator
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

    @Cache.decorator
    def canAccessDraygonFromMainStreet(self):
        sm = self.smbm
        return sm.wand(sm.canDefeatBotwoon(),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.canDoSuitlessMaridia(), sm.knowsGravLessLevel2())))

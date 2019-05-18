from functools import reduce

# the difficulties for each technics
from smbool import SMBool
from rom import RomPatches
from helpers import Helpers, Bosses
from graph_access import getAccessPoint
from cache import Cache
from math import ceil

class HelpersGraph(Helpers):
    def __init__(self, smbm):
        self.smbm = smbm
        self.vanillaDraygon = None

    @Cache.decorator
    def canAccessKraidsLair(self):
        sm = self.smbm
        # EXPLAINED: access the upper right platform with either:
        #             -hijump boots (easy regular way)
        #             -fly (space jump or infinite bomb jump)
        #             -know how to wall jump on the platform without the hijump boots
        return sm.wand(lambda: sm.canOpenGreenDoors(),
                       lambda: sm.wor(lambda: sm.haveItem('HiJump'),
                                      lambda: sm.canFly(),
                                      lambda: sm.knowsEarlyKraid()))

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
        return sm.wor(lambda: sm.haveItem('Grapple'),
                      lambda: sm.haveItem('SpaceJump'),
                      lambda: sm.knowsContinuousWallJump(),
                      lambda: sm.wand(lambda: sm.knowsDiagonalBombJump(),
                                      lambda: sm.canUseBombs()),
                      lambda: sm.canSimpleShortCharge(),
                      lambda: sm.wand(lambda: sm.haveItem('Gravity'),
                                      lambda: sm.wor(lambda: sm.knowsGravityJump(),
                                                     lambda: sm.haveItem('HiJump'),
                                                     lambda: sm.canInfiniteBombJump())),
                      lambda: sm.wand(lambda: sm.knowsMockballWs(),
                                      lambda: sm.canUseSpringBall()))

    @Cache.decorator
    def canPassMoatReverse(self):
        sm = self.smbm
        return sm.wor(lambda: sm.haveItem('Grapple'),
                      lambda: sm.haveItem('SpaceJump'),
                      lambda: sm.haveItem('Gravity'),
                      lambda: sm.wand(lambda: sm.haveItem('Morph'),
                                      lambda: sm.wor(lambda: RomPatches.has(RomPatches.MoatShotBlock),
                                                     lambda: sm.canPassBombPassages())))

    @Cache.decorator
    def canPassSpongeBath(self):
        sm = self.smbm
        return sm.wand(lambda: Bosses.bossDead('Phantoon'),
                       lambda: sm.wor(lambda: sm.wand(lambda: sm.canPassBombPassages(),
                                                      lambda: sm.knowsSpongeBathBombJump()),
                                      lambda: sm.wand(lambda: sm.haveItem('HiJump'),
                                                      lambda: sm.knowsSpongeBathHiJump()),
                                      lambda: sm.wor(lambda: sm.haveItem('Gravity'),
                                                     lambda: sm.haveItem('SpaceJump'),
                                                     lambda: sm.wand(lambda: sm.haveItem('SpeedBooster'),
                                                                     lambda: sm.knowsSpongeBathSpeed()),
                                                     lambda: sm.canSpringBallJump())))

    @Cache.decorator
    def canPassBowling(self):
        sm = self.smbm
        return sm.wand(lambda: Bosses.bossDead('Phantoon'),
                       lambda: sm.wor(lambda: sm.heatProof(),
                                      lambda: sm.energyReserveCountOk(1),
                                      lambda: sm.haveItem("SpaceJump"),
                                      lambda: sm.haveItem("Grapple")))

    @Cache.decorator
    def canAccessEtecoons(self):
        sm = self.smbm
        return sm.wor(lambda: sm.canUsePowerBombs(),
                      lambda: sm.wand(lambda: sm.knowsMoondance(),
                                      lambda: sm.canUseBombs(),
                                      lambda: sm.canOpenRedDoors()))

    # the water zone east of WS
    def canPassForgottenHighway(self, fromWs):
        sm = self.smbm
        suitless = sm.canDoSuitlessOuterMaridia()
        if fromWs is True:
            suitless = sm.wand(lambda: suitless, # to climb on the ledges
                               lambda: sm.haveItem('SpaceJump')) # to go through the door on the right
        return sm.wand(lambda: sm.wor(lambda: sm.haveItem('Gravity'),
                                      lambda: suitless),
                       lambda: sm.haveItem('Morph')) # for crab maze

    @Cache.decorator
    def canExitCrabHole(self):
        sm = self.smbm
        return sm.wand(lambda: sm.haveItem('Morph'), # morph to exit the hole
                       lambda: sm.wor(lambda: sm.wand(lambda: sm.haveItem('Gravity'), # even with gravity you need some way to climb...
                                                      lambda: sm.wor(lambda: sm.haveItem('Ice'), # ...on crabs...
                                                                     lambda: sm.haveItem('HiJump'), # ...or by jumping
                                                                     lambda: sm.knowsGravityJump(),
                                                                     lambda: sm.canFly())),
                                      lambda: sm.wand(lambda: sm.haveItem('Ice'),
                                                      lambda: sm.canDoSuitlessOuterMaridia()))) # climbing crabs

    @Cache.decorator
    def canPassMaridiaToRedTowerNode(self):
        sm = self.smbm
        return sm.wand(lambda: sm.haveItem('Morph'),
                       lambda: sm.wor(lambda: RomPatches.has(RomPatches.AreaRandoGatesBase),
                                      lambda: sm.canOpenGreenDoors()))

    @Cache.decorator
    def canPassRedTowerToMaridiaNode(self):
        sm = self.smbm
        return sm.wand(lambda: sm.haveItem('Morph'),
                       lambda: RomPatches.has(RomPatches.AreaRandoGatesBase))

    def canEnterCathedral(self, mult=1.0):
        sm = self.smbm
        return sm.wand(lambda: sm.canOpenRedDoors(),
                       lambda: sm.wor(lambda: sm.wand(lambda: sm.canHellRun('MainUpperNorfair', mult),
                                                      lambda: sm.wor(lambda: sm.wor(lambda: RomPatches.has(RomPatches.CathedralEntranceWallJump),
                                                                                    lambda: sm.haveItem('HiJump'),
                                                                                    lambda: sm.canFly()),
                                                                     lambda: sm.wor(lambda: sm.haveItem('SpeedBooster'), # spark
                                                                                    lambda: sm.canSpringBallJump()))),
                                      lambda: sm.wand(lambda: sm.canHellRun('MainUpperNorfair', 0.5*mult),
                                                      lambda: sm.knowsNovaBoost())))

    @Cache.decorator
    def canHellRunToSpeedBooster(self):
        sm = self.smbm
        mult = 1
        hasSpeed = sm.haveItem('SpeedBooster').bool
        if hasSpeed == True:
            mult = 2
        return sm.canHellRun('MainUpperNorfair', mult)

    @Cache.decorator
    def canExitCathedral(self):
        # from top: can use bomb/powerbomb jumps
        # from bottom: can do a shinespark or use space jump
        #              can do it with highjump + wall jump
        #              can do it with only two wall jumps (the first one is delayed like on alcatraz)
        #              can do it with a spring ball jump from wall
        sm = self.smbm
        return sm.wand(lambda: sm.wor(lambda: sm.canHellRun('MainUpperNorfair', 0.75),
                                      lambda: sm.heatProof()),
                       lambda: sm.wor(lambda: sm.wor(lambda: sm.canPassBombPassages(),
                                                     lambda: sm.haveItem("SpeedBooster")),
                                      lambda: sm.wor(lambda: sm.haveItem("SpaceJump"),
                                                     lambda: sm.haveItem("HiJump"),
                                                     lambda: sm.knowsWallJumpCathedralExit(),
                                                     lambda: sm.wand(lambda: sm.knowsSpringBallJumpFromWall(),
                                                                     lambda: sm.canUseSpringBall()))))

    @Cache.decorator
    def canGrappleEscape(self):
        sm = self.smbm
        return sm.wor(lambda: sm.wor(lambda: sm.haveItem('SpaceJump'),
                                     lambda: sm.wand(lambda: sm.canInfiniteBombJump(), # IBJ from lava...either have grav or freeze the enemy there if hellrunning (otherwise single DBJ at the end)
                                                     lambda: sm.wor(lambda: sm.heatProof(),
                                                                    lambda: sm.haveItem('Gravity'),
                                                                    lambda: sm.haveItem('Ice')))),
                      lambda: sm.haveItem('Grapple'),
                      lambda: sm.wand(lambda: sm.haveItem('SpeedBooster'),
                                      lambda: sm.wor(lambda: sm.haveItem('HiJump'), # jump from the blocks below
                                                     lambda: sm.knowsShortCharge())), # spark from across the grapple blocks
                      lambda: sm.wand(lambda: sm.haveItem('HiJump'),
                                      lambda: sm.canSpringBallJump())) # jump from the blocks below

    @Cache.decorator
    def canPassFrogSpeedwayRightToLeft(self):
        sm = self.smbm
        return sm.wor(lambda: sm.haveItem('SpeedBooster'),
                      lambda: sm.wand(lambda: sm.knowsFrogSpeedwayWithoutSpeed(),
                                      lambda: sm.haveItem('Wave'),
                                      lambda: sm.wor(lambda: sm.haveItem('Spazer'),
                                                     lambda: sm.haveItem('Plasma'))))

    @Cache.decorator
    def canEnterNorfairReserveArea(self):
        sm = self.smbm
        return sm.wand(lambda: sm.canOpenGreenDoors(),
                       lambda: sm.wor(lambda: sm.wor(lambda: sm.canFly(),
                                                     lambda: sm.haveItem('Grapple'),
                                                     lambda: sm.wand(lambda: sm.haveItem('HiJump'),
                                                                     lambda: sm.knowsGetAroundWallJump())),
                                      lambda: sm.wor(lambda: sm.haveItem('Ice'),
                                                     lambda: sm.wand(lambda: sm.canUseSpringBall(),
                                                                     lambda: sm.knowsSpringBallJumpFromWall()),
                                                     lambda: sm.knowsNorfairReserveDBoost())))

    @Cache.decorator
    def canPassLavaPit(self):
        sm = self.smbm
        nTanks4Dive = 3
        if sm.heatProof().bool == False:
            nTanks4Dive = 8
        if sm.haveItem('HiJump').bool == False:
            nTanks4Dive = ceil(nTanks4Dive * 1.25) # 4 or 10
        return sm.wand(lambda: sm.wor(lambda: sm.wand(lambda: sm.haveItem('Gravity'),
                                                      lambda: sm.haveItem('SpaceJump')),
                                      lambda: sm.wand(lambda: sm.knowsGravityJump(),
                                                      lambda: sm.haveItem('Gravity'),
                                                      lambda: sm.wor(lambda: sm.haveItem('HiJump'),
                                                                     lambda: sm.knowsLavaDive())),
                                      lambda: sm.wand(lambda: sm.wor(lambda: sm.wand(lambda: sm.knowsLavaDive(),
                                                                                     lambda: sm.haveItem('HiJump')),
                                                                     lambda: sm.knowsLavaDiveNoHiJump()),
                                                      lambda: sm.energyReserveCountOk(nTanks4Dive))),
                       lambda: sm.canUsePowerBombs()) # power bomb blocks left and right of LN entrance without any items before

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
        return sm.wand(lambda: sm.canHellRun('LowerNorfair', 0.75), # 0.75 to require one more CF if no heat protection because of distance to cover, wait times, acid...
                       lambda: sm.canUsePowerBombs(),
                       lambda: sm.wor(lambda: sm.haveItem('SpaceJump'),
                                      lambda: RomPatches.has(RomPatches.LNChozoSJCheckDisabled)))

    @Cache.decorator
    def canExitScrewAttackArea(self):
        sm = self.smbm

        return sm.wand(lambda: sm.canDestroyBombWalls(),
                       lambda: sm.wor(lambda: sm.canFly(),
                                      lambda: sm.wand(lambda: sm.haveItem('HiJump'),
                                                      lambda: sm.haveItem('SpeedBooster'),
                                                      lambda: sm.wor(lambda: sm.wand(lambda: sm.haveItem('ScrewAttack'),
                                                                                     lambda: sm.knowsScrewAttackExit()),
                                                                     lambda: sm.knowsScrewAttackExitWithoutScrew())),
                                      lambda: sm.wand(lambda: sm.canUseSpringBall(),
                                                      lambda: sm.knowsSpringBallJumpFromWall()),
                                      lambda: sm.wand(lambda: sm.canSimpleShortCharge(), # fight GT and spark out
                                                      lambda: sm.enoughStuffGT())))

    @Cache.decorator
    def canPassWorstRoom(self):
        sm = self.smbm
        return sm.wand(lambda: sm.canDestroyBombWalls(),
                       lambda: sm.wor(lambda: sm.canFly(),
                                      lambda: sm.wand(lambda: sm.knowsWorstRoomIceCharge(),
                                                      lambda: sm.haveItem('Ice'),
                                                      lambda: sm.haveItem('Charge')),
                                      lambda: sm.wand(lambda: sm.knowsGetAroundWallJump(),
                                                      lambda: sm.haveItem('HiJump')),
                                      lambda: sm.wand(lambda: sm.knowsSpringBallJumpFromWall(),
                                                      lambda: sm.canUseSpringBall())))

    @Cache.decorator
    def canPassThreeMuskateers(self):
        sm = self.smbm
        destroy = sm.wor(lambda: sm.haveItem('Plasma'),
                         lambda: sm.haveItem('ScrewAttack'),
                         lambda: sm.wand(lambda: sm.heatProof(), # this takes a loooong time ...
                                         lambda: sm.wor(lambda: sm.haveItem('Spazer'),
                                                        lambda: sm.haveItem('Ice'))))
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
            return sm.wand(lambda: sm.heatProof(),
                           lambda: SMBool(True, 0, items=['Super', 'ETank'])) # require heat proof as long as taking damage is necessary

        return SMBool(False, 0)

    # go though the pirates room filled with acid
    @Cache.decorator
    def canPassAmphitheaterReverse(self):
        sm = self.smbm
        nTanksGrav = 3
        nTanksNoGrav = 6
        if sm.heatProof().bool == False:
            nTanksGrav *= 5
            nTanksNoGrav *= 5 # 30 should not happen ...
        return sm.wor(lambda: sm.wand(lambda: sm.haveItem('Gravity'),
                                      lambda: sm.energyReserveCountOk(nTanksGrav)),
                      lambda: sm.wand(lambda: sm.energyReserveCountOk(nTanksNoGrav),
                                      lambda: sm.knowsLavaDive())) # should be a good enough skill filter for acid wall jumps with no grav...

    @Cache.decorator
    def canClimbRedTower(self):
        sm = self.smbm
        return sm.wor(lambda: sm.knowsRedTowerClimb(),
                      lambda: sm.haveItem('Ice'),
                      lambda: sm.haveItem('SpaceJump'))

    @Cache.decorator
    def canClimbBottomRedTower(self):
        sm = self.smbm
        return sm.wor(lambda: sm.wor(lambda: RomPatches.has(RomPatches.RedTowerLeftPassage),
                                     lambda: sm.haveItem('HiJump'),
                                     lambda: sm.haveItem('Ice'),
                                     lambda: sm.canFly()),
                      lambda: sm.canShortCharge())

    @Cache.decorator
    def canGoUpMtEverest(self):
        sm = self.smbm
        return sm.wor(lambda: sm.wand(lambda: sm.haveItem('Gravity'),
                                      lambda: sm.wor(lambda: sm.haveItem('Grapple'),
                                                     lambda: sm.haveItem('SpeedBooster'),
                                                     lambda: sm.canFly(),
                                                     lambda: sm.wand(lambda: sm.haveItem('HiJump'),
                                                                     lambda: sm.knowsGravityJump()))),
                      lambda: sm.wand(lambda: sm.canDoSuitlessOuterMaridia(),
                                      lambda: sm.haveItem('Grapple')))

    @Cache.decorator
    def canPassMtEverest(self):
        sm = self.smbm
        return  sm.wor(lambda: sm.wand(lambda: sm.haveItem('Gravity'),
                                       lambda: sm.wor(lambda: sm.wor(lambda: sm.haveItem('Grapple'),
                                                                     lambda: sm.haveItem('SpeedBooster')),
                                                      lambda: sm.wor(lambda: sm.canFly(),
                                                                     lambda: sm.knowsGravityJump(),
                                                                     lambda: sm.wand(lambda: sm.haveItem('Ice'),
                                                                                     lambda: sm.knowsTediousMountEverest())))),
                       lambda: sm.canDoSuitlessMaridia(),
                       lambda: sm.wand(lambda: sm.haveItem('Ice'),
                                       lambda: sm.canDoSuitlessOuterMaridia(),
                                       lambda: sm.knowsTediousMountEverest()))

    @Cache.decorator
    def canDoSuitlessOuterMaridia(self):
        sm = self.smbm
        return sm.wand(lambda: sm.knowsGravLessLevel1(),
                       lambda: sm.haveItem('HiJump'),
                       lambda: sm.wor(lambda: sm.haveItem('Ice'),
                                      lambda: sm.canSpringBallJump()))

    @Cache.decorator
    def canDoSuitlessMaridia(self):
        sm = self.smbm
        return sm.wand(lambda: sm.canDoSuitlessOuterMaridia(),
                       lambda: sm.wor(lambda: sm.haveItem('Grapple'),
                                      lambda: sm.canDoubleSpringBallJump()))

    @Cache.decorator
    def canAccessBotwoonFromMainStreet(self):
        sm = self.smbm
        return sm.wand(lambda: sm.canPassMtEverest(),
                       lambda: sm.canOpenGreenDoors(),
                       lambda: sm.canUsePowerBombs())

    # from main street only
    @Cache.decorator
    def canDefeatBotwoon(self):
        sm = self.smbm
        # EXPLAINED: in Botwoon Hallway, either:
        #             -use regular speedbooster (with gravity)
        #             -do a mochtroidclip (https://www.youtube.com/watch?v=1z_TQu1Jf1I&t=20m28s)
        return sm.wand(lambda: sm.canAccessBotwoonFromMainStreet(),
                       lambda: sm.enoughStuffBotwoon(),
                       lambda: sm.wor(lambda: sm.wand(lambda: sm.haveItem('SpeedBooster'),
                                                      lambda: sm.haveItem('Gravity')),
                                      lambda: sm.wand(lambda: sm.knowsMochtroidClip(),
                                                      lambda: sm.haveItem('Ice'))))

    @Cache.decorator
    def canAccessDraygonFromMainStreet(self):
        sm = self.smbm
        return sm.wand(lambda: sm.wor(lambda: sm.haveItem('Gravity'),
                                      lambda: sm.wand(lambda: sm.canDoSuitlessMaridia(),
                                                      lambda: sm.knowsGravLessLevel2())),
                       lambda: sm.canDefeatBotwoon())

    def isVanillaDraygon(self):
        if self.vanillaDraygon is None:
            drayRoomOut = getAccessPoint('DraygonRoomOut')
            self.vanillaDraygon = drayRoomOut.ConnectedTo == 'DraygonRoomIn'
        return self.vanillaDraygon

    @Cache.decorator
    def canFightDraygon(self):
        sm = self.smbm
        return sm.wor(lambda: sm.haveItem('Gravity'),
                      lambda: sm.wand(lambda: sm.haveItem('HiJump'),
                                      lambda: sm.wor(lambda: sm.knowsGravLessLevel2(),
                                                     lambda: sm.knowsGravLessLevel3())))

    @Cache.decorator
    def canDraygonCrystalFlashSuit(self):
        sm = self.smbm
        return sm.wand(lambda: sm.canCrystalFlash(),
                       lambda: sm.knowsDraygonRoomCrystalFlash(),
                       # ask for 4 PB pack as an ugly workaround for
                       # a rando bug which can place a PB at space
                       # jump to "get you out" (this check is in
                       # PostAvailable condition of the Dray/Space
                       # Jump locs)
                       lambda: sm.itemCountOk('PowerBomb', 4))

    @Cache.decorator
    def canExitDraygonVanilla(self):
        sm = self.smbm
        # to get out of draygon room:
        #   with gravity but without highjump/bomb/space jump: gravity jump
        #     to exit draygon room: grapple or crystal flash (for free shine spark)
        #     to exit precious room: spring ball jump, xray scope glitch or stored spark
        return sm.wor(lambda: sm.wand(lambda: sm.haveItem('Gravity'),
                                      lambda: sm.wor(lambda: sm.canFly(),
                                                     lambda: sm.knowsGravityJump(),
                                                     lambda: sm.wand(lambda: sm.haveItem('HiJump'),
                                                                     lambda: sm.haveItem('SpeedBooster')))),
                      lambda: sm.wand(lambda: sm.canDraygonCrystalFlashSuit(),
                                      # use the spark either to exit draygon room or precious room
                                      lambda: sm.wor(lambda: sm.wand(lambda: sm.haveItem('Grapple'),
                                                                     lambda: sm.knowsDraygonRoomGrappleExit()),
                                                     lambda: sm.wand(lambda: sm.haveItem('XRayScope'),
                                                                     lambda: sm.knowsPreciousRoomXRayExit()),
                                                     lambda: sm.canSpringBallJump())),
                      # spark-less exit (no CF)
                      lambda: sm.wand(lambda: sm.wand(lambda: sm.haveItem('Grapple'),
                                                      lambda: sm.knowsDraygonRoomGrappleExit()),
                                      lambda: sm.wor(lambda: sm.wand(lambda: sm.haveItem('XRayScope'),
                                                                     lambda: sm.knowsPreciousRoomXRayExit()),
                                                     lambda: sm.canSpringBallJump())),
                      lambda: sm.canDoubleSpringBallJump())

    @Cache.decorator
    def canExitDraygonRandomized(self):
        sm = self.smbm
        # disregard precious room
        return sm.wor(lambda: sm.wand(lambda: sm.haveItem('Gravity'),
                                      lambda: sm.wor(lambda: sm.canFly(),
                                                     lambda: sm.knowsGravityJump(),
                                                     lambda: sm.wand(lambda: sm.haveItem('HiJump'),
                                                                     lambda: sm.haveItem('SpeedBooster')))),
                      lambda: sm.canDraygonCrystalFlashSuit(),
                      lambda: sm.wand(lambda: sm.haveItem('Grapple'),
                                      lambda: sm.knowsDraygonRoomGrappleExit()),
                      lambda: sm.canDoubleSpringBallJump())

    def canExitDraygon(self):
        if self.isVanillaDraygon():
            return self.canExitDraygonVanilla()
        else:
            return self.canExitDraygonRandomized()

    @Cache.decorator
    def canExitPreciousRoomVanilla(self):
        return SMBool(True) # handled by canExitDraygonVanilla

    @Cache.decorator
    def canExitPreciousRoomRandomized(self):
        sm = self.smbm
        return sm.wor(lambda: sm.wand(lambda: sm.haveItem('Gravity'),
                                      lambda: sm.wor(lambda: sm.canFly(),
                                                     lambda: sm.knowsGravityJump(),
                                                     lambda: sm.haveItem('HiJump'))),
                      lambda: sm.wor(lambda: sm.wand(lambda: sm.haveItem('XRayScope'),
                                                     lambda: sm.knowsPreciousRoomXRayExit()),
                                     lambda: sm.canSpringBallJump()))

    def canExitPreciousRoom(self):
        if self.isVanillaDraygon():
            return self.canExitPreciousRoomVanilla()
        else:
            return self.canExitPreciousRoomRandomized()

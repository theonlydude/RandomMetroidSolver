from functools import reduce

# the difficulties for each technics
from smbool import SMBool
from rom import RomPatches
from helpers import Helpers, Bosses

class HelpersGraph(Helpers):
    def __init__(self, smbm):
        self.smbm = smbm
        # cacheable functions sorted to avoid dependencies
        self.cachedMethods = []

    def canAccessKraidsLair(self):
        # EXPLAINED: access the upper right platform with either:
        #             -hijump boots (easy regular way)
        #             -fly (space jump or infinite bomb jump)
        #             -know how to wall jump on the platform without the hijump boots
        #            then we have to break a bomb block at Warehouse Zeela room
        return self.smbm.wand(self.smbm.canOpenGreenDoors(),
                              self.smbm.wor(self.smbm.haveItem('HiJump'),
                                            self.smbm.canFly(),
                                            self.smbm.knowsEarlyKraid()),
                              self.smbm.canPassBombPassages())

    def canPassTerminatorBombWall(self):
        return self.smbm.wor(self.smbm.wand(self.smbm.haveItem('SpeedBooster'),
                                            self.smbm.wor(self.smbm.knowsSimpleShortCharge(), self.smbm.knowsShortCharge())), 
                             self.smbm.canDestroyBombWalls())

    def canPassMoat(self):
        # EXPLAINED: In the Moat we can either:
        #             -use grapple or space jump (easy way)
        #             -do a continuous wall jump (https://www.youtube.com/watch?v=4HVhTwwax6g)
        #             -do a diagonal bomb jump from the middle platform (https://www.youtube.com/watch?v=5NRqQ7RbK3A&t=10m58s)
        #             -do a short charge from the Keyhunter room (https://www.youtube.com/watch?v=kFAYji2gFok)
        #             -do a gravity jump from below the right platform
        #             -do a mock ball and a bounce ball (https://www.youtube.com/watch?v=WYxtRF--834)
        return self.smbm.wor(self.smbm.wor(self.smbm.haveItem('Grapple'),
                                           self.smbm.haveItem('SpaceJump'),
                                           self.smbm.knowsContinuousWallJump()),
                             self.smbm.wor(self.smbm.wand(self.smbm.knowsDiagonalBombJump(), self.smbm.canUseBombs()),
                                           self.smbm.wand(self.smbm.haveItem('SpeedBooster'),
                                                          self.smbm.wor(self.smbm.knowsSimpleShortCharge(), self.smbm.knowsShortCharge())),
                                           self.smbm.wand(self.smbm.knowsGravityJump(), self.smbm.haveItem('Gravity')),
                                           self.smbm.wand(self.smbm.knowsMockballWs(), self.smbm.haveItem('Morph'), self.smbm.haveItem('SpringBall'))))

    def canPassMoatReverse(self):
        return self.smbm.wor(self.smbm.haveItem('Grapple'),
                             self.smbm.haveItem('SpaceJump'),
                             self.smbm.haveItem('Gravity'),
                             self.smbm.wand(haveItem('Morph'),
                                            self.smbm.wor(RomPatches.has(RomPatches.MoatShotBlock),
                                                          self.smbm.canPassBombPassages())))

    def canPassSpongeBath(self):
        return self.smbm.wand(Bosses.bossDead('Phantoon'),
                              self.smbm.wor(self.smbm.wand(self.smbm.canPassBombPassages(),
                                                           self.smbm.knowsSpongeBathBombJump()),
                                            self.smbm.wand(self.smbm.haveItem('HiJump'),
                                                           self.smbm.knowsSpongeBathHiJump()),
                                            self.smbm.wor(self.smbm.haveItem('Gravity'),
                                                          self.smbm.haveItem('SpaceJump'),
                                                          self.smbm.wand(self.smbm.haveItem('SpeedBooster'),
                                                                         self.smbm.knowsSpongeBathSpeed()),
                                                          self.smbm.wand(self.smbm.haveItem('Morph'),
                                                                         self.smbm.haveItem('SpringBall'),
                                                                         self.smbm.knowsSpringBallJump()))))

    # the water zone east of WS
    def canPassForgottenHighway(self, fromWs):
        # TODO add knows for this?
        baseSuitLess = self.smbm.wand(self.smbm.haveItem('HiJump'),
                                      self.smbm.wor(self.smbm.haveItem('Ice'), 
                                                    self.smbm.wand(self.smbm.haveItem('SpringBall'), self.smbm.knowsSpringBallJump())))
        if fromWs is True:
            suitlessCondition = self.smbm.wand(baseSuitLess, # to climb on the ledges
                                               self.smbm.haveItem('SpaceJump')) # to go through the door on the right
        else:
            suitlessCondition = baseSuitLess

        return self.smbm.wor(self.smbm.haveItem('Gravity'),
                             suitlessCondition)

    def canExitCrabHole(self):
        return self.smbm.wand(self.smbm.haveItem('Morph'), # morph to exit the hole
                              self.smbm.canOpenRedDoors(), # to exit and re-enter if needed
                              self.smbm.wor(self.smbm.wand(self.smbm.haveItem('Gravity'), # even with gravity you need some way to climb...
                                                           self.smbm.wor(self.smbm.haveItem('Ice'), # ...on crabs...
                                                                         self.smbm.haveItem('HiJump'), # ...or by jumping
                                                                         self.smbm.knowsGravityJump(),
                                                                         self.smbm.canFly())),
                                            self.smbm.canDoSuitlessOuterMaridia())) # climing crabs

    def canAccessHeatedNorfairFromEntrance(self, bubbleMountain=True):
        return self.smbm.wand(self.smbm.wor(self.smbm.wand(self.smbm.haveItem('SpeedBooster'), # frog speedway
                                                           self.smbm.wor(SMBool(not bubbleMountain, 0), self.smbm.canPassBombPassages())),
                                            # go through cathedral
                                            self.smbm.wand(self.smbm.canOpenRedDoors(),
                                                           self.smbm.wor(RomPatches.has(RomPatches.CathedralEntranceWallJump),
                                                                         self.smbm.haveItem('HiJump'),
                                                                         self.smbm.canFly()))),
                              self.smbm.canHellRun('MainUpperNorfair'))

    def canAccessCrocFromNorfairEntrance(self):
        return self.smbm.wand(self.smbm.wand(self.smbm.canOpenGreenDoors(), # below Ice
                                             self.smbm.haveItem('SpeedBooster'),
                                             self.smbm.canUsePowerBombs(),
                                             self.smbm.energyReserveCountOk(2)),
                              self.smbm.wand(self.smbm.canAccessHeatedNorfairFromEntrance(bubbleMountain=False),
                                             self.smbm.wor(self.smbm.wand(self.smbm.canOpenRedDoors(), self.smbm.knowsGreenGateGlitch()),
                                                           self.smbm.haveItem('Wave'))))

    def canAccessCrocFromMainUpperNorfair(self):
        # from bubble mountain
        return self.smbm.wand(self.smbm.canHellRun('MainUpperNorfair'),
                              self.smbm.canPassBombPassages(),
                              self.smbm.wor(self.smbm.wand(self.smbm.canOpenRedDoors(), self.smbm.knowsGreenGateGlitch()),
                                            self.smbm.haveItem('Wave')))

    def canEnterNorfairReserveArea(self):
        return self.smbm.wand(self.smbm.canOpenGreenDoors(),
                              self.smbm.wor(self.smbm.wor(self.smbm.canFly(),
                                                          self.smbm.haveItem('Grapple'),
                                                          self.smbm.wand(self.smbm.haveItem('HiJump'),
                                                                         self.smbm.knowsGetAroundWallJump())),
                                            self.smbm.wor(self.smbm.haveItem('Ice'),
                                                          self.smbm.wand(self.smbm.haveItem('SpringBall'),
                                                                         self.smbm.knowsSpringBallJumpFromWall()))))

    def canPassLavaPit(self):
        nTanks4Dive = 3
        if not self.smbm.heatProof():
            nTanks4Dive = 8
        return self.smbm.wor(self.smbm.wand(self.smbm.haveItem('Gravity'), self.smbm.haveItem('SpaceJump')),
                             self.smbm.wand(self.smbm.knowsGravityJump(), self.smbm.haveItem('Gravity')),
                             self.smbm.wand(self.smbm.wor(self.smbm.wand(self.smbm.knowsLavaDive(), self.smbm.haveItem('HiJump')),
                                                          self.smbm.knowsLavaDiveNoHiJump()),
                                            self.smbm.energyReserveCountOk(nTanks4Dive)))

    def canPassWorstRoom(self):
        return self.smbm.wor(self.smbm.canFly(),
                             self.smbm.wand(self.smbm.knowsWorstRoomIceCharge(), self.smbm.haveItem('Ice'), self.smbm.haveItem('Charge')),
                             self.smbm.wand(self.smbm.knowsGetAroundWallJump(), self.smbm.haveItem('HiJump')),
                             self.smbm.wand(self.smbm.knowsSpringBallJumpFromWall(), self.smbm.haveItem('SpringBall')))

    # go though the pirates room filled with acid
    def canPassAmphitheaterReverse(self):
        nTanks = 4
        if not self.smbm.heatProof():
            nTanks = 16
        return self.smbm.wand(self.smbm.haveItem('Gravity'),
                              self.smbm.energyReserveCountOk(nTanks))

    def canClimbRedTower(self):
        return self.smbm.wor(self.smbm.knowsRedTowerClimb(),
                             self.smbm.haveItem('Ice'),
                             self.smbm.haveItem('SpaceJump'))

    def canClimbBottomRedTower(self):
        return self.smbm.wor(self.smbm.wor(RomPatches.has(RomPatches.RedTowerLeftPassage),
                                           self.smbm.haveItem('HiJump'),
                                           self.smbm.haveItem('Ice'),
                                           self.smbm.canFly()),
                             self.smbm.wand(self.smbm.haveItem('SpeedBooster'), self.smbm.knowsShortCharge()))

    def canGoUpMtEverest(self):
        return self.smbm.wor(self.smbm.wand(self.smbm.haveItem('Gravity'),                      
                                            self.smbm.wor(self.smbm.haveItem('Grapple'),
                                                          self.smbm.haveItem('SpeedBooster')),
                                            self.smbm.wor(self.smbm.canFly(),
                                                          self.smbm.knowsGravityJump())),
                             self.smbm.wand(self.smbm.canDoSuitlessOuterMaridia(),
                                            self.smbm.haveItem('Grapple')))

    def canPassMtEverest(self):
        return  self.smbm.wor(self.smbm.wand(self.smbm.haveItem('Gravity'),                      
                                             self.smbm.wor(self.smbm.wor(self.smbm.haveItem('Grapple'),
                                                                         self.smbm.haveItem('SpeedBooster')),
                                                           self.smbm.wor(self.smbm.canFly(),
                                                                         self.smbm.knowsGravityJump(),
                                                                         self.smbm.wand(self.smbm.haveItem('Ice'), self.smbm.knowsTediousMountEverest())))),
                              self.smbm.canDoSuitlessMaridia(),
                              self.smbm.wand(self.smbm.canDoSuitlessOuterMaridia(), self.smbm.knowsTediousMountEverest()))

    def canAccessDraygonFromMainStreet(self):
        return self.smbm.wand(self.smbm.canDefeatBotwoon(),
                              self.smbm.wor(self.smbm.haveItem('Gravity'),
                                            self.smbm.canDoSuitlessMaridia()))

    def canDoSuitlessOuterMaridia(self):
        return self.smbm.wand(self.smbm.knowsGravLessLevel1(),
                              self.smbm.haveItem('HiJump'),
                              self.smbm.haveItem('Ice'),
                              self.smbm.wor(self.smbm.haveItem('Wave'),
                                            self.smbm.haveItem('Spazer'),
                                            self.smbm.haveItem('Plasma')))

    def canAccessBotwoonFromMainStreet(self):
        return self.smbm.wand(self.smbm.canPassMtEverest(),
                              self.smbm.canOpenGreenDoors(),
                              self.smbm.canUsePowerBombs())

    # from main street only
    def canDefeatBotwoon(self):
        # EXPLAINED: in Botwoon Hallway, either:
        #             -use regular speedbooster (with gravity)
        #             -do a mochtroidclip (https://www.youtube.com/watch?v=1z_TQu1Jf1I&t=20m28s)
        return self.smbm.wand(self.smbm.canAccessBotwoonFromMainStreet(),
                              self.smbm.enoughStuffBotwoon(),
                              self.smbm.wor(self.smbm.wand(self.smbm.haveItem('SpeedBooster'),
                                                           self.smbm.haveItem('Gravity')),
                                            self.smbm.wand(self.smbm.knowsMochtroidClip(), self.smbm.haveItem('Ice'))))

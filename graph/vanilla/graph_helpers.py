from math import ceil

from logic.smbool import SMBool
from logic.helpers import Helpers, Bosses
from logic.cache import Cache
from rom.rom_patches import RomPatches
from graph.graph_utils import getAccessPoint
from utils.parameters import Settings

class HelpersGraph(Helpers):
    def __init__(self, smbm):
        self.smbm = smbm

    def canEnterAndLeaveGauntletQty(self, nPB, nTanksSpark):
        sm = self.smbm
        # EXPLAINED: to access Gauntlet Entrance from Landing site we can either:
        #             -fly to it (infinite bomb jumps or space jump)
        #             -shinespark to it
        #             -wall jump with high jump boots
        #             -wall jump without high jump boots
        #            then inside it to break the bomb wals:
        #             -use screw attack (easy way)
        #             -use power bombs
        #             -use bombs
        #             -perform a simple short charge on the way in
        #              and use power bombs on the way out
        return sm.wand(sm.wor(sm.canFly(),
                              sm.haveItem('SpeedBooster'),
                              sm.wand(sm.knowsHiJumpGauntletAccess(),
                                      sm.haveItem('HiJump')),
                              sm.knowsHiJumpLessGauntletAccess()),
                       sm.wor(sm.haveItem('ScrewAttack'),
                              sm.wor(sm.wand(sm.energyReserveCountOkHardRoom('Gauntlet'),
                                             sm.wand(sm.canUsePowerBombs(),
                                                     sm.wor(sm.itemCountOk('PowerBomb', nPB),
                                                            sm.wand(sm.haveItem('SpeedBooster'),
                                                                    sm.energyReserveCountOk(nTanksSpark))))),
                                     sm.wand(sm.energyReserveCountOkHardRoom('Gauntlet', 0.51),
                                             sm.canUseBombs()))))

    @Cache.decorator
    def canEnterAndLeaveGauntlet(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.canShortCharge(),
                              sm.canEnterAndLeaveGauntletQty(2, 2)),
                      sm.canEnterAndLeaveGauntletQty(2, 3))

    def canPassTerminatorBombWall(self, fromLandingSite=True):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('SpeedBooster'),
                              sm.wor(SMBool(not fromLandingSite, 0), sm.knowsSimpleShortCharge(), sm.knowsShortCharge())),
                      sm.canDestroyBombWalls())

    @Cache.decorator
    def canPassCrateriaGreenPirates(self):
        sm = self.smbm
        return sm.wor(sm.canPassBombPassages(),
                      sm.haveMissileOrSuper(),
                      sm.energyReserveCountOk(1),
                      sm.wor(sm.haveItem('Charge'),
                             sm.haveItem('Ice'),
                             sm.haveItem('Wave'),
                             sm.wor(sm.haveItem('Spazer'),
                                    sm.haveItem('Plasma'),
                                    sm.haveItem('ScrewAttack'))))

    # from blue brin elevator
    @Cache.decorator
    def canAccessBillyMays(self):
        sm = self.smbm
        return sm.wand(sm.wor(RomPatches.has(RomPatches.BlueBrinstarBlueDoor),
                              sm.traverse('ConstructionZoneRight')),
                       sm.canUsePowerBombs(),
                       sm.wor(sm.knowsBillyMays(),
                              sm.haveItem('Gravity'),
                              sm.haveItem('SpaceJump')))

    @Cache.decorator
    def canAccessKraidsLair(self):
        sm = self.smbm
        # EXPLAINED: access the upper right platform with either:
        #             -hijump boots (easy regular way)
        #             -fly (space jump or infinite bomb jump)
        #             -know how to wall jump on the platform without the hijump boots
        return sm.wand(sm.haveItem('Super'),
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
        return sm.wor(sm.haveItem('Grapple'),
                      sm.haveItem('SpaceJump'),
                      sm.knowsContinuousWallJump(),
                      sm.wand(sm.knowsDiagonalBombJump(), sm.canUseBombs()),
                      sm.canSimpleShortCharge(),
                      sm.wand(sm.haveItem('Gravity'),
                              sm.wor(sm.knowsGravityJump(),
                                     sm.haveItem('HiJump'),
                                     sm.canInfiniteBombJump())),
                      sm.wand(sm.knowsMockballWs(), sm.canUseSpringBall()))

    @Cache.decorator
    def canPassMoatFromMoat(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Grapple'),
                      sm.haveItem('SpaceJump'),
                      sm.wand(sm.knowsDiagonalBombJump(), sm.canUseBombs()),
                      sm.wand(sm.haveItem('Gravity'),
                              sm.wor(sm.knowsGravityJump(),
                                     sm.haveItem('HiJump'),
                                     sm.canInfiniteBombJump())))

    @Cache.decorator
    def canPassMoatReverse(self):
        sm = self.smbm
        return sm.wor(RomPatches.has(RomPatches.MoatShotBlock),
                      sm.haveItem('Grapple'),
                      sm.haveItem('SpaceJump'),
                      sm.haveItem('Gravity'),
                      sm.canPassBombPassages())

    @Cache.decorator
    def canPassSpongeBath(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.canPassBombPassages(),
                              sm.knowsSpongeBathBombJump()),
                      sm.wand(sm.haveItem('HiJump'),
                              sm.knowsSpongeBathHiJump()),
                      sm.haveItem('Gravity'),
                      sm.haveItem('SpaceJump'),
                      sm.wand(sm.haveItem('SpeedBooster'),
                              sm.knowsSpongeBathSpeed()),
                      sm.canSpringBallJump())

    @Cache.decorator
    def canPassBowling(self):
        sm = self.smbm
        return sm.wand(Bosses.bossDead(sm, 'Phantoon'),
                       sm.wor(SMBool(sm.getDmgReduction()[0] >= 2),
                              sm.energyReserveCountOk(1),
                              sm.haveItem("SpaceJump"),
                              sm.haveItem("Grapple")))

    @Cache.decorator
    def canAccessEtecoons(self):
        sm = self.smbm
        return sm.wor(sm.canUsePowerBombs(),
                      sm.wand(sm.knowsMoondance(), sm.canUseBombs(), sm.traverse('MainShaftBottomRight')))

    @Cache.decorator
    def canKillBeetoms(self):
        sm = self.smbm
        # can technically be killed with bomb, but it's harder
        return sm.wor(sm.haveMissileOrSuper(), sm.canUsePowerBombs(), sm.haveItem('ScrewAttack'))

    # the water zone east of WS
    def canPassForgottenHighway(self, fromWs):
        sm = self.smbm
        suitless = sm.wand(sm.haveItem('HiJump'), sm.knowsGravLessLevel1())
        if fromWs is True and RomPatches.has(RomPatches.EastOceanPlatforms).bool is False:
            suitless = sm.wand(suitless,
                               sm.wor(sm.canSpringBallJump(), # two sbj on the far right
                                      # to break water line and go through the door on the right
                                      sm.haveItem('SpaceJump')))
        return sm.wand(sm.wor(sm.haveItem('Gravity'),
                              suitless),
                       sm.haveItem('Morph')) # for crab maze

    @Cache.decorator
    def canExitCrabHole(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), # morph to exit the hole
                       sm.wor(sm.wand(sm.haveItem('Gravity'), # even with gravity you need some way to climb...
                                      sm.wor(sm.haveItem('Ice'), # ...on crabs...
                                             sm.wand(sm.haveItem('HiJump'), sm.knowsMaridiaWallJumps()), # ...or by jumping
                                             sm.knowsGravityJump(),
                                             sm.canFly())),
                              sm.wand(sm.haveItem('Ice'), sm.canDoSuitlessOuterMaridia()), # climbing crabs
                              sm.canDoubleSpringBallJump()))

    # bottom sandpits with the evirs except west sand hall left to right
    @Cache.decorator
    def canTraverseSandPits(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.knowsGravLessLevel3(),
                              sm.haveItem('HiJump'),
                              sm.wor(sm.haveItem('Ice'),
                                     sm.wand(sm.canSpringBallJump(),
                                             sm.knowsEastSandHallSpringBallJump()))))

    @Cache.decorator
    def canTraverseWestSandHallLeftToRight(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.knowsGravLessLevel3(),
                              sm.haveItem('HiJump'),
                              sm.canUseBombs(),
                              sm.knowsWestSandHallInsaneBombJump()))

    @Cache.decorator
    def canPassMaridiaToRedTowerNode(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       sm.wor(RomPatches.has(RomPatches.AreaRandoGatesBase),
                              sm.haveItem('Super')))

    @Cache.decorator
    def canPassRedTowerToMaridiaNode(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       RomPatches.has(RomPatches.AreaRandoGatesBase))

    def canEnterCathedral(self, mult=1.0):
        sm = self.smbm
        return sm.wand(sm.traverse('CathedralEntranceRight'),
                       sm.wor(sm.wand(sm.canHellRun('MainUpperNorfair', mult),
                                      sm.wor(sm.wor(RomPatches.has(RomPatches.CathedralEntranceWallJump),
                                                    sm.haveItem('HiJump'),
                                                    sm.canFly()),
                                             sm.wor(sm.haveItem('SpeedBooster'), # spark
                                                    sm.canSpringBallJump()))),
                              sm.wand(sm.canHellRun('MainUpperNorfair', 0.5*mult),
                                      sm.haveItem('Morph'),
                                      sm.knowsNovaBoost())))

    @Cache.decorator
    def canClimbBubbleMountain(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('HiJump'),
                      sm.canFly(),
                      sm.haveItem('Ice'),
                      sm.knowsBubbleMountainWallJump())

    @Cache.decorator
    def canHellRunToSpeedBooster(self):
        sm = self.smbm
        return sm.canHellRun(**Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Speed Booster w/Speed' if sm.haveItem('SpeedBooster') else 'Bubble -> Speed Booster'])

    # with door color rando, there can be situations where you have to come back from the missile
    # loc without being able to open the speed booster door
    @Cache.decorator
    def canHellRunBackFromSpeedBoosterMissile(self):
        sm = self.smbm
        # require more health to count 1st hell run + way back is slower
        hellrun = 'MainUpperNorfair'
        tbl = Settings.hellRunsTable[hellrun]['Bubble -> Speed Booster']
        mult = tbl['mult']
        minE = tbl['minE']
        mult *= 0.66 if sm.haveItem('SpeedBooster') else 0.33 # speed booster usable for 1st hell run
        return sm.wor(RomPatches.has(RomPatches.SpeedAreaBlueDoors),
                      sm.traverse('SpeedBoosterHallRight'),
                      sm.canHellRun(hellrun, mult, minE))

    @Cache.decorator
    def canAccessDoubleChamberItems(self):
        sm = self.smbm
        hellRun = Settings.hellRunsTable['MainUpperNorfair']['Bubble -> Wave']
        return sm.wor(sm.wand(sm.traverse('SingleChamberRight'),
                              sm.canHellRun(**hellRun)),
                      sm.wand(sm.wor(sm.haveItem('HiJump'),
                                     sm.canSimpleShortCharge(),
                                     sm.canFly(),
                                     sm.knowsDoubleChamberWallJump()),
                              sm.canHellRun(hellRun['hellRun'], hellRun['mult']*0.8, hellRun['minE'])))

    @Cache.decorator
    def canExitWaveBeam(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Morph'), # exit through lower passage under the spikes
                      sm.wand(sm.wor(sm.haveItem('SpaceJump'), # exit through blue gate
                                     sm.haveItem('Grapple')),
                              sm.wor(sm.haveItem('Wave'),
                                     sm.wand(sm.heatProof(), # hell run + green gate glitch is too much
                                             sm.canBlueGateGlitch(),
                                             # if missiles were required to open the door, require two packs as no farming around
                                             sm.wor(sm.wnot(SMBool('Missile' in sm.traverse('DoubleChamberRight').items)),
                                                    sm.itemCountOk("Missile", 2),
                                                    sm.wand(sm.itemCountOk('Missile', 1), sm.itemCountOk('Super', 1)))))))

    def canExitCathedral(self, hellRun):
        # from top: can use bomb/powerbomb jumps
        # from bottom: can do a shinespark or use space jump
        #              can do it with highjump + wall jump
        #              can do it with only two wall jumps (the first one is delayed like on alcatraz)
        #              can do it with a spring ball jump from wall
        sm = self.smbm
        return sm.wand(sm.wor(sm.canHellRun(**hellRun),
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
        hellrun = 'MainUpperNorfair'
        tbl = Settings.hellRunsTable[hellrun]['Croc -> Norfair Entrance']
        mult = tbl['mult']
        minE = tbl['minE']
        if sm.haveItem('SpaceJump'):
            return sm.wand(sm.haveItem('SpaceJump'), sm.canHellRun(hellrun, mult*1.5, minE))
        if sm.haveItem('Grapple'):
            return sm.wand(sm.haveItem('Grapple'), sm.canHellRun(hellrun, mult*1.25, minE))
        speedHj = sm.wand(sm.haveItem('SpeedBooster'), sm.haveItem('HiJump')) # jump from the blocks below
        if speedHj:
            return sm.wand(speedHj, sm.canHellRun(hellrun, mult, minE))
        sbj = sm.wand(sm.haveItem('HiJump'), sm.canSpringBallJump()) # jump from the blocks below
        if sbj:
            return sm.wand(sbj, sm.canHellRun(hellrun, mult, minE))
        return sm.wand(sm.wor(sm.wand(sm.haveItem('SpeedBooster'),
                                      sm.knowsShortCharge()),
                              sm.wand(sm.canInfiniteBombJump(), # IBJ from lava...either have grav or freeze the enemy there if hellrunning (otherwise single DBJ at the end)
                                      sm.wor(sm.heatProof(),
                                             sm.haveItem('Gravity'),
                                             sm.haveItem('Ice')))),
                       sm.canHellRun(hellrun, mult*0.7, minE))

    @Cache.decorator
    def canHellRunBackFromGrappleEscape(self):
        sm = self.smbm
        # require more health to count 1st hell run from croc speedway bottom to here+hellrun back (which is faster)
        hellrun = 'MainUpperNorfair'
        tbl = Settings.hellRunsTable[hellrun]['Croc -> Norfair Entrance']
        mult = tbl['mult']
        minE = tbl['minE']
        mult *= 0.6
        return sm.canHellRun(hellrun, mult, minE)

    @Cache.decorator
    def canPassFrogSpeedwayRightToLeft(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('SpeedBooster'),
                      sm.wand(sm.knowsFrogSpeedwayWithoutSpeed(),
                              sm.haveItem('Wave'),
                              sm.wor(sm.haveItem('Spazer'),
                                     sm.haveItem('Plasma'))))

    @Cache.decorator
    def canPassFrogSpeedwayLeftToRight(self):
        sm = self.smbm
        return sm.haveItem('SpeedBooster')

    @Cache.decorator
    def canEnterNorfairReserveAreaFromBubbleMoutain(self):
        sm = self.smbm
        return sm.wand(sm.traverse('BubbleMountainTopLeft'),
                       sm.wor(sm.canFly(),
                              sm.haveItem('Ice'),
                              sm.wand(sm.haveItem('HiJump'),
                                      sm.knowsGetAroundWallJump()),
                              sm.wand(sm.canUseSpringBall(),
                                      sm.knowsSpringBallJumpFromWall())))

    @Cache.decorator
    def canEnterNorfairReserveAreaFromBubbleMoutainTop(self):
        sm = self.smbm
        return sm.wand(sm.traverse('BubbleMountainTopLeft'),
                       sm.wor(sm.haveItem('Grapple'),
                              sm.haveItem('SpaceJump'),
                              sm.knowsNorfairReserveDBoost()))

    @Cache.decorator
    def canPassLavaPit(self):
        sm = self.smbm
        nTanks4Dive = 8 / sm.getDmgReduction()[0]
        if sm.haveItem('HiJump').bool == False:
            nTanks4Dive = ceil(nTanks4Dive * 1.25)
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
        # to require one more CF if no heat protection because of distance to cover, wait times, acid...
        return sm.wand(sm.canHellRun(**Settings.hellRunsTable['LowerNorfair']['Entrance -> GT via Chozo']),
                       sm.canUsePowerBombs(),
                       sm.wor(RomPatches.has(RomPatches.LNChozoSJCheckDisabled), sm.haveItem('SpaceJump')))

    @Cache.decorator
    def canExitScrewAttackArea(self):
        sm = self.smbm

        return sm.wand(sm.canDestroyBombWalls(),
                       sm.wor(sm.canFly(),
                              sm.wand(sm.haveItem('HiJump'),
                                      sm.haveItem('SpeedBooster'),
                                      sm.wor(sm.wand(sm.haveItem('ScrewAttack'), sm.knowsScrewAttackExit()),
                                             sm.knowsScrewAttackExitWithoutScrew())),
                              sm.wand(sm.canUseSpringBall(),
                                      sm.knowsSpringBallJumpFromWall()),
                              sm.wand(sm.canSimpleShortCharge(), # fight GT and spark out
                                      sm.enoughStuffGT())))

    @Cache.decorator
    def canPassWorstRoom(self):
        sm = self.smbm
        return sm.wand(sm.canDestroyBombWalls(),
                       sm.canPassWorstRoomPirates(),
                       sm.wor(sm.haveItem("SpaceJump"),
                              sm.wand(sm.haveItem('Bomb'), sm.knowsInfiniteBombJump(), sm.heatProof()), # do not require suitless IBJ
                              sm.wand(sm.knowsWorstRoomIceCharge(),
                                      sm.haveItem('Ice'),
                                      sm.wor(sm.wand(sm.heatProof(), sm.canFireChargedShots()),
                                             sm.wand(sm.haveItem('Charge'), sm.haveItem('Plasma')))), # require firepower if suitless for ice strat
                              sm.wand(sm.knowsGetAroundWallJump(), sm.haveItem('HiJump')),
                              sm.knowsWorstRoomWallJump(),
                              sm.wand(sm.knowsSpringBallJumpFromWall(), sm.canUseSpringBall())))

    # checks mix of super missiles/health if heat proof. if not heat proof, just require an additional CF
    def canGoThroughLowerNorfairEnemy(self, nmyHealth, nbNmy, nmyHitDmg, supDmg=300.0):
        sm = self.smbm
        if sm.heatProof().bool == True:
            # supers only
            if sm.itemCount('Super')*5*supDmg >= nbNmy*nmyHealth:
                return SMBool(True, 0, items=['Super'])

            # - or with taking damage as well?
            (dmgRed, redItems) = sm.getDmgReduction(envDmg=False)
            dmg = nmyHitDmg / dmgRed
            if (sm.itemCount('Super')*5*supDmg)/nmyHealth + (sm.energyReserveCount()*100 - 2)/dmg >= nbNmy:
                # display all the available energy in the solver.
                return SMBool(True, 0, items=redItems+['Super', '{}-ETank - {}-Reserve'.format(self.smbm.itemCount('ETank'), self.smbm.itemCount('Reserve'))])
        else:
            # NOTE: assuming mult=1 for LN hellrun here. we can, because this function is only called
            # in "main LN" areas (ie not GT), which has a mult of 1
            mult = 1.0
            if sm.wand(RomPatches.has(RomPatches.ProgressiveSuits), sm.haveItem('Gravity')).bool == True:
                # half heat protection
                mult *= 2.0
            nCF = self.getLNRequiredCFs(mult)
            canCF = self.canCrystalFlash(nCF + 1)
            if canCF.bool == True:
                return canCF
        return sm.knowsDodgeLowerNorfairEnemies()

    def canPassRedKiHunters(self, n):
        sm = self.smbm
        return sm.wor(sm.haveItem('Plasma'),
                      sm.haveItem('ScrewAttack'),
                      sm.wand(sm.heatProof(), # this takes a loooong time ...
                              sm.wor(sm.haveItem('Spazer'),
                                     sm.haveItem('Ice'),
                                     sm.wand(sm.haveItem('Charge'),
                                             sm.haveItem('Wave')))),
                      sm.canGoThroughLowerNorfairEnemy(1800.0, float(n), 200.0))

    @Cache.decorator
    def canPassThreeMuskateers(self):
        sm = self.smbm
        return sm.canPassRedKiHunters(3)

    @Cache.decorator
    def canPassRedKiHunterStairs(self):
        sm = self.smbm
        return sm.canPassRedKiHunters(3)

    @Cache.decorator
    def canPassWastelandDessgeegas(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Plasma'),
                      sm.haveItem('ScrewAttack'),
                      sm.wand(sm.heatProof(), # this takes a loooong time ...
                              sm.wor(sm.haveItem('Spazer'),
                                     sm.wand(sm.haveItem('Charge'),
                                             sm.haveItem('Wave')))),
                      sm.itemCountOk('PowerBomb', 4),
                      sm.canGoThroughLowerNorfairEnemy(800.0, 3.0, 160.0))

    @Cache.decorator
    def canPassNinjaPirates(self):
        sm = self.smbm
        return sm.wor(sm.itemCountOk('Missile', 10),
                      sm.itemCountOk('Super', 2),
                      sm.haveItem('Plasma'),
                      sm.wand(sm.heatProof(), # no suitless slow kill
                              sm.wor(sm.haveItem('Spazer'),
                                     sm.wand(sm.canFireChargedShots(),
                                             sm.wor(sm.haveItem('Wave'),
                                                    sm.haveItem('Ice'))))),
                      sm.canShortCharge()) # echoes kill

    @Cache.decorator
    def canPassWorstRoomPirates(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('ScrewAttack'),
                      sm.itemCountOk('Missile', 6),
                      sm.itemCountOk('Super', 3),
                      sm.wand(sm.haveItem('Charge'),
                              sm.wor(sm.haveItem("Plasma"),
                                     sm.wand(sm.heatProof(), # do not require suitless long charged shot fights
                                             sm.wor(sm.haveItem('Spazer'),
                                                    sm.haveItem('Wave'),
                                                    sm.haveItem('Ice'))))),
                      sm.knowsDodgeLowerNorfairEnemies())

    # go though the pirates room filled with acid
    @Cache.decorator
    def canPassAmphitheaterReverse(self):
        sm = self.smbm
        dmgRed = sm.getDmgReduction()[0]
        nTanksGrav = 4 * 4/dmgRed
        nTanksNoGrav = 6 * 4/dmgRed
        return sm.wor(sm.wand(sm.haveItem('Gravity'),
                              sm.energyReserveCountOk(nTanksGrav, reserveRestriction=True)),
                      sm.wand(sm.energyReserveCountOk(nTanksNoGrav, reserveRestriction=True),
                              sm.knowsLavaDive())) # should be a good enough skill filter for acid wall jumps with no grav...

    @Cache.decorator
    def canGetBackFromRidleyZone(self):
        sm = self.smbm
        return sm.wand(sm.canUsePowerBombs(),
                       sm.wor(sm.canUseSpringBall(),
                              sm.canUseBombs(),
                              sm.itemCountOk('PowerBomb', 2),
                              sm.haveItem('ScrewAttack'),
                              sm.canShortCharge()), # speedball
                       # in escape you don't have PBs and can't shoot bomb blocks in long tunnels
                       # in wasteland and ki hunter room
                       sm.wnot(sm.canUseHyperBeam()))

    @Cache.decorator
    def canClimbRedTower(self):
        sm = self.smbm
        knowsRedTower = sm.knowsRedTowerClimb()
        # adjusted smbool depending on equipment
        adjustedKnows = SMBool(knowsRedTower.bool, knowsRedTower.difficulty, knowsRedTower.knows)
        # destroy rippers
        items = []
        if sm.haveItem('ScrewAttack'):
            items.append('ScrewAttack')
            adjustedKnows.difficulty *= 0.16
        elif sm.canUsePowerBombs():
            items.append('PowerBomb')
            adjustedKnows.difficulty *= 0.16
        elif sm.haveItem('Super'):
            items.append('Super')
            adjustedKnows.difficulty *= 0.33
        # space jump for the last part
        if sm.haveItem('SpaceJump'):
            items.append('SpaceJump')
            adjustedKnows.difficulty *= 0.5
        adjustedKnows.items = items
        return sm.wor(adjustedKnows,
                      sm.haveItem('Ice'))

    @Cache.decorator
    def canClimbBottomRedTower(self):
        sm = self.smbm
        return sm.wor(RomPatches.has(RomPatches.RedTowerLeftPassage),
                      sm.haveItem('HiJump'),
                      sm.haveItem('Ice'),
                      sm.canFly(),
                      sm.canShortCharge())

    @Cache.decorator
    def canGoUpMtEverest(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Gravity'),
                              sm.wor(sm.haveItem('Grapple'),
                                     sm.haveItem('SpeedBooster'),
                                     sm.canFly(),
                                     sm.wand(sm.knowsGravityJump(),
                                             sm.wor(sm.haveItem('HiJump'),
                                                    sm.knowsMtEverestGravJump())))),
                      sm.wand(sm.canDoSuitlessOuterMaridia(),
                              sm.wor(sm.haveItem('Grapple'),
                                     sm.canDoubleSpringBallJump())))

    @Cache.decorator
    def canPassMtEverest(self):
        sm = self.smbm
        return  sm.wor(sm.wand(sm.haveItem('Gravity'),
                               sm.wor(sm.haveItem('Grapple'),
                                      sm.haveItem('SpeedBooster'),
                                      sm.canFly(),
                                      sm.knowsGravityJump())),
                       sm.wand(sm.canDoSuitlessOuterMaridia(),
                               sm.wor(sm.haveItem('Grapple'),
                                      sm.wand(sm.haveItem('Ice'), sm.knowsTediousMountEverest(), sm.haveItem('Super')),
                                      sm.canDoubleSpringBallJump())))

    @Cache.decorator
    def canJumpUnderwater(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.knowsGravLessLevel1(),
                              sm.haveItem('HiJump')))

    @Cache.decorator
    def canDoSuitlessOuterMaridia(self):
        sm = self.smbm
        return sm.wand(sm.knowsGravLessLevel1(),
                       sm.haveItem('HiJump'),
                       sm.wor(sm.haveItem('Ice'),
                              sm.canSpringBallJump()))

    @Cache.decorator
    def canDoOuterMaridia(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.canDoSuitlessOuterMaridia())

    @Cache.decorator
    def canPassBotwoonHallway(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('SpeedBooster'),
                              sm.haveItem('Gravity')),
                      sm.wand(sm.knowsMochtroidClip(), sm.haveItem('Ice')),
                      sm.canCrystalFlashClip())

    @Cache.decorator
    def canDefeatBotwoon(self):
        sm = self.smbm
        hallway = sm.canPassBotwoonHallway()
        cfClip = 'CrystalFlashClip' in hallway.knows or 'SuitlessCrystalFlashClip' in hallway.knows
        return sm.wand(hallway,
                       sm.enoughStuffBotwoon(cfClip))

    # the sandpits from aqueduct
    @Cache.decorator
    def canAccessSandPits(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.haveItem('HiJump'),
                              sm.knowsGravLessLevel3()))

    @Cache.decorator
    def canReachCacatacAlleyFromBotowoon(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.knowsGravLessLevel2(),
                              sm.haveItem("HiJump"),
                              sm.wor(sm.haveItem('Grapple'),
                                     sm.haveItem('Ice'),
                                     sm.canDoubleSpringBallJump())))

    @Cache.decorator
    def canPassCacatacAlleyEastToWest(self):
        sm = self.smbm
        return sm.wand(Bosses.bossDead(sm, 'Draygon'),
                       sm.haveItem('Morph'),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.knowsGravLessLevel2(),
                                      sm.haveItem('HiJump'),
                                      sm.haveItem('SpaceJump'))))

    @Cache.decorator
    def canPassCacatacAlleyWestToEast(self):
        sm = self.smbm
        return sm.wand(Bosses.bossDead(sm, 'Draygon'),
                       sm.haveItem('Morph'),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.knowsGravLessLevel2(),
                                      sm.haveItem('HiJump'),
                                      sm.haveItem('SpaceJump'),
                                      sm.knowsCacAlleyUWJ())))

    @Cache.decorator
    def canGoThroughColosseumSuitless(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Grapple'),
                      sm.haveItem('SpaceJump'),
                      sm.wand(sm.haveItem('Ice'),
                              sm.energyReserveCountOk(int(7.0/sm.getDmgReduction(False)[0])), # mochtroid dmg
                              sm.knowsBotwoonToDraygonWithIce()))

    @Cache.decorator
    def canBotwoonExitToColosseum(self):
        sm = self.smbm
                       # traverse Botwoon Energy Tank Room
        return sm.wand(sm.wor(sm.wand(sm.haveItem('Gravity'), sm.haveItem('SpeedBooster')),
                              sm.wand(sm.haveItem('Morph'), sm.canJumpUnderwater())),
                       # after Botwoon Energy Tank Room
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.knowsGravLessLevel2(),
                                      sm.haveItem("HiJump"),
                                      # get to top right door
                                      sm.wor(sm.haveItem('Grapple'),
                                             sm.haveItem('Ice'), # climb mochtroids
                                             sm.wand(sm.canDoubleSpringBallJump(),
                                                     sm.haveItem('SpaceJump'))),
                                      sm.canGoThroughColosseumSuitless())))

    @Cache.decorator
    def canColosseumToBotwoonExit(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.knowsGravLessLevel2(),
                              sm.haveItem("HiJump"),
                              sm.canGoThroughColosseumSuitless()))

    @Cache.decorator
    def canClimbColosseum(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.knowsGravLessLevel2(),
                              sm.haveItem("HiJump"),
                              sm.wor(sm.haveItem('Grapple'),
                                     sm.haveItem('Ice'),
                                     sm.knowsPreciousRoomGravJumpExit())))

    @Cache.decorator
    def canClimbWestSandHole(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.haveItem('HiJump'),
                              sm.knowsGravLessLevel3(),
                              sm.wor(sm.haveItem('SpaceJump'),
                                     sm.canSpringBallJump(),
                                     sm.knowsWestSandHoleSuitlessWallJumps())))

    @Cache.decorator
    def canAccessItemsInWestSandHole(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('HiJump'), # vanilla strat
                              sm.canUseSpringBall()),
                      sm.wand(sm.haveItem('SpaceJump'), # alternate strat with possible double bomb jump but no difficult wj
                              sm.wor(sm.canUseSpringBall(),
                                     sm.canUseBombs())),
                      sm.wand(sm.canPassBombPassages(), # wjs and/or 3 tile mid air morph
                              sm.knowsMaridiaWallJumps()))

    @Cache.decorator
    def getDraygonConnection(self):
        return getAccessPoint('DraygonRoomOut').ConnectedTo

    @Cache.decorator
    def isVanillaDraygon(self):
        return SMBool(self.getDraygonConnection() == 'DraygonRoomIn')

    @Cache.decorator
    def canUseCrocRoomToChargeSpeed(self):
        sm = self.smbm
        crocRoom = getAccessPoint('Crocomire Room Top')
        speedway = getAccessPoint('Crocomire Speedway Bottom')
        return sm.wand(SMBool(crocRoom.ConnectedTo == 'Crocomire Speedway Bottom'),
                       crocRoom.traverse(sm),
                       speedway.traverse(sm))

    @Cache.decorator
    def canFightDraygon(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Gravity'),
                      sm.wand(sm.haveItem('HiJump'),
                              sm.wor(sm.knowsGravLessLevel2(),
                                     sm.knowsGravLessLevel3())))

    @Cache.decorator
    def canDraygonCrystalFlashSuit(self):
        sm = self.smbm
        return sm.wand(sm.canCrystalFlash(),
                       sm.knowsDraygonRoomCrystalFlash(),
                       # ask for 4 PB pack as an ugly workaround for
                       # a rando bug which can place a PB at space
                       # jump to "get you out" (this check is in
                       # PostAvailable condition of the Dray/Space
                       # Jump locs)
                       sm.itemCountOk('PowerBomb', 4))

    @Cache.decorator
    def canExitDraygonRoomWithGravity(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Gravity'),
                       sm.wor(sm.canFly(),
                              sm.knowsGravityJump(),
                              sm.wand(sm.haveItem('HiJump'),
                                      sm.haveItem('SpeedBooster'))))

    @Cache.decorator
    def canGrappleExitDraygon(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Grapple'),
                       sm.knowsDraygonRoomGrappleExit())

    @Cache.decorator
    def canExitDraygonVanilla(self):
        sm = self.smbm
        # to get out of draygon room:
        #   with gravity but without highjump/bomb/space jump: gravity jump
        #     to exit draygon room: grapple or crystal flash (for free shine spark)
        #     to exit precious room: spring ball jump, xray scope glitch or stored spark
        return sm.wor(sm.canExitDraygonRoomWithGravity(),
                      sm.wand(sm.canDraygonCrystalFlashSuit(),
                              # use the spark either to exit draygon room or precious room
                              sm.wor(sm.canGrappleExitDraygon(),
                                     sm.wand(sm.haveItem('XRayScope'),
                                             sm.knowsPreciousRoomXRayExit()),
                                     sm.canSpringBallJump())),
                      # spark-less exit (no CF)
                      sm.wand(sm.canGrappleExitDraygon(),
                              sm.wor(sm.wand(sm.haveItem('XRayScope'),
                                             sm.knowsPreciousRoomXRayExit()),
                                     sm.canSpringBallJump())),
                      sm.canDoubleSpringBallJump())

    @Cache.decorator
    def canExitDraygonRandomized(self):
        sm = self.smbm
        # disregard precious room
        return sm.wor(sm.canExitDraygonRoomWithGravity(),
                      sm.canDraygonCrystalFlashSuit(),
                      sm.canGrappleExitDraygon(),
                      sm.canDoubleSpringBallJump())

    @Cache.decorator
    def canExitDraygon(self):
        sm = self.smbm
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
        suitlessRoomExit = sm.wand(sm.wnot(sm.haveItem('Gravity')),
                                   sm.canJumpUnderwater(),
                                   sm.canSpringBallJump())
        if suitlessRoomExit.bool == False:
            if self.getDraygonConnection() == 'KraidRoomIn':
                suitlessRoomExit = sm.canShortCharge() # charge spark in kraid's room
            elif self.getDraygonConnection() == 'RidleyRoomIn':
                suitlessRoomExit = sm.wand(sm.haveItem('XRayScope'), # get doorstuck in compatible transition
                                           sm.knowsPreciousRoomXRayExit())
        return sm.wor(sm.wand(sm.haveItem('Gravity'),
                              sm.wor(sm.canFly(),
                                     sm.knowsGravityJump(),
                                     sm.haveItem('HiJump'))),
                      suitlessRoomExit)

    @Cache.decorator
    def canExitPreciousRoom(self):
        if self.isVanillaDraygon():
            return self.canExitPreciousRoomVanilla()
        else:
            return self.canExitPreciousRoomRandomized()

    @Cache.decorator
    def canPassDachoraRoom(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('SpeedBooster'), sm.canDestroyBombWalls())

    @Cache.decorator
    def canTraverseCrabTunnelLeftToRight(self):
        sm = self.smbm
        return sm.wand(sm.traverse('MainStreetBottomRight'),
                       sm.wor(sm.haveItem('Super'),
                              RomPatches.has(RomPatches.AreaRandoGatesOther)))

    @Cache.decorator
    def canAccessShaktoolFromPantsRoom(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Ice'), # puyo clip
                              sm.wor(sm.wand(sm.haveItem('Gravity'),
                                             sm.knowsPuyoClip()),
                                     sm.wand(sm.haveItem('Gravity'),
                                             sm.haveItem('XRayScope'),
                                             sm.knowsPuyoClipXRay()),
                                     sm.knowsSuitlessPuyoClip())),
                      sm.wand(sm.haveItem('Grapple'), # go through grapple block
                              sm.wor(sm.wand(sm.haveItem('Gravity'),
                                             sm.wor(sm.wor(sm.wand(sm.haveItem('HiJump'), sm.knowsAccessSpringBallWithHiJump()),
                                                           sm.haveItem('SpaceJump')),
                                                    sm.knowsAccessSpringBallWithGravJump(),
                                                    sm.wand(sm.haveItem('Bomb'),
                                                            sm.wor(sm.knowsAccessSpringBallWithBombJumps(),
                                                                   sm.wand(sm.haveItem('SpringBall'),
                                                                           sm.knowsAccessSpringBallWithSpringBallBombJumps()))),
                                                    sm.wand(sm.haveItem('SpringBall'), sm.knowsAccessSpringBallWithSpringBallJump()))),
                                     sm.wand(sm.haveItem('SpaceJump'), sm.knowsAccessSpringBallWithFlatley()))),
                      sm.wand(sm.haveItem('XRayScope'), sm.knowsAccessSpringBallWithXRayClimb()), # XRay climb
                      sm.canCrystalFlashClip())

    # only used for map completion objectives
    @Cache.decorator
    def canExploreAmphitheater(self):
        sm = self.smbm
        return sm.wand(sm.canPassAmphitheaterReverse(), sm.haveItem('SpaceJump'))

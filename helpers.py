
# the difficulties for each technics
from smbool import SMBool
from rom import RomPatches
from parameters import Settings, easy, medium, hard, harder, hardcore, mania

class Helpers(object):
    def __init__(self, smbm):
        self.smbm = smbm
        # cacheable functions sorted to avoid dependencies
        self.methodList = [
            'heatProof', 'canFly', 'canUseBombs', 'canOpenRedDoors',
            'canOpenYellowDoors', 'canUsePowerBombs',
            'canDestroyBombWalls', 'canPassBombPassages',
            'canAccessRedBrinstar', 'canAccessKraid', 'canAccessWs', 'canAccessHeatedNorfair',
            'canAccessCrocomire', 'enoughStuffCroc', 'canDefeatCrocomire',
            'canAccessLowerNorfair', 'canPassWorstRoom', 'canAccessOuterMaridia',
            'canDoSuitlessMaridia', 'canPassMtEverest',
            'enoughStuffBotwoon', 'canDefeatBotwoon'
        ]

    # return bool
    def haveItemCount(self, item, count):
        return self.smbm.itemCount(item) >= count

    # return integer
    def energyReserveCount(self):
        return self.smbm.itemCount('ETank') + self.smbm.itemCount('Reserve')

    def energyReserveCountOkDiff(self, difficulties, mult=1.0):
        if difficulties is None or len(difficulties) == 0:
            return SMBool(False)
        def f(difficulty):
            return self.smbm.energyReserveCountOk(difficulty[0]*mult, difficulty=difficulty[1])
        result = reduce(lambda result, difficulty: self.smbm.wor(result, f(difficulty)),
                        difficulties[1:], f(difficulties[0]))
        return result

    def energyReserveCountOkHellRun(self, hellRunName, mult=1.0):
        difficulties = Settings.hellRuns[hellRunName]
        result = self.energyReserveCountOkDiff(difficulties, mult)

        if self.smbm.getBool(result) == True:
            result = self.smbm.internal2SMBool(result)
            result.knows = [hellRunName+'HellRun']
        return result

    def energyReserveCountOkHardRoom(self, roomName, mult=1.0):
        difficulties = Settings.hardRooms[roomName]
        mult = 1.0
        if self.heatProof(): # env dmg reduction
            mult = 2.0
        result = self.energyReserveCountOkDiff(difficulties, mult)

        if self.smbm.getBool(result) == True:
            result = self.smbm.internal2SMBool(result)
            result.knows = ['HardRoom-'+roomName]
        return result

    def heatProof(self):
        return self.smbm.wor(self.smbm.haveItem('Varia'),
                             self.smbm.wand(self.smbm.wnot(RomPatches.has(RomPatches.NoGravityEnvProtection)),
                                            self.smbm.haveItem('Gravity')))

    def canHellRun(self, hellRun, mult=1.0):
        isHeatProof = self.smbm.heatProof()
        if self.smbm.getBool(isHeatProof) == True:
            isHeatProof = self.smbm.internal2SMBool(isHeatProof)
            isHeatProof.difficulty = easy
            return isHeatProof
        elif self.energyReserveCount() >= 2:
            return self.energyReserveCountOkHellRun(hellRun, mult)
        else:
            return SMBool(False)

    def canFly(self):
        if self.smbm.getBool(self.smbm.haveItem('SpaceJump')) == True:
            return self.smbm.setSMBool(True, easy, ['SpaceJump'])
        elif self.smbm.getBool(self.smbm.wand(self.smbm.haveItem('Morph'),
                                              self.smbm.haveItem('Bomb'),
                                              self.smbm.knowsInfiniteBombJump())) == True:
            return self.smbm.knowsInfiniteBombJump()
        else:
            return SMBool(False)

    def canFlyDiagonally(self):
        if self.smbm.getBool(self.smbm.haveItem('SpaceJump')) == True:
            return self.smbm.setSMBool(True, easy, ['SpaceJump'])
        elif self.smbm.getBool(self.smbm.wand(self.smbm.haveItem('Morph'),
                                              self.smbm.haveItem('Bomb'),
                                              self.smbm.knowsDiagonalBombJump())) == True:
            return self.smbm.knowsDiagonalBombJump()
        else:
            return self.smbm.setSMBool(False)

    def canUseBombs(self):
        return self.smbm.wand(self.smbm.haveItem('Morph'), self.smbm.haveItem('Bomb'))

    def canOpenRedDoors(self):
        return self.smbm.wor(self.smbm.haveItem('Missile'), self.smbm.haveItem('Super'))

    def canOpenGreenDoors(self):
        return self.smbm.haveItem('Super')

    def canOpenYellowDoors(self):
        return self.smbm.wand(self.smbm.haveItem('Morph'), self.smbm.haveItem('PowerBomb'))

    def canUsePowerBombs(self):
        return self.smbm.canOpenYellowDoors()

    def canDestroyBombWalls(self):
        return self.smbm.wor(self.smbm.wand(self.smbm.haveItem('Morph'),
                                            self.smbm.wor(self.smbm.haveItem('Bomb'),
                                                          self.smbm.haveItem('PowerBomb'))),
                             self.smbm.haveItem('ScrewAttack'))

    def canEnterAndLeaveGauntlet(self):
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
        return self.smbm.wand(self.smbm.wor(self.smbm.canFly(),
                                            self.smbm.haveItem('SpeedBooster'),
                                            self.smbm.wand(self.smbm.knowsHiJumpGauntletAccess(),
                                                           self.smbm.haveItem('HiJump')),
                                            self.smbm.knowsHiJumpLessGauntletAccess()),
                              self.smbm.wor(self.smbm.haveItem('ScrewAttack'),
                                            self.smbm.wor(self.smbm.wand(self.energyReserveCountOkHardRoom('Gauntlet'),
                                                                         self.smbm.wand(self.smbm.canUsePowerBombs(),
                                                                                        self.smbm.wor(self.smbm.itemCountOk('PowerBomb', 2),
                                                                                                      self.smbm.wand(self.smbm.haveItem('SpeedBooster'),
                                                                                                                     self.smbm.energyReserveCountOk(2))))),
                                                          self.smbm.wand(self.energyReserveCountOkHardRoom('Gauntlet', 0.5),
                                                                         self.smbm.canUseBombs()))))

    def canPassBombPassages(self):
        return self.smbm.wor(self.smbm.canUseBombs(),
                             self.smbm.canUsePowerBombs())

    def canAccessRedBrinstar(self):
        # EXPLAINED: we can go from Landing Site to Red Tower using two different paths:
        #             -break the bomb wall at left of Parlor and Alcatraz,
        #              open red door at Green Brinstar Main Shaft,
        #              morph at the lower part of Big Pink then use a super on the green door
        #             -open green door at the right of Landing Site, then open the yellow
        #              door at Crateria Keyhunter room
        return self.smbm.wand(self.smbm.haveItem('Super'),
                              self.smbm.wor(self.smbm.wand(self.smbm.wor(self.smbm.canDestroyBombWalls(),
                                                                         self.smbm.wand(self.smbm.haveItem('SpeedBooster'), self.smbm.knowsSimpleShortCharge())),
                                                           self.smbm.haveItem('Morph')),
                                            self.smbm.canUsePowerBombs()))

    def canAccessKraid(self):
        # EXPLAINED: from Red Tower we have to go to Warehouse Entrance, and there we have to
        #            access the upper right platform with either:
        #             -hijump boots (easy regular way)
        #             -fly (space jump or infinite bomb jump)
        #             -know how to wall jump on the platform without the hijump boots
        #            then we have to break a bomb block at Warehouse Zeela room
        return self.smbm.wand(self.smbm.canAccessRedBrinstar(),
                              self.smbm.wor(self.smbm.haveItem('HiJump'),
                                            self.smbm.canFly(),
                                            self.smbm.knowsEarlyKraid()),
                              self.smbm.canPassBombPassages())

    def canAccessWs(self):
        # EXPLAINED: from Landing Site we open the green door on the right, then in Crateria
        #            Keyhunter room we open the yellow door on the right to the Moat.
        #            In the Moat we can either:
        #             -use grapple or space jump (easy way)
        #             -do a continuous wall jump (https://www.youtube.com/watch?v=4HVhTwwax6g)
        #             -do a diagonal bomb jump from the middle platform (https://www.youtube.com/watch?v=5NRqQ7RbK3A&t=10m58s)
        #             -do a short charge from the Keyhunter room (https://www.youtube.com/watch?v=kFAYji2gFok)
        #             -do a gravity jump from below the right platform
        #             -do a mock ball and a bounce ball (https://www.youtube.com/watch?v=WYxtRF--834)
        return self.smbm.wand(self.smbm.haveItem('Super'),
                              self.smbm.canUsePowerBombs(),
                              self.smbm.wor(self.smbm.wor(self.smbm.haveItem('Grapple'),
                                                          self.smbm.haveItem('SpaceJump'),
                                                          self.smbm.knowsContinuousWallJump()),
                                            self.smbm.wor(self.smbm.wand(self.smbm.knowsDiagonalBombJump(),
                                                                         self.smbm.canUseBombs()),
                                                          self.smbm.wand(self.smbm.knowsSimpleShortCharge(),
                                                                         self.smbm.haveItem('SpeedBooster')),
                                                          self.smbm.haveItem('Gravity'),
                                                          self.smbm.wand(self.smbm.knowsMockballWs(),
                                                                         self.smbm.haveItem('Morph'),
                                                                         self.smbm.haveItem('SpringBall')))))

    def canAccessHeatedNorfair(self):
        # EXPLAINED: from Red Tower, to go to Bubble Mountain we have to pass through
        #            heated rooms, which requires a hell run if we don't have gravity.
        #            this test is then used to access Speed, Norfair Reserve Tank, Wave and Crocomire
        #            as they are all hellruns from Bubble Mountain.
        return self.smbm.wand(self.smbm.canAccessRedBrinstar(),
                              self.smbm.wor(self.smbm.haveItem('SpeedBooster'), # frog speedway
                                            # go through cathedral
                                            RomPatches.has(RomPatches.CathedralEntranceWallJump),
                                            self.smbm.haveItem('HiJump'),
                                            self.smbm.canFly()),
                              self.canHellRun('MainUpperNorfair'))

    def canAccessNorfairReserve(self):
        return self.smbm.wand(self.smbm.canAccessHeatedNorfair(),
                              self.smbm.wor(self.smbm.wor(self.smbm.canFly(),
                                                          self.smbm.haveItem('Grapple'),
                                                          self.smbm.wand(self.smbm.haveItem('HiJump'),
                                                                         self.smbm.knowsGetAroundWallJump())),
                                            self.smbm.wor(self.smbm.haveItem('Ice'),
                                                          self.smbm.wand(self.smbm.haveItem('SpringBall'),
                                                                         self.smbm.knowsSpringBallJumpFromWall()))))

    def canAccessCrocomire(self):
        # EXPLAINED: two options there, either:
        #             -from Bubble Mountain, hellrun to Crocomire's room. at Upper Norfair
        #              Farming room there's a blue gate which requires a gate glitch if no wave
        #             -the regular way, from Red Tower, power bomb in Ice Beam Gate room,
        #              then speed booster in Crocomire Speedway (easy hell run if no varia
        #              as we only have to go in straight line, so two ETanks are required)
        return self.smbm.wor(self.smbm.wand(self.smbm.canAccessHeatedNorfair(),
                                            self.smbm.wor(self.smbm.knowsGreenGateGlitch(), self.smbm.haveItem('Wave'))),
                             self.smbm.wand(self.smbm.canAccessRedBrinstar(),
                                            self.smbm.canUsePowerBombs(),
                                            self.smbm.haveItem('SpeedBooster'),
                                            self.smbm.canHellRun('Ice', 2)))

    def canDefeatCrocomire(self):
        return self.smbm.wand(self.smbm.canAccessCrocomire(),
                              self.smbm.enoughStuffCroc())

    def canAccessLowerNorfair(self):
        # EXPLAINED: the randomizer never requires to pass it without the Varia suit.
        #            from Red Tower in Brinstar to access Lava Dive room we open the yellow door
        #            in Kronic Boost room with a power bomb then pass the Lava Dive room.
        #            To pass Lava Dive room, either:
        #             -have gravity suit and space jump (easy way)
        #             -have gravity and perform a gravity jump
        #             -have hijump boots and knows the Lava Dive wall jumps, the wall jumps are
        #              a little easier with Ice and Plasma as we can freeze the Funes, we need
        #              at least three ETanks to do it without gravity
        nTanks4Dive = 3
        if self.smbm.getBool(self.smbm.heatProof()) == False:
            nTanks4Dive = 8
        return self.smbm.wand(self.canHellRun('LowerNorfair'),
                              self.smbm.canAccessRedBrinstar(),
                              self.smbm.canUsePowerBombs(),
                              self.smbm.wor(self.smbm.wand(self.smbm.haveItem('Gravity'), self.smbm.haveItem('SpaceJump')),
                                            self.smbm.wand(self.smbm.knowsGravityJump(), self.smbm.haveItem('Gravity')),
                                            self.smbm.wand(self.smbm.wor(self.smbm.wand(self.smbm.knowsLavaDive(),
                                                                                        self.smbm.haveItem('HiJump')),
                                                                         self.smbm.knowsLavaDiveNoHiJump()),
                                                           self.smbm.energyReserveCountOk(nTanks4Dive))))

    def canPassWorstRoom(self):
        # https://www.youtube.com/watch?v=gfmEDDmSvn4
        return self.smbm.wand(self.smbm.canAccessLowerNorfair(),
                              self.smbm.wor(self.smbm.canFly(),
                                            self.smbm.wand(self.smbm.knowsWorstRoomIceCharge(),
                                                           self.smbm.haveItem('Ice'),
                                                           self.smbm.haveItem('Charge')),
                                            self.smbm.wand(self.smbm.knowsGetAroundWallJump(),
                                                           self.smbm.haveItem('HiJump')),
                                            self.smbm.wand(self.smbm.knowsSpringBallJumpFromWall(),
                                                           self.smbm.haveItem('SpringBall'))))

    def canPassMtEverest(self):
        return self.smbm.wand(self.smbm.canAccessOuterMaridia(),
                              self.smbm.wor(self.smbm.wand(self.smbm.haveItem('Gravity'),
                                                           self.smbm.wor(self.smbm.wor(self.smbm.haveItem('Grapple'),
                                                                                       self.smbm.haveItem('SpeedBooster')),
                                                                         self.smbm.wor(self.smbm.canFly(),
                                                                                       self.smbm.knowsGravityJump(),
                                                                                       self.smbm.wand(self.smbm.haveItem('Ice'),
                                                                                                      self.smbm.knowsTediousMountEverest())))),
                                            self.smbm.canDoSuitlessMaridia()))

    def canAccessOuterMaridia(self):
        # EXPLAINED: access Red Tower in red brinstar,
        #            power bomb to destroy the tunnel at Glass Tunnel,
        #            then to climb up Main Street, either:
        #             -have gravity (easy regular way)
        #             -freeze the enemies to jump on them, but without a strong gun in the upper left
        #              when the Sciser comes down you don't have enough time to hit it several times
        #              to freeze it, as such you have to either:
        #               -use the first Sciser from the ground and wait for it to come all the way up
        #               -do a double jump with spring ball
        return self.smbm.wand(self.smbm.canAccessRedBrinstar(),
                              self.smbm.canUsePowerBombs(),
                              self.smbm.wor(self.smbm.haveItem('Gravity'),
                                            self.smbm.wand(self.smbm.haveItem('HiJump'),
                                                           self.smbm.haveItem('Ice'),
                                                           self.smbm.knowsGravLessLevel1())))

    def canAccessInnerMaridia(self):
        # EXPLAINED: this is the easy regular way:
        #            access Red Tower in red brinstar,
        #            power bomb to destroy the tunnel at Glass Tunnel,
        #            gravity suit to move freely under water,
        #            at Mt Everest, no need for grapple to access upper right door:
        #            https://www.youtube.com/watch?v=2GPx-6ARSIw&t=2m28s
        return self.smbm.wand(self.smbm.canAccessRedBrinstar(),
                              self.smbm.canUsePowerBombs(),
                              self.smbm.wor(self.smbm.haveItem('Gravity'),
                                            self.smbm.wand(self.smbm.haveItem('HiJump'),
                                                           self.smbm.haveItem('Ice'),
                                                           self.smbm.knowsGravLessLevel3())))

    def canDoSuitlessMaridia(self):
        # EXPLAINED: this is the harder way if no gravity,
        #            reach the Mt Everest then use the grapple to access the upper right door.
        #            it can also be done without gravity nor grapple but the randomizer will never
        #            require it (https://www.youtube.com/watch?v=lsbnUKcblPk).
        return self.smbm.wand(self.smbm.canAccessOuterMaridia(),
                              self.smbm.wor(self.smbm.haveItem('Grapple'),
                                            self.smbm.knowsTediousMountEverest()))

    def canDefeatBotwoon(self):
        # EXPLAINED: access Aqueduct, either with or without gravity suit,
        #            then in Botwoon Hallway, either:
        #             -use regular speedbooster (with gravity)
        #             -do a mochtroidclip (https://www.youtube.com/watch?v=1z_TQu1Jf1I&t=20m28s)
        return self.smbm.wand(self.smbm.enoughStuffBotwoon(),
                              self.smbm.canPassMtEverest(),
                              self.smbm.wor(self.smbm.wand(self.smbm.haveItem('SpeedBooster'),
                                                           self.smbm.haveItem('Gravity')),
                                            self.smbm.wand(self.smbm.knowsMochtroidClip(),
                                                           self.smbm.haveItem('Ice'))))

    def canCrystalFlash(self):
        return self.smbm.wand(self.smbm.canUsePowerBombs(),
                              self.smbm.itemCountOk('Missile', 2),
                              self.smbm.itemCountOk('Super', 2),
                              self.smbm.itemCountOk('PowerBomb', 3))

    def canDefeatDraygon(self):
        return self.smbm.wand(self.smbm.canDefeatBotwoon(),
                              self.smbm.wor(self.smbm.haveItem('Gravity'),
                                            self.smbm.wand(self.smbm.knowsGravLessLevel2(),
                                                           self.smbm.haveItem('Grapple')))) # HiJump and Ice are checked in canDefeatBotwoon if suitless

    def getBeamDamage(self):
        standardDamage = 20

        if self.smbm.getBool(self.smbm.wand(self.smbm.haveItem('Ice'),
                                            self.smbm.haveItem('Wave'),
                                            self.smbm.haveItem('Plasma'))) == True:
            standardDamage = 300
        elif self.smbm.getBool(self.smbm.wand(self.smbm.haveItem('Wave'),
                                              self.smbm.haveItem('Plasma'))) == True:
            standardDamage = 250
        elif self.smbm.getBool(self.smbm.wand(self.smbm.haveItem('Ice'),
                                              self.smbm.haveItem('Plasma'))) == True:
            standardDamage = 200
        elif self.smbm.getBool(self.smbm.haveItem('Plasma')) == True:
            standardDamage = 150
        elif self.smbm.getBool(self.smbm.wand(self.smbm.haveItem('Ice'),
                                              self.smbm.haveItem('Wave'),
                                              self.smbm.haveItem('Spazer'))) == True:
            standardDamage = 100
        elif self.smbm.getBool(self.smbm.wand(self.smbm.haveItem('Wave'),
                                              self.smbm.haveItem('Spazer'))) == True:
            standardDamage = 70
        elif self.smbm.getBool(self.smbm.wand(self.smbm.haveItem('Ice'),
                                              self.smbm.haveItem('Spazer'))) == True:
            standardDamage = 60
        elif self.smbm.getBool(self.smbm.wand(self.smbm.haveItem('Ice'),
                                              self.smbm.haveItem('Wave'))) == True:
            standardDamage = 60
        elif self.smbm.getBool(self.smbm.haveItem('Wave')) == True:
            standardDamage = 50
        elif self.smbm.getBool(self.smbm.haveItem('Spazer')) == True:
            standardDamage = 40
        elif self.smbm.getBool(self.smbm.haveItem('Ice')) == True:
            standardDamage = 30

        return standardDamage

    # returns a tuple with :
    #
    # - a floating point number : 0 if boss is unbeatable with
    # current equipment, and an ammo "margin" (ex : 1.5 means we have 50%
    # more firepower than absolutely necessary). Useful to compute boss
    # difficulty when not having charge. If player has charge, the actual
    # value is not useful, and is guaranteed to be > 2.
    #
    # - estimation of the fight duration in seconds (well not really, it
    # is if you fire and land shots perfectly and constantly), giving info
    # to compute boss fight difficulty
    def canInflictEnoughDamages(self, bossEnergy, doubleSuper=False, charge=True, power=False, givesDrops=True):
        # TODO: handle special beam attacks ? (http://deanyd.net/sm/index.php?title=Charge_Beam_Combos)

        # http://deanyd.net/sm/index.php?title=Damage
        standardDamage = 0
        if self.smbm.getBool(self.smbm.haveItem('Charge')) == True and charge == True:
            standardDamage = self.getBeamDamage()
        # charge triples the damage
        chargeDamage = standardDamage * 3.0

        # missile 100 damages, super missile 300 damages, PBs 200 dmg, 5 in each extension
        missilesAmount = self.smbm.itemCount('Missile') * 5
        missilesDamage = missilesAmount * 100
        supersAmount = self.smbm.itemCount('Super') * 5
        oneSuper = 300.0
        if doubleSuper == True:
            oneSuper *= 2
        supersDamage = supersAmount * oneSuper
        powerDamage = 0
        powerAmount = 0
        if power == True and self.smbm.getBool(self.smbm.haveItem('PowerBomb')) == True:
            powerAmount = self.smbm.itemCount('PowerBomb') * 5
            powerDamage = powerAmount * 200

        canBeatBoss = chargeDamage > 0 or givesDrops or (missilesDamage + supersDamage + powerDamage) >= bossEnergy
        if not canBeatBoss:
            return (0, 0)

        ammoMargin = (missilesDamage + supersDamage + powerDamage) / bossEnergy
        if chargeDamage > 0:
            ammoMargin += 2

        missilesDPS = Settings.algoSettings['missilesPerSecond'] * 100.0
        supersDPS = Settings.algoSettings['supersPerSecond'] * 300.0
        if doubleSuper == True:
            supersDPS *= 2
        if powerDamage > 0:
            powerDPS = Settings.algoSettings['powerBombsPerSecond'] * 200.0
        else:
            powerDPS = 0.0
        chargeDPS = chargeDamage * Settings.algoSettings['chargedShotsPerSecond']
        # print("chargeDPS=" + str(chargeDPS))
        dpsDict = {
            missilesDPS: (missilesAmount, 100.0),
            supersDPS: (supersAmount, oneSuper),
            powerDPS: (powerAmount, 200.0),
            # no boss will take more 10000 charged shots
            chargeDPS: (10000, chargeDamage)
        }
        secs = 0
        for dps in sorted(dpsDict, reverse=True):
            amount = dpsDict[dps][0]
            one = dpsDict[dps][1]
            if dps == 0 or one == 0 or amount == 0:
                continue
            fire = min(bossEnergy / one, amount)
            secs += fire * (one / dps)
            bossEnergy -= fire * one
            if bossEnergy <= 0:
                break
        if bossEnergy > 0:
            # print ('!! drops !! ')
            secs += bossEnergy * Settings.algoSettings['missileDropsPerMinute'] * 100 / 60
            # print('ammoMargin = ' + str(ammoMargin) + ', secs = ' + str(secs))

        return (ammoMargin, secs)

    def computeBossDifficulty(self, ammoMargin, secs, diffTbl):
        # actual fight duration :
        rate = None
        if 'Rate' in diffTbl:
            rate = float(diffTbl['Rate'])
        if rate is None:
            duration = 120.0
        else:
            duration = secs / rate
        # print('rate=' + str(rate) + ', duration=' + str(duration))
        suitsCoeff = 0.5
        if self.smbm.getBool(self.smbm.haveItem('Gravity')) == True:
            suitsCoeff = 2
        elif self.smbm.getBool(self.smbm.haveItem('Varia')) == True:
            suitsCoeff = 1
        energy = suitsCoeff * (1 + self.energyReserveCount())
        energyDict = None
        if 'Energy' in diffTbl:
            energyDict = diffTbl['Energy']
        difficulty = medium
        # get difficulty by energy
        if energyDict:
            energyDict = {float(k):float(v) for k,v in energyDict.items()}
            keyz = sorted(energyDict.keys())
            if len(keyz) > 0:
                current = keyz[0]
                sup = None
                difficulty = energyDict[current]
                for k in keyz:
                    if k > energy:
                        sup=k
                        break
                    current = k
                    difficulty = energyDict[k]
                # interpolate if we can
                if energy > current and sup is not None:
                    difficulty += (energyDict[sup] - difficulty)/(sup - current) * (energy - current)
    #    print("energy=" + str(energy) + ", base diff=" + str(difficulty))
        # adjust by fight duration
        difficulty *= (duration / 120)
        # and by ammo margin
        # only augment difficulty in case of no charge, don't lower it.
        # if we have charge, ammoMargin will have a huge value (see canInflictEnoughDamages),
        # so this does not apply
        diffAdjust = (1 - (ammoMargin - Settings.algoSettings['ammoMarginIfNoCharge']))
        if diffAdjust > 1:
            difficulty *= diffAdjust

        return difficulty

    def enoughStuffCroc(self):
        # say croc has ~5000 energy, and ignore its useless drops
        (ammoMargin, secs) = self.canInflictEnoughDamages(5000, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)
        self.smbm.curSMBool.difficulty = easy
        self.smbm.curSMBool.bool = True
        return self.smbm.getSMBoolCopy()

    def enoughStuffBotwoon(self):
        # say botwoon has 5000 energy : it is actually 3000 but account for missed shots
        (ammoMargin, secs) = self.canInflictEnoughDamages(5000, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)
        self.smbm.curSMBool.difficulty = easy
        self.smbm.curSMBool.bool = True
        return self.smbm.getSMBoolCopy()

    def enoughStuffsRidley(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(18000, doubleSuper=True, power=True, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)

        # print('RIDLEY', ammoMargin, secs)
        self.smbm.curSMBool.difficulty = self.computeBossDifficulty(ammoMargin, secs,
                                                                    Settings.bossesDifficulty['Ridley'])
        self.smbm.curSMBool.bool = True
        return self.smbm.getSMBoolCopy()

    def enoughStuffsKraid(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(1000)
        if ammoMargin == 0:
            return SMBool(False)
        #print('KRAID True ', ammoMargin, secs)
        self.smbm.curSMBool.difficulty = self.computeBossDifficulty(ammoMargin, secs,
                                                                    Settings.bossesDifficulty['Kraid'])
        self.smbm.curSMBool.bool = True
        return self.smbm.getSMBoolCopy()

    def enoughStuffsDraygon(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(6000)
        # print('DRAY', ammoMargin, secs)
        if ammoMargin > 0:
            fight = SMBool(True, self.computeBossDifficulty(ammoMargin, secs,
                                                            Settings.bossesDifficulty['Draygon']))
            if self.smbm.getBool(self.smbm.haveItem('Gravity')) == False:
                fight.difficulty *= Settings.algoSettings['draygonNoGravityMalus']
        else:
            fight = SMBool(False)
        return self.smbm.wor(fight,
                        self.smbm.wand(self.smbm.knowsDraygonGrappleKill(),
                                       self.smbm.haveItem('Grapple')),
                        self.smbm.wand(self.smbm.knowsMicrowaveDraygon(),
                                       self.smbm.haveItem('Plasma'),
                                       self.smbm.haveItem('Charge'),
                                       self.smbm.haveItem('XRayScope')),
                        self.smbm.wand(self.smbm.haveItem('Gravity'),
                                       self.smbm.knowsShortCharge(),
                                       self.smbm.haveItem('SpeedBooster')))

    def enoughStuffsPhantoon(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(2500, doubleSuper=True)
        if ammoMargin == 0:
            return SMBool(False)
        # print('PHANTOON', ammoMargin, secs)
        difficulty = self.computeBossDifficulty(ammoMargin, secs,
                                                Settings.bossesDifficulty['Phantoon'])
        hasCharge = self.smbm.getBool(self.smbm.haveItem('Charge'))
        if hasCharge or self.smbm.getBool(self.smbm.haveItem('ScrewAttack')) == True:
            difficulty /= Settings.algoSettings['phantoonFlamesAvoidBonus']
        elif not hasCharge and self.smbm.itemCount('Missile') <= 2: # few missiles is harder
            difficulty *= Settings.algoSettings['phantoonLowMissileMalus']
        fight = SMBool(True, difficulty)

        return self.smbm.wor(fight,
                             self.smbm.wand(self.smbm.knowsMicrowavePhantoon(),
                                            self.smbm.haveItem('Plasma'),
                                            self.smbm.haveItem('Charge'),
                                            self.smbm.haveItem('XRayScope')))

    def enoughStuffsMotherbrain(self):
        #print('MB')
        # MB1 can't be hit by charge beam
        (ammoMargin, secs) = self.canInflictEnoughDamages(3000, charge=False, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)

        # we actually don't give a shit about MB1 difficulty,
        # since we embark its health in the following calc
        (ammoMargin, secs) = self.canInflictEnoughDamages(18000 + 3000, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)

        # print('MB2', ammoMargin, secs)
        nTanks = self.smbm.ETankCount
        if self.smbm.getBool(self.smbm.haveItem('Varia')) == False:
            # "remove" 3 etanks (accounting for rainbow beam damage without varia)
            if nTanks < 6:
                return SMBool(False, 0)
            self.smbm.ETankCount -= 3
        elif nTanks < 3:
            return SMBool(False, 0)

        diff = self.computeBossDifficulty(ammoMargin, secs, Settings.bossesDifficulty['MotherBrain'])
        self.smbm.ETankCount = nTanks
        return SMBool(True, diff)

    def canPassMetroids(self):
        return self.smbm.wand(self.smbm.canOpenRedDoors(),
                              self.smbm.wor(self.smbm.haveItem('Ice'),
                                            # to avoid leaving tourian to refill power bombs
                                            self.smbm.itemCountOk('PowerBomb', 3)))

    def canPassZebetites(self):
        # account for one zebetite, refill may be necessary
        return self.smbm.wor(self.smbm.wand(self.smbm.haveItem('Ice'), self.smbm.knowsIceZebSkip()),
                             self.smbm.wand(self.smbm.haveItem('SpeedBooster'), self.smbm.knowsSpeedZebSkip()),
                             SMBool(self.canInflictEnoughDamages(1100, charge=False, givesDrops=False)[0] >= 1, 0))

    def enoughStuffTourian(self):
        return self.smbm.wand(self.canPassMetroids(),
                              self.canPassZebetites(),
                              self.enoughStuffsMotherbrain())

class Pickup:
    def __init__(self, majorsPickup, minorsPickup):
        self.majorsPickup = majorsPickup
        self.minorsPickup = minorsPickup

    def _enoughMinorTable(self, smbm, minorType):
        return smbm.haveItemCount(minorType, int(self.minorsPickup[minorType]))

    def enoughMinors(self, smbm, minorLocations):
        if self.minorsPickup == 'all':
            # need them all
            return len(minorLocations) == 0
        elif self.minorsPickup == 'any':
            return True
        else:
            canEnd = smbm.enoughStuffTourian().bool
            return (canEnd
                    and self._enoughMinorTable(smbm, 'Missile')
                    and self._enoughMinorTable(smbm, 'Super')
                    and self._enoughMinorTable(smbm, 'PowerBomb'))

    def enoughMajors(self, smbm, majorLocations):
        # the end condition
        if self.majorsPickup == 'all':
            return len(majorLocations) == 0
        elif self.majorsPickup == 'any':
            return True
        elif self.majorsPickup == 'minimal':
            canResistRainbow = (smbm.haveItemCount('ETank', 3)
                                and smbm.haveItem('Varia')) \
                               or smbm.haveItemCount('ETank', 6)
            
            return (smbm.haveItem('Morph')
                    # pass bomb block passages
                    and (smbm.haveItem('Bomb')
                         or smbm.haveItem('PowerBomb'))
                    # mother brain rainbow attack
                    and canResistRainbow
                    # lower norfair access
                    and (smbm.haveItem('Varia') or smbm.wnot(RomPatches.has(RomPatches.NoGravityEnvProtection)).bool) # gravity is checked below
                    # speed or ice to access botwoon
                    and (smbm.haveItem('SpeedBooster')
                         or smbm.haveItem('Ice'))
                    # draygon access
                    and smbm.haveItem('Gravity'))
        else:
            return False

class Bosses:
    # bosses helpers to know if they are dead
    areaBosses = {
        'Brinstar': 'Kraid',
        'Norfair': 'Ridley',
        'LowerNorfair': 'Ridley',
        'WreckedShip': 'Phantoon',
        'Maridia': 'Draygon'
    }

    golden4Dead = {
        'Kraid' : False,
        'Phantoon' : False,
        'Draygon' : False,
        'Ridley' : False
    }

    @staticmethod
    def reset():
        for boss in Bosses.golden4Dead:
            Bosses.golden4Dead[boss] = False

    @staticmethod
    def bossDead(boss):
        return SMBool(Bosses.golden4Dead[boss], 0)

    @staticmethod
    def beatBoss(boss):
        Bosses.golden4Dead[boss] = True

    @staticmethod
    def areaBossDead(area):
        if area not in Bosses.areaBosses:
            return True
        return Bosses.golden4Dead[Bosses.areaBosses[area]]

    @staticmethod
    def allBossesDead(smbm):
        return smbm.wand(Bosses.bossDead('Kraid'),
                         Bosses.bossDead('Phantoon'),
                         Bosses.bossDead('Draygon'),
                         Bosses.bossDead('Ridley'))

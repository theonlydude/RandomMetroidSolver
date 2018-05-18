
# the difficulties for each technics
from smbool import SMBool
from rom import RomPatches
from parameters import Settings, easy, medium, hard, harder, hardcore, mania

class Helpers(object):
    def __init__(self, smbm):
        self.smbm = smbm
        # cacheable functions sorted to avoid dependencies
        self.cachedMethods = [
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
        sm = self.smbm
        if sm.getBool(sm.haveItem('SpaceJump')) == True:
            return sm.setSMBool(True, easy, ['SpaceJump'])
        elif sm.getBool(sm.wand(sm.haveItem('Morph'),
                                sm.haveItem('Bomb'),
                                sm.knowsInfiniteBombJump())) == True:
            return sm.knowsInfiniteBombJump()
        else:
            return SMBool(False)

    def canFlyDiagonally(self):
        sm = self.smbm
        if sm.getBool(sm.haveItem('SpaceJump')) == True:
            return sm.setSMBool(True, easy, ['SpaceJump'])
        elif sm.getBool(sm.wand(sm.haveItem('Morph'),
                                sm.haveItem('Bomb'),
                                sm.knowsDiagonalBombJump())) == True:
            return sm.knowsDiagonalBombJump()
        else:
            return sm.setSMBool(False)

    def canUseBombs(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), sm.haveItem('Bomb'))

    def canOpenRedDoors(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Missile'), sm.haveItem('Super'))

    def canOpenGreenDoors(self):
        return self.smbm.haveItem('Super')

    def canOpenYellowDoors(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), sm.haveItem('PowerBomb'))

    def canUsePowerBombs(self):
        return self.smbm.canOpenYellowDoors()

    def canPassTerminatorBombWall(self, fromLandingSite=True):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('SpeedBooster'),
                              sm.wor(SMBool(not fromLandingSite, 0), sm.knowsSimpleShortCharge(), sm.knowsShortCharge())),
                      sm.canDestroyBombWalls())

    def canDestroyBombWalls(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Morph'),
                              sm.wor(sm.haveItem('Bomb'),
                                     sm.haveItem('PowerBomb'))),
                      sm.haveItem('ScrewAttack'))

    def canEnterAndLeaveGauntlet(self):
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
                              sm.wor(sm.wand(self.energyReserveCountOkHardRoom('Gauntlet'),
                                             sm.wand(sm.canUsePowerBombs(),
                                                     sm.wor(sm.itemCountOk('PowerBomb', 2),
                                                            sm.wand(sm.haveItem('SpeedBooster'),
                                                                    sm.energyReserveCountOk(2))))),
                                     sm.wand(self.energyReserveCountOkHardRoom('Gauntlet', 0.5),
                                             sm.canUseBombs()))))

    def canPassBombPassages(self):
        sm = self.smbm
        return sm.wor(sm.canUseBombs(),
                      sm.canUsePowerBombs())

    def canAccessRedBrinstar(self):
        sm = self.smbm
        # EXPLAINED: we can go from Landing Site to Red Tower using two different paths:
        #             -break the bomb wall at left of Parlor and Alcatraz,
        #              open red door at Green Brinstar Main Shaft,
        #              morph at the lower part of Big Pink then use a super on the green door
        #             -open green door at the right of Landing Site, then open the yellow
        #              door at Crateria Keyhunter room
        return sm.wand(sm.haveItem('Super'),
                       sm.wor(sm.wand(sm.canPassTerminatorBombWall(),
                                      sm.haveItem('Morph')),
                              sm.canUsePowerBombs()))

    def canAccessKraid(self):
        sm = self.smbm
        # EXPLAINED: from Red Tower we have to go to Warehouse Entrance, and there we have to
        #            access the upper right platform with either:
        #             -hijump boots (easy regular way)
        #             -fly (space jump or infinite bomb jump)
        #             -know how to wall jump on the platform without the hijump boots
        #            then we have to break a bomb block at Warehouse Zeela room
        return sm.wand(sm.canAccessRedBrinstar(),
                       sm.wor(sm.haveItem('HiJump'),
                              sm.canFly(),
                              sm.knowsEarlyKraid()),
                       sm.canPassBombPassages())

    def canAccessWs(self):
        sm = self.smbm
        # EXPLAINED: from Landing Site we open the green door on the right, then in Crateria
        #            Keyhunter room we open the yellow door on the right to the Moat.
        #            In the Moat we can either:
        #             -use grapple or space jump (easy way)
        #             -do a continuous wall jump (https://www.youtube.com/watch?v=4HVhTwwax6g)
        #             -do a diagonal bomb jump from the middle platform (https://www.youtube.com/watch?v=5NRqQ7RbK3A&t=10m58s)
        #             -do a short charge from the Keyhunter room (https://www.youtube.com/watch?v=kFAYji2gFok)
        #             -do a gravity jump from below the right platform
        #             -do a mock ball and a bounce ball (https://www.youtube.com/watch?v=WYxtRF--834)
        return sm.wand(sm.haveItem('Super'),
                       sm.canUsePowerBombs(),
                       sm.wor(sm.wor(sm.haveItem('Grapple'),
                                     sm.haveItem('SpaceJump'),
                                     sm.knowsContinuousWallJump()),
                              sm.wor(sm.wand(sm.knowsDiagonalBombJump(),
                                             sm.canUseBombs()),
                                     sm.wand(sm.wor(sm.knowsSimpleShortCharge(),
                                                    sm.knowsShortCharge()),
                                             sm.haveItem('SpeedBooster')),
                                     sm.wor(sm.haveItem('Gravity'), # grav jump of forgotten highway
                                            sm.wand(sm.knowsGravLessLevel3(), sm.haveItem('HiJump'))), # forgotten highway suitless
                                     sm.wand(sm.knowsMockballWs(),
                                             sm.haveItem('Morph'),
                                             sm.haveItem('SpringBall')))))

    def canAccessHeatedNorfair(self):
        sm = self.smbm
        # EXPLAINED: from Red Tower, to go to Bubble Mountain we have to pass through
        #            heated rooms, which requires a hell run if we don't have gravity.
        #            this test is then used to access Speed, Norfair Reserve Tank, Wave and Crocomire
        #            as they are all hellruns from Bubble Mountain.
        return sm.wand(sm.canAccessRedBrinstar(),
                       sm.wor(sm.haveItem('SpeedBooster'), # frog speedway
                              # go through cathedral
                              RomPatches.has(RomPatches.CathedralEntranceWallJump),
                              sm.haveItem('HiJump'),
                              sm.canFly()),
                       self.canHellRun('MainUpperNorfair'))

    def canAccessNorfairReserve(self):
        sm = self.smbm
        return sm.wand(sm.canAccessHeatedNorfair(),
                       sm.wor(sm.wor(sm.canFly(),
                                     sm.haveItem('Grapple'),
                                     sm.wand(sm.haveItem('HiJump'),
                                             sm.knowsGetAroundWallJump())),
                              sm.wor(sm.haveItem('Ice'),
                                     sm.wand(sm.haveItem('SpringBall'),
                                             sm.knowsSpringBallJumpFromWall()))))

    def canAccessCrocomire(self):
        sm = self.smbm
        # EXPLAINED: two options there, either:
        #             -from Bubble Mountain, hellrun to Crocomire's room. at Upper Norfair
        #              Farming room there's a blue gate which requires a gate glitch if no wave
        #             -the regular way, from Red Tower, power bomb in Ice Beam Gate room,
        #              then speed booster in Crocomire Speedway (easy hell run if no varia
        #              as we only have to go in straight line, so two ETanks are required)
        return sm.wor(sm.wand(sm.canAccessHeatedNorfair(),
                              sm.wor(sm.knowsGreenGateGlitch(), sm.haveItem('Wave'))),
                      sm.wand(sm.canAccessRedBrinstar(),
                              sm.canUsePowerBombs(),
                              sm.haveItem('SpeedBooster'),
                              sm.canHellRun('Ice', 2)))

    def canDefeatCrocomire(self):
        sm = self.smbm
        return sm.wand(sm.canAccessCrocomire(),
                       sm.enoughStuffCroc())

    def canAccessLowerNorfair(self):
        sm = self.smbm
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
        if sm.getBool(sm.heatProof()) == False:
            nTanks4Dive = 8
        return sm.wand(self.canHellRun('LowerNorfair'),
                       sm.canAccessRedBrinstar(),
                       sm.canUsePowerBombs(),
                       sm.wor(sm.wand(sm.haveItem('Gravity'), sm.haveItem('SpaceJump')),
                              sm.wand(sm.knowsGravityJump(), sm.haveItem('Gravity')),
                              sm.wand(sm.wor(sm.wand(sm.knowsLavaDive(),
                                                     sm.haveItem('HiJump')),
                                             sm.knowsLavaDiveNoHiJump()),
                                      sm.energyReserveCountOk(nTanks4Dive))))

    def canPassWorstRoom(self):
        sm = self.smbm
        # https://www.youtube.com/watch?v=gfmEDDmSvn4
        return sm.wand(sm.canAccessLowerNorfair(),
                       sm.wor(sm.canFly(),
                              sm.wand(sm.knowsWorstRoomIceCharge(),
                                      sm.haveItem('Ice'),
                                      sm.haveItem('Charge')),
                              sm.wand(sm.knowsGetAroundWallJump(),
                                      sm.haveItem('HiJump')),
                              sm.wand(sm.knowsSpringBallJumpFromWall(),
                                      sm.haveItem('SpringBall'))))

    def canPassMtEverest(self):
        sm = self.smbm
        return sm.wand(sm.canAccessOuterMaridia(),
                       sm.wor(sm.wand(sm.haveItem('Gravity'),
                                      sm.wor(sm.wor(sm.haveItem('Grapple'),
                                                    sm.haveItem('SpeedBooster')),
                                             sm.wor(sm.canFly(),
                                                    sm.knowsGravityJump(),
                                                    sm.wand(sm.haveItem('Ice'),
                                                            sm.knowsTediousMountEverest())))),
                              sm.canDoSuitlessMaridia()))

    def canAccessOuterMaridia(self):
        sm = self.smbm
        # EXPLAINED: access Red Tower in red brinstar,
        #            power bomb to destroy the tunnel at Glass Tunnel,
        #            then to climb up Main Street, either:
        #             -have gravity (easy regular way)
        #             -freeze the enemies to jump on them
        return sm.wand(sm.canAccessRedBrinstar(),
                       sm.canUsePowerBombs(),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.haveItem('HiJump'),
                                      sm.haveItem('Ice'),
                                      sm.knowsGravLessLevel1())))

    def canAccessInnerMaridia(self):
        sm = self.smbm
        # EXPLAINED: this is the easy regular way:
        #            access Red Tower in red brinstar,
        #            power bomb to destroy the tunnel at Glass Tunnel,
        #            gravity suit to move freely under water,
        #            at Mt Everest, no need for grapple to access upper right door:
        #            https://www.youtube.com/watch?v=2GPx-6ARSIw&t=2m28s
        return sm.wand(sm.canAccessRedBrinstar(),
                       sm.canUsePowerBombs(),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.haveItem('HiJump'),
                                      sm.haveItem('Ice'),
                                      sm.knowsGravLessLevel3())))

    def canDoSuitlessMaridia(self):
        sm = self.smbm
        # EXPLAINED: this is the harder way if no gravity,
        #            reach the Mt Everest then use the grapple to access the upper right door.
        #            it can also be done without gravity nor grapple but the randomizer will never
        #            require it (https://www.youtube.com/watch?v=lsbnUKcblPk).
        return sm.wand(sm.canAccessOuterMaridia(),
                       sm.wor(sm.haveItem('Grapple'),
                              sm.knowsTediousMountEverest()))

    def canDefeatBotwoon(self):
        sm = self.smbm
        # EXPLAINED: access Aqueduct, either with or without gravity suit,
        #            then in Botwoon Hallway, either:
        #             -use regular speedbooster (with gravity)
        #             -do a mochtroidclip (https://www.youtube.com/watch?v=1z_TQu1Jf1I&t=20m28s)
        return sm.wand(sm.enoughStuffBotwoon(),
                       sm.canPassMtEverest(),
                       sm.wor(sm.wand(sm.haveItem('SpeedBooster'),
                                      sm.haveItem('Gravity')),
                              sm.wand(sm.knowsMochtroidClip(),
                                      sm.haveItem('Ice'))))

    def canCrystalFlash(self):
        sm = self.smbm
        return sm.wand(sm.canUsePowerBombs(),
                       sm.itemCountOk('Missile', 2),
                       sm.itemCountOk('Super', 2),
                       sm.itemCountOk('PowerBomb', 3))

    def canDefeatDraygon(self):
        sm = self.smbm
        return sm.wand(sm.canDefeatBotwoon(),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.knowsGravLessLevel2(),
                                      sm.haveItem('Grapple')))) # HiJump and Ice are checked in canDefeatBotwoon if suitless

    def canAccessDraygonFromMainStreet(self):
        sm = self.smbm
        return sm.wand(sm.canDefeatBotwoon(),
                       sm.wor(sm.haveItem('Gravity'),
                              sm.wand(sm.canDoSuitlessMaridia(), sm.knowsGravLessLevel2())))

    def getBeamDamage(self):
        sm = self.smbm
        standardDamage = 20

        if sm.getBool(sm.wand(sm.haveItem('Ice'),
                              sm.haveItem('Wave'),
                              sm.haveItem('Plasma'))) == True:
            standardDamage = 300
        elif sm.getBool(sm.wand(sm.haveItem('Wave'),
                                sm.haveItem('Plasma'))) == True:
            standardDamage = 250
        elif sm.getBool(sm.wand(sm.haveItem('Ice'),
                                sm.haveItem('Plasma'))) == True:
            standardDamage = 200
        elif sm.getBool(sm.haveItem('Plasma')) == True:
            standardDamage = 150
        elif sm.getBool(sm.wand(sm.haveItem('Ice'),
                                sm.haveItem('Wave'),
                                sm.haveItem('Spazer'))) == True:
            standardDamage = 100
        elif sm.getBool(sm.wand(sm.haveItem('Wave'),
                                sm.haveItem('Spazer'))) == True:
            standardDamage = 70
        elif sm.getBool(sm.wand(sm.haveItem('Ice'),
                                sm.haveItem('Spazer'))) == True:
            standardDamage = 60
        elif sm.getBool(sm.wand(sm.haveItem('Ice'),
                                sm.haveItem('Wave'))) == True:
            standardDamage = 60
        elif sm.getBool(sm.haveItem('Wave')) == True:
            standardDamage = 50
        elif sm.getBool(sm.haveItem('Spazer')) == True:
            standardDamage = 40
        elif sm.getBool(sm.haveItem('Ice')) == True:
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
        sm = self.smbm
        (ammoMargin, secs) = self.canInflictEnoughDamages(6000)
        # print('DRAY', ammoMargin, secs)
        if ammoMargin > 0:
            fight = SMBool(True, self.computeBossDifficulty(ammoMargin, secs,
                                                            Settings.bossesDifficulty['Draygon']))
            if sm.getBool(sm.haveItem('Gravity')) == False:
                fight.difficulty *= Settings.algoSettings['draygonNoGravityMalus']
        else:
            fight = SMBool(False)
        return sm.wor(fight,
                      sm.wand(sm.knowsDraygonGrappleKill(),
                              sm.haveItem('Grapple')),
                      sm.wand(sm.knowsMicrowaveDraygon(),
                              sm.haveItem('Plasma'),
                              sm.haveItem('Charge'),
                              sm.haveItem('XRayScope')),
                      sm.wand(sm.haveItem('Gravity'),
                              sm.knowsShortCharge(),
                              sm.haveItem('SpeedBooster')))

    def enoughStuffsPhantoon(self):
        sm = self.smbm
        (ammoMargin, secs) = self.canInflictEnoughDamages(2500, doubleSuper=True)
        if ammoMargin == 0:
            return SMBool(False)
        # print('PHANTOON', ammoMargin, secs)
        difficulty = self.computeBossDifficulty(ammoMargin, secs,
                                                Settings.bossesDifficulty['Phantoon'])
        hasCharge = sm.getBool(sm.haveItem('Charge'))
        if hasCharge or sm.getBool(sm.haveItem('ScrewAttack')) == True:
            difficulty /= Settings.algoSettings['phantoonFlamesAvoidBonus']
        elif not hasCharge and sm.itemCount('Missile') <= 2: # few missiles is harder
            difficulty *= Settings.algoSettings['phantoonLowMissileMalus']
        fight = SMBool(True, difficulty)

        return sm.wor(fight,
                      sm.wand(sm.knowsMicrowavePhantoon(),
                              sm.haveItem('Plasma'),
                              sm.haveItem('Charge'),
                              sm.haveItem('XRayScope')))

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
        sm = self.smbm
        return sm.wand(sm.canOpenRedDoors(),
                       sm.wor(sm.haveItem('Ice'),
                              # to avoid leaving tourian to refill power bombs
                              sm.itemCountOk('PowerBomb', 3)))

    def canPassZebetites(self):
        sm = self.smbm
        # account for one zebetite, refill may be necessary
        return sm.wor(sm.wand(sm.haveItem('Ice'), sm.knowsIceZebSkip()),
                      sm.wand(sm.haveItem('SpeedBooster'), sm.knowsSpeedZebSkip()),
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
        'Blue Brinstar': 'Kraid',
        'Green Brinstar': 'Kraid',
        'Pink Brinstar': 'Kraid',
        'Red Brinstar': 'Kraid',
        'Norfair': 'Ridley',
        'Bubble Norfair': 'Ridley',
        'Crocomire': 'Ridley',
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

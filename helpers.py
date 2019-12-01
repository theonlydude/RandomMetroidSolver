
import math
from functools import reduce
from smbool import SMBool
from rom import RomPatches
from parameters import Settings, easy, medium, hard, harder, hardcore, mania, diff2text
from cache import Cache

class Helpers(object):
    def __init__(self, smbm):
        self.smbm = smbm

    # return bool
    def haveItemCount(self, item, count):
        return self.smbm.itemCount(item) >= count

    # return integer
    @Cache.decorator
    def energyReserveCount(self):
        return self.smbm.itemCount('ETank') + self.smbm.itemCount('Reserve')

    def energyReserveCountOkDiff(self, difficulties, mult=1.0):
        if difficulties is None or len(difficulties) == 0:
            return SMBool(False)
        def f(difficulty):
            return self.smbm.energyReserveCountOk(int(round(difficulty[0] / mult)), difficulty=difficulty[1])
        result = reduce(lambda result, difficulty: self.smbm.wor(result, f(difficulty)),
                        difficulties[1:], f(difficulties[0]))
        return result

    def energyReserveCountOkHellRun(self, hellRunName, mult=1.0):
        difficulties = Settings.hellRuns[hellRunName]
        result = self.energyReserveCountOkDiff(difficulties, mult)

        if result == True:
            result.knows = [hellRunName+'HellRun']
        return result

    # gives damage reduction factor with the current suits
    # envDmg : if true (default) will return environmental damage reduction
    def getDmgReduction(self, envDmg=True):
        ret = 1.0
        sm = self.smbm
        hasVaria = sm.haveItem('Varia')
        hasGrav = sm.haveItem('Gravity')
        item = None
        if RomPatches.has(RomPatches.NoGravityEnvProtection):
            if hasVaria:
                item = 'Varia'
                if envDmg:
                    ret = 4.0
                else:
                    ret = 2.0
            if hasGrav and not envDmg:
                ret = 4.0
                item = 'Gravity'
        else:
            if hasVaria:
                ret = 2.0
                item = 'Varia'
            if hasGrav:
                ret = 4.0
                item = 'Gravity'
        return (ret, item)

    # higher values for mult means room is that much "easier" (HP mult)
    def energyReserveCountOkHardRoom(self, roomName, mult=1.0):
        difficulties = Settings.hardRooms[roomName]
        (dmgRed, item) = self.getDmgReduction()
        mult *= dmgRed
        result = self.energyReserveCountOkDiff(difficulties, mult)

        if result == True:
            result.knows = ['HardRoom-'+roomName]
            if dmgRed != 1.0:
                result.items.append(item)
        return result

    @Cache.decorator
    def heatProof(self):
        return self.smbm.wor(self.smbm.haveItem('Varia'),
                             self.smbm.wand(self.smbm.wnot(RomPatches.has(RomPatches.NoGravityEnvProtection)),
                                            self.smbm.haveItem('Gravity')))

    # higher values for mult means hell run is that much "easier" (HP mult)
    def canHellRun(self, hellRun, mult=1.0, minE=2):
        sm = self.smbm

        isHeatProof = sm.heatProof()
        if isHeatProof == True:
            return SMBool(isHeatProof.bool, easy, isHeatProof.knows, isHeatProof.items)
        elif self.energyReserveCount() >= minE:
            if hellRun != 'LowerNorfair':
                return self.energyReserveCountOkHellRun(hellRun, mult)
            else:
                tanks = self.energyReserveCount()
                multCF = mult
                if tanks >= 14:
                    multCF *= 2.0
                nCF = int(math.ceil(2/multCF))
                ret = sm.wand(self.energyReserveCountOkHellRun(hellRun, mult),
                              self.canCrystalFlash(nCF))
                if ret.bool == True:
                    if sm.haveItem('Gravity') == True:
                        ret.difficulty *= 0.7
                        ret.items.append('Gravity')
                    elif sm.haveItem('ScrewAttack') == True:
                        ret.difficulty *= 0.7
                        ret.items.append('ScrewAttack')
                #nPB = self.smbm.itemCount('PowerBomb')
                #print("canHellRun LN. tanks=" + str(tanks) + ", nCF=" + str(nCF) + ", nPB=" + str(nPB) + ", mult=" + str(mult) + ", heatProof=" + str(isHeatProof.bool) + ", ret=" + str(ret))
                return ret
        else:
            return SMBool(False)

    @Cache.decorator
    def canFly(self):
        sm = self.smbm
        if sm.haveItem('SpaceJump') == True:
            return SMBool(True, easy, items=['SpaceJump'])
        elif sm.canInfiniteBombJump() == True:
            return sm.knowsInfiniteBombJump()
        else:
            return SMBool(False)

    @Cache.decorator
    def canFlyDiagonally(self):
        sm = self.smbm
        if sm.haveItem('SpaceJump') == True:
            return SMBool(True, easy, items=['SpaceJump'])
        elif sm.wand(sm.haveItem('Morph'),
                     sm.haveItem('Bomb'),
                     sm.knowsDiagonalBombJump()) == True:
            return sm.knowsDiagonalBombJump()
        else:
            return SMBool(False)

    @Cache.decorator
    def canSimpleShortCharge(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('SpeedBooster'),
                       sm.wor(sm.knowsSimpleShortCharge(),
                              sm.knowsShortCharge()))

    @Cache.decorator
    def canShortCharge(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('SpeedBooster'), sm.knowsShortCharge())

    @Cache.decorator
    def canUseBombs(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), sm.haveItem('Bomb'))

    @Cache.decorator
    def canInfiniteBombJump(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), sm.haveItem('Bomb'), sm.knowsInfiniteBombJump())

    @Cache.decorator
    def canOpenRedDoors(self):
        sm = self.smbm
        return sm.wor(sm.haveItem('Missile'), sm.haveItem('Super'))

    @Cache.decorator
    def canOpenGreenDoors(self):
        return self.smbm.haveItem('Super')

    @Cache.decorator
    def canOpenYellowDoors(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'), sm.haveItem('PowerBomb'))

    @Cache.decorator
    def canUsePowerBombs(self):
        return self.smbm.canOpenYellowDoors()

    @Cache.decorator
    def canUseSpringBall(self):
        sm = self.smbm
        return sm.wand(sm.haveItem('Morph'),
                       sm.haveItem('SpringBall'))

    @Cache.decorator
    def canSpringBallJump(self):
        sm = self.smbm
        return sm.wand(sm.canUseSpringBall(),
                       sm.knowsSpringBallJump())

    @Cache.decorator
    def canDoubleSpringBallJump(self):
        sm = self.smbm
        return sm.wand(sm.canUseSpringBall(),
                       sm.haveItem('HiJump'),
                       sm.knowsDoubleSpringBallJump())

    def canPassTerminatorBombWall(self, fromLandingSite=True):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('SpeedBooster'),
                              sm.wor(SMBool(not fromLandingSite, 0), sm.knowsSimpleShortCharge(), sm.knowsShortCharge())),
                      sm.canDestroyBombWalls())

    @Cache.decorator
    def canDestroyBombWalls(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Morph'),
                              sm.wor(sm.haveItem('Bomb'),
                                     sm.haveItem('PowerBomb'))),
                      sm.haveItem('ScrewAttack'))

    @Cache.decorator
    def canDestroyBombWallsUnderwater(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Gravity'),
                              sm.canDestroyBombWalls()),
                      sm.wand(sm.haveItem('Morph'),
                              sm.wor(sm.haveItem('Bomb'),
                                     sm.haveItem('PowerBomb'))))

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

    @Cache.decorator
    def canPassBombPassages(self):
        sm = self.smbm
        return sm.wor(sm.canUseBombs(),
                      sm.canUsePowerBombs())

    def canCrystalFlash(self, n=1):
        sm = self.smbm
        return sm.wand(sm.canUsePowerBombs(),
                       sm.itemCountOk('Missile', 2*n),
                       sm.itemCountOk('Super', 2*n),
                       sm.itemCountOk('PowerBomb', 2*n+1))

    @Cache.decorator
    def getBeamDamage(self):
        sm = self.smbm
        standardDamage = 20

        if sm.wand(sm.haveItem('Ice'),
                   sm.haveItem('Wave'),
                   sm.haveItem('Plasma')) == True:
            standardDamage = 300
        elif sm.wand(sm.haveItem('Wave'),
                     sm.haveItem('Plasma')) == True:
            standardDamage = 250
        elif sm.wand(sm.haveItem('Ice'),
                     sm.haveItem('Plasma')) == True:
            standardDamage = 200
        elif sm.haveItem('Plasma') == True:
            standardDamage = 150
        elif sm.wand(sm.haveItem('Ice'),
                     sm.haveItem('Wave'),
                     sm.haveItem('Spazer')) == True:
            standardDamage = 100
        elif sm.wand(sm.haveItem('Wave'),
                     sm.haveItem('Spazer')) == True:
            standardDamage = 70
        elif sm.wand(sm.haveItem('Ice'),
                     sm.haveItem('Spazer')) == True:
            standardDamage = 60
        elif sm.wand(sm.haveItem('Ice'),
                     sm.haveItem('Wave')) == True:
            standardDamage = 60
        elif sm.haveItem('Wave') == True:
            standardDamage = 50
        elif sm.haveItem('Spazer') == True:
            standardDamage = 40
        elif sm.haveItem('Ice') == True:
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
    def canInflictEnoughDamages(self, bossEnergy, doubleSuper=False, charge=True, power=False, givesDrops=True, ignoreMissiles=False, ignoreSupers=False):
        # TODO: handle special beam attacks ? (http://deanyd.net/sm/index.php?title=Charge_Beam_Combos)
        sm = self.smbm

        # http://deanyd.net/sm/index.php?title=Damage
        standardDamage = 0
        if sm.haveItem('Charge') == True and charge == True:
            standardDamage = self.getBeamDamage()
        # charge triples the damage
        chargeDamage = standardDamage * 3.0

        # missile 100 damages, super missile 300 damages, PBs 200 dmg, 5 in each extension
        missilesAmount = sm.itemCount('Missile') * 5
        if ignoreMissiles == True:
            missilesDamage = 0
        else:
            missilesDamage = missilesAmount * 100
        supersAmount = sm.itemCount('Super') * 5
        if ignoreSupers == True:
            oneSuper = 0
        else:
            oneSuper = 300.0
        if doubleSuper == True:
            oneSuper *= 2
        supersDamage = supersAmount * oneSuper
        powerDamage = 0
        powerAmount = 0
        if power == True and sm.haveItem('PowerBomb') == True:
            powerAmount = sm.itemCount('PowerBomb') * 5
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

    # return diff score, or -1 if below minimum energy in diffTbl
    def computeBossDifficulty(self, ammoMargin, secs, diffTbl, energyDiff=0):
        sm = self.smbm

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
        if sm.haveItem('Gravity') == True:
            suitsCoeff = 2
        elif sm.haveItem('Varia') == True:
            suitsCoeff = 1
        energy = suitsCoeff * (1 + self.energyReserveCount() + energyDiff)
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
                if energy < current:
                    return -1
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

    @Cache.decorator
    def enoughStuffCroc(self):
        # say croc has ~5000 energy, and ignore its useless drops
        (ammoMargin, secs) = self.canInflictEnoughDamages(5000, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)
        else:
            return SMBool(True, easy)

    @Cache.decorator
    def enoughStuffBotwoon(self):
        # say botwoon has 4000 energy : it is actually 3000 but account for missed shots
        # 4000 to allow for low% botwoon without charge beam (10 - 10 | missiles - supers)
        # there is a setup to "never" miss a shot by only shooting him when he exits through the top left hole
        (ammoMargin, secs) = self.canInflictEnoughDamages(4000, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)
        else:
            return SMBool(True, easy)

    @Cache.decorator
    def enoughStuffGT(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(3000, ignoreMissiles=True) # requires 10 supers or charge for the fight
        if ammoMargin == 0:
            return SMBool(False)
        else:
            # TODO add energy check
            return SMBool(True, easy)

    @Cache.decorator
    def enoughStuffsRidley(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(18000, doubleSuper=True, power=True, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)

        # print('RIDLEY', ammoMargin, secs)
        diff = self.computeBossDifficulty(ammoMargin, secs,
                                          Settings.bossesDifficulty['Ridley'])
        if diff < 0:
            return SMBool(False)
        else:
            return SMBool(True, diff)

    @Cache.decorator
    def enoughStuffsKraid(self):
        sm = self.smbm
        (ammoMargin, secs) = self.canInflictEnoughDamages(1000)
        if ammoMargin == 0:
            return SMBool(False)
        #print('KRAID True ', ammoMargin, secs)
        diff = self.computeBossDifficulty(ammoMargin, secs,
                                          Settings.bossesDifficulty['Kraid'])
        if diff < 0:
            return SMBool(False)

        # need missile or super to open the eye door
        if sm.wor(sm.haveItem('Missile'), sm.haveItem('Super')) == False:
            return SMBool(False)
        else:
            return SMBool(True, diff)

    def adjustHealthDropDiff(self, difficulty):
        (dmgRed, item) = self.getDmgReduction(envDmg=False)
        # 2 is Varia suit, considered standard eqt for boss fights
        # there's certainly a smarter way to do this but...
        if dmgRed < 2:
            difficulty *= Settings.algoSettings['dmgReductionDifficultyFactor']
        elif dmgRed > 2:
            difficulty /= Settings.algoSettings['dmgReductionDifficultyFactor']
        return difficulty

    @Cache.decorator
    def enoughStuffsDraygon(self):
        sm = self.smbm
        (ammoMargin, secs) = self.canInflictEnoughDamages(6000)
        # print('DRAY', ammoMargin, secs)
        if ammoMargin > 0:
            diff = self.computeBossDifficulty(ammoMargin, secs,
                                              Settings.bossesDifficulty['Draygon'])
            if diff < 0:
                fight = SMBool(False)
            else:
                fight = SMBool(True, diff)
            if sm.haveItem('Gravity') == False:
                fight.difficulty *= Settings.algoSettings['draygonNoGravityMalus']
            fight.difficulty = self.adjustHealthDropDiff(fight.difficulty)
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
                              sm.knowsDraygonSparkKill(),
                              sm.haveItem('SpeedBooster')))

    @Cache.decorator
    def enoughStuffsPhantoon(self):
        sm = self.smbm
        (ammoMargin, secs) = self.canInflictEnoughDamages(2500, doubleSuper=True)
        if ammoMargin == 0:
            return SMBool(False)
        # print('PHANTOON', ammoMargin, secs)
        difficulty = self.computeBossDifficulty(ammoMargin, secs,
                                                Settings.bossesDifficulty['Phantoon'])
        if difficulty < 0:
            return SMBool(False)
        hasCharge = sm.haveItem('Charge')
        hasScrew = sm.haveItem('ScrewAttack')
        if hasScrew:
            difficulty /= Settings.algoSettings['phantoonFlamesAvoidBonusScrew']
        elif hasCharge:
            difficulty /= Settings.algoSettings['phantoonFlamesAvoidBonusCharge']
        elif not hasCharge and sm.itemCount('Missile') <= 2: # few missiles is harder
            difficulty *= Settings.algoSettings['phantoonLowMissileMalus']
        difficulty = self.adjustHealthDropDiff(difficulty)
        fight = SMBool(True, difficulty)

        return sm.wor(fight,
                      sm.wand(sm.knowsMicrowavePhantoon(),
                              sm.haveItem('Plasma'),
                              sm.haveItem('Charge'),
                              sm.haveItem('XRayScope')))

    def mbEtankCheck(self):
        sm = self.smbm
        nTanks = sm.energyReserveCount()
        energyDiff = 0
        if sm.haveItem('Varia') == False:
            # "remove" 3 etanks (accounting for rainbow beam damage without varia)
            if nTanks < 6:
                return (False, 0)
            energyDiff = -3
        elif nTanks < 3:
            return (False, 0)
        return (True, energyDiff)

    @Cache.decorator
    def enoughStuffsMotherbrain(self):
        sm = self.smbm
        # MB1 can't be hit by charge beam
        (ammoMargin, secs) = self.canInflictEnoughDamages(3000, charge=False, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)
        # requires 10-10 to break the glass
        if sm.itemCount('Missile') <= 1 or sm.itemCount('Super') <= 1:
            return SMBool(False)
        # we actually don't give a shit about MB1 difficulty,
        # since we embark its health in the following calc
        (ammoMargin, secs) = self.canInflictEnoughDamages(18000 + 3000, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)
        (possible, energyDiff) = self.mbEtankCheck()
        if possible == False:
            return SMBool(False)
        # print('MB2', ammoMargin, secs)
        #print("ammoMargin: {}, secs: {}, settings: {}, energyDiff: {}".format(ammoMargin, secs, Settings.bossesDifficulty['MotherBrain'], energyDiff))
        diff = self.computeBossDifficulty(ammoMargin, secs, Settings.bossesDifficulty['MotherBrain'], energyDiff)
        if diff < 0:
            return SMBool(False)
        return SMBool(True, diff)

    @Cache.decorator
    def canPassMetroids(self):
        sm = self.smbm
        return sm.wand(sm.canOpenRedDoors(),
                       sm.wor(sm.haveItem('Ice'),
                              # to avoid leaving tourian to refill power bombs
                              sm.itemCountOk('PowerBomb', 3)))

    @Cache.decorator
    def canPassZebetites(self):
        sm = self.smbm
        return sm.wor(sm.wand(sm.haveItem('Ice'), sm.knowsIceZebSkip()),
                      sm.wand(sm.haveItem('SpeedBooster'), sm.knowsSpeedZebSkip()),
                      # account for one zebetite, refill may be necessary
                      SMBool(self.canInflictEnoughDamages(1100, charge=False, givesDrops=False, ignoreSupers=True)[0] >= 1, 0))

    @Cache.decorator
    def enoughStuffTourian(self):
        sm = self.smbm
        ret = self.smbm.wand(sm.canPassMetroids(),
                             sm.canPassZebetites(),
                             sm.enoughStuffsMotherbrain())
        return ret

class Pickup:
    def __init__(self, itemsPickup):
        self.itemsPickup = itemsPickup
        self.minorsPickupMinimal = {
            'Missile' : 10,
            'Super' : 5,
            'PowerBomb' : 2
        }
    def _enoughMinorTable(self, smbm, minorType):
        return smbm.haveItemCount(minorType, int(self.minorsPickupMinimal[minorType]))

    def enoughMinors(self, smbm, minorLocations):
        if self.itemsPickup == 'all':
            # need them all
            return len(minorLocations) == 0
        elif self.itemsPickup == 'any':
            return True
        else:
            canEnd = smbm.enoughStuffTourian()
            return (canEnd
                    and self._enoughMinorTable(smbm, 'Missile')
                    and self._enoughMinorTable(smbm, 'Super')
                    and self._enoughMinorTable(smbm, 'PowerBomb'))

    def enoughMajors(self, smbm, majorLocations):
        # the end condition
        if self.itemsPickup == 'all':
            return len(majorLocations) == 0
        elif self.itemsPickup == 'any':
            return True
        elif self.itemsPickup == 'minimal':
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
                    and (smbm.haveItem('Varia') or smbm.wnot(RomPatches.has(RomPatches.NoGravityEnvProtection))) # gravity is checked below
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
        # classic areas
        'Brinstar': 'Kraid',
        'Norfair': 'Ridley',
        'LowerNorfair': 'Ridley',
        'WreckedShip': 'Phantoon',
        'Maridia': 'Draygon',
        # solver areas
        'Blue Brinstar': 'Kraid',
        'Brinstar Hills': 'Kraid',
        'Bubble Norfair': 'Ridley',
        'Bubble Norfair Bottom': 'Ridley',
        'Bubble Norfair Reserve': 'Ridley',
        'Bubble Norfair Speed': 'Ridley',
        'Bubble Norfair Wave': 'Ridley',
        'Crocomire': 'Ridley',
        'Green Brinstar': 'Kraid',
        'Green Brinstar Reserve': 'Kraid',
        'Lower Norfair After Amphitheater': 'Ridley',
        'Lower Norfair Before Amphitheater': 'Ridley',
        'Lower Norfair Screw Attack': 'Ridley',
        'Maridia Forgotten Highway': 'Draygon',
        'Maridia Green': 'Draygon',
        'Maridia Pink Bottom': 'Draygon',
        'Maridia Pink Top': 'Draygon',
        'Maridia Sandpits': 'Draygon',
        'Norfair Entrance': 'Ridley',
        'Norfair Grapple Escape': 'Ridley',
        'Norfair Ice': 'Ridley',
        'Pink Brinstar': 'Kraid',
        'Red Brinstar': 'Kraid',
        'Red Brinstar Top': 'Kraid',
        'Warehouse': 'Kraid',
        'WreckedShip': 'Phantoon',
        'WreckedShip Back': 'Phantoon',
        'WreckedShip Bottom': 'Phantoon',
        'WreckedShip Gravity': 'Phantoon',
        'WreckedShip Main': 'Phantoon',
        'WreckedShip Top': 'Phantoon'
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
        if boss in Bosses.golden4Dead:
            Bosses.golden4Dead[boss] = True

    @staticmethod
    def unbeatBoss(boss):
        if boss in Bosses.golden4Dead:
            Bosses.golden4Dead[boss] = False

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


def diffValue2txt(diff):
    last = 0
    for d in sorted(diff2text.keys()):
        if diff >= last and diff < d:
            return diff2text[last]
        last = d
    return None

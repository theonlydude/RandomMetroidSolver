# object to handle the smbools and optimize them

import copy
from functools import reduce

from smbool import SMBool
from rom import RomPatches
from parameters import Settings, easy, medium, hard, harder, hardcore, mania

class SMOptim(object):
    @staticmethod
    def factory(store='all'):
        # possible values: all, diff, bool
        # all: store the difficulty, knows and items used, bool result (solver)
        # diff: store the difficulty and the bool result (randomizer with difficulty target)
        # bool: store only the bool result (randomizer w/o difficulty target)
        if store not in ['all', 'diff', 'bool']:
            raise Exception("SMOptim::factory::invalid store param")

        if store == 'all':
            return SMOptimAll()
        elif store == 'diff':
            return SMOptimDiff()
        elif store == 'bool':
            return SMOptimBool()

    items = ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']
    countItems = ['ETank', 'Reserve', 'Missile', 'Super', 'PowerBomb']
    methodList = ['_heatProof', '_canFly', '_canFlyDiagonally', '_canUseBombs', '_canOpenRedDoors',
                  '_canOpenGreenDoors', '_canOpenYellowDoors', '_canUsePowerBombs',
                  '_canDestroyBombWalls', '_canEnterAndLeaveGauntlet', '_canPassBombPassages',
                  '_canAccessRedBrinstar', '_canAccessKraid', '_canAccessWs',
                  '_canAccessHeatedNorfair', '_canAccessCrocomire', '_canDefeatCrocomire',
                  '_canAccessLowerNorfair', '_canPassWorstRoom', '_canAccessOuterMaridia',
                  '_canAccessInnerMaridia', '_canDoSuitlessMaridia', '_canPassMtEverest',
                  '_canDefeatBotwoon', '_canCrystalFlash']

    def __init__(self):
        self.curSMBool = SMBool(False)
        self.createCacheFunctions()
        self.createItemsFunctions()
        self.createKnowsFunctions()
        self.resetItems()

    def resetSMBool(self):
        self.curSMBool.bool = False
        self.curSMBool.diff = 0
        self.curSMBool.items = []
        self.curSMBool.knows = []

    def getSMBool(self):
        return self.curSMBool

    def getSMBoolCopy(self):
        return SMBool(self.curSMBool.bool,
                      self.curSMBool.difficulty,
                      self.curSMBool.knows[:],
                      self.curSMBool.items[:])

    def setSMBool(self, bool, diff=0):
        self.curSMBool.bool = bool
        self.curSMBool.diff = diff

    def getBool(self, dummy):
        # get access to current smbool boolean (as internaly it can be (bool, diff) or bool)
        return self.curSMBool.bool

    def resetItems(self):
        # start without items
        for item in SMOptim.items:
            setattr(self, item, False)

        for item in SMOptim.countItems:
            setattr(self, item+'Count', 0)

        self.updateCache('reset', None)

    def updateCache(self, action, item):
        # reset: set last item added to None, recompute current
        if action == 'reset':
            self.lastItemAdded = None
            for fun in self.methodList:
                self.resetSMBool()
                getattr(self, fun)()
                setattr(self, fun+'SMBool', self.getSMBoolCopy())

        # add: copy current in bak, set lastItemAdded, recompute current
        elif action == 'add':
            self.lastItemAdded = item
            for fun in self.methodList:
                setattr(self, fun+'SMBoolbak', getattr(self, fun+'SMBool'))
                self.resetSMBool()
                getattr(self, fun)()
                setattr(self, fun+'SMBool', self.getSMBoolCopy())

        # remove: if item removed is last added, copy bak in current, set lastItemAdded to None
        elif action == 'remove':
            if self.lastItemAdded == item:
                self.lastItemAdded = None
                for fun in self.methodList:
                    setattr(self, fun+'SMBool', getattr(self, fun+'SMBoolbak'))
            else:
                self.lastItemAdded = None
                for fun in self.methodList:
                    self.resetSMBool()
                    getattr(self, fun)()
                    setattr(self, fun+'SMBool', self.getSMBoolCopy())

        #print("updateCache::{}: {}".format(fun, getattr(self, '_'+fun+'SMBool')))

    def addItem(self, item):
        # a new item is available
        #print("addItem: {} previous {}".format(item, getattr(self, item)))
        setattr(self, item, True)
        if item in self.countItems:
            setattr(self, item+'Count', getattr(self, item+'Count') + 1)

        self.updateCache('add', item)

    def removeItem(self, item):
        # randomizer removed an item
        #print("removeItem: {} previous {}".format(item, getattr(self, item)))
        if item in self.countItems:
            count = getattr(self, item+'Count') - 1
            setattr(self, item+'Count', count)
            if count == 0:
                setattr(self, item, False)
        else:
            setattr(self, item, False)
        #print("removeItem: {} {}".format(item, getattr(self, item)))

        self.updateCache('remove', item)

    def createCacheFunctions(self):
        for fun in self.methodList:
            setattr(self, fun[1:], lambda fun=fun: self.getCacheSMBool(fun+'SMBool'))

    def getCacheSMBool(self, fun):
        smb = getattr(self, fun)
        self.setSMBoolCache(smb)
        return smb

    def createItemsFunctions(self):
        # for each item we have a function haveItem (ex: haveBomb()) which take an
        # optional parameter: the difficulty
        for item in SMOptim.items:
            setattr(self, 'have'+item, lambda item=item, difficulty=0: self.haveItem(item, difficulty))

        for item in SMOptim.countItems:
            setattr(self, 'count'+item, lambda item=item: self.countItem(item))

    def createKnowsFunctions(self):
        # for each knows we have a function knowsKnows (ex: knowsAlcatrazEscape()) which
        # take no parameter
        from parameters import Knows, isKnows
        for knows in Knows.__dict__:
            if isKnows(knows):
                setattr(self, 'knows'+knows, lambda knows=knows: self.knowsKnows(knows,
                                                                                 (Knows.__dict__[knows].bool,
                                                                                  Knows.__dict__[knows].difficulty)))

    # all the functions from helpers (those starting with an _ are only called from other helpers)
    def haveItemCount(self, item, count):
        # return bool
        return self.itemCount(item) >= count

    def itemCount(self, item):
        # return integer
        return getattr(self, item+'Count')

    def energyReserveCount(self):
        # return integer
        return self.itemCount('ETank') + self.itemCount('Reserve')

    def energyReserveCountOkHellRun(self, hellRunName):
        difficulties = Settings.hellRuns[hellRunName]

        if difficulties is None or len(difficulties) == 0:
            return SMBool(False)

        # get a list: [(2, difficulty=hard), (4, difficulty=medium), (6, difficulty=easy)]
        def f(difficulty):
            return self.energyReserveCountOk(difficulty[0], difficulty=difficulty[1])
        result = reduce(lambda result, difficulty: self.wor(result, f(difficulty)),
                        difficulties[1:], f(difficulties[0]))
        if self.curSMBool.bool == True:
            self.curSMBool.knows.append(hellRunName+'HellRun')
        return result

    def _heatProof(self):
        return self.wor(self.haveItem('Varia'),
                        self.wand(self.wnot(RomPatches.has(RomPatches.NoGravityEnvProtection)),
                                  self.haveItem('Gravity')))

    def canHellRun(self, hellRun):
        # TODO::return heat proof item in smbool
        if self.getBool(self.heatProof()) == True:
            return SMBool(True, easy)
        elif self.energyReserveCount() >= 2:
            return self.energyReserveCountOkHellRun(hellRun)
        else:
            return SMBool(False)

#    def canFly(self):
#        self.setSMBoolCache(self._canFlySMBool)
#        return self._canFlySMBool

    def _canFly(self):
        # TODO::return spacejump item
        if self.getBool(self.haveItem('SpaceJump')) == True:
            return SMBool(True, easy)
        elif self.getBool(self.wand(self.haveItem('Morph'),
                                    self.haveItem('Bomb'),
                                    self.knowsInfiniteBombJump())) == True:
            return self.knowsInfiniteBombJump()
        else:
            return SMBool(False)

    def _canFlyDiagonally(self):
        # TODO::return spacejump item
        if self.getBool(self.haveItem('SpaceJump')) == True:
            return SMBool(True, easy)
        elif self.getBool(self.wand(self.haveItem('Morph'),
                                    self.haveItem('Bomb'),
                                    self.knowsDiagonalBombJump())) == True:
            return self.knowsDiagonalBombJump()
        else:
            return SMBool(False)

    def _canUseBombs(self):
        return self.wand(self.haveItem('Morph'), self.haveItem('Bomb'))

    def _canOpenRedDoors(self):
        return self.wor(self.haveItem('Missile'), self.haveItem('Super'))

    def _canOpenGreenDoors(self):
        return self.haveItem('Super')

    def _canOpenYellowDoors(self):
        return self.wand(self.haveItem('Morph'), self.haveItem('PowerBomb'))

    def _canUsePowerBombs(self):
        return self.canOpenYellowDoors()

    def _canDestroyBombWalls(self):
        return self.wor(self.wand(self.haveItem('Morph'),
                                  self.wor(self.haveItem('Bomb'),
                                           self.haveItem('PowerBomb'))),
                        self.haveItem('ScrewAttack'))

    def _canEnterAndLeaveGauntlet(self):
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
        return self.wand(self.wor(self.canFly(),
                                  self.haveItem('SpeedBooster'),
                                  self.wand(self.knowsHiJumpGauntletAccess(),
                                            self.haveItem('HiJump')),
                                  self.knowsHiJumpLessGauntletAccess()),
                         self.wor(self.haveItem('ScrewAttack'),
                                  self.wand(self.knowsGauntletWithPowerBombs(),
                                            self.canUsePowerBombs(),
                                            self.itemCountOk('PowerBomb', 2)),
                                  self.wand(self.knowsGauntletWithBombs(), self.canUseBombs()),
                                  self.wand(self.haveItem('SpeedBooster'),
                                            self.canUsePowerBombs(),
                                            self.energyReserveCountOk(2),
                                            self.knowsGauntletWithPowerBombs())))

    def _canPassBombPassages(self):
        return self.wor(self.canUseBombs(),
                        self.canUsePowerBombs())

#    def canAccessRedBrinstar(self):
#        #print("canAccessRedBrinstar type({}) value({})".format(type(self._canAccessRedBrinstarSMBool), self._canAccessRedBrinstarSMBool))
#        #self.curSMBool = copy.copy(self._canAccessRedBrinstarSMBool)
#        self.setSMBoolCache(self._canAccessRedBrinstarSMBool)
#        return self._canAccessRedBrinstarSMBool

    def _canAccessRedBrinstar(self):
        # EXPLAINED: we can go from Landing Site to Red Tower using two different paths:
        #             -break the bomb wall at left of Parlor and Alcatraz,
        #              open red door at Green Brinstar Main Shaft,
        #              morph at the lower part of Big Pink then use a super on the green door
        #             -open green door at the right of Landing Site, then open the yellow
        #              door at Crateria Keyhunter room
        #print("haveSuper {}".format(self.haveItem('Super')))
        #print("self.Super = {}".format(self.Super))
        #print("canDestroyBombWalls {}".format(self.canDestroyBombWalls()))
        #print("haveMorph {}".format(self.haveItem('Morph')))
        #print("canUsePowerBombs {}".format(self.canUsePowerBombs()))
        return self.wand(self.haveItem('Super'),
                         self.wor(self.wand(self.canDestroyBombWalls(),
                                            self.haveItem('Morph')),
                                  self.canUsePowerBombs()))

    def _canAccessKraid(self):
        # EXPLAINED: from Red Tower we have to go to Warehouse Entrance, and there we have to
        #            access the upper right platform with either:
        #             -hijump boots (easy regular way)
        #             -fly (space jump or infinite bomb jump)
        #             -know how to wall jump on the platform without the hijump boots
        #            then we have to break a bomb block at Warehouse Zeela room
        return self.wand(self.canAccessRedBrinstar(),
                         self.wor(self.haveItem('HiJump'),
                                  self.canFly(),
                                  self.knowsEarlyKraid()),
                         self.canPassBombPassages())

#    def canAccessWs(self):
#        self.setSMBoolCache(self._canAccessWsSMBool)
#        return self._canAccessWsSMBool

    def _canAccessWs(self):
        # EXPLAINED: from Landing Site we open the green door on the right, then in Crateria
        #            Keyhunter room we open the yellow door on the right to the Moat.
        #            In the Moat we can either:
        #             -use grapple or space jump (easy way)
        #             -do a continuous wall jump (https://www.youtube.com/watch?v=4HVhTwwax6g)
        #             -do a diagonal bomb jump from the middle platform (https://www.youtube.com/watch?v=5NRqQ7RbK3A&t=10m58s)
        #             -do a short charge from the Keyhunter room (https://www.youtube.com/watch?v=kFAYji2gFok)
        #             -do a gravity jump from below the right platform
        #             -do a mock ball and a bounce ball (https://www.youtube.com/watch?v=WYxtRF--834)
        return self.wand(self.haveItem('Super'),
                         self.canUsePowerBombs(),
                         self.wor(self.wor(self.haveItem('Grapple'),
                                           self.haveItem('SpaceJump'),
                                           self.knowsContinuousWallJump()),
                                  self.wor(self.wand(self.knowsDiagonalBombJump(),
                                                     self.canUseBombs()),
                                           self.wand(self.knowsSimpleShortCharge(),
                                                     self.haveItem('SpeedBooster')),
                                           self.wand(self.knowsGravityJump(),
                                                     self.haveItem('Gravity')),
                                           self.wand(self.knowsMockballWs(),
                                                     self.haveItem('Morph'),
                                                     self.haveItem('SpringBall')))))

    def _canAccessHeatedNorfair(self):
        # EXPLAINED: from Red Tower, to go to Bubble Mountain we have to pass through
        #            heated rooms, which requires a hell run if we don't have gravity.
        #            this test is then used to access Speed, Norfair Reserve Tank, Wave and Crocomire
        #            as they are all hellruns from Bubble Mountain.
        return self.wand(self.canAccessRedBrinstar(),
                         self.wor(self.haveItem('SpeedBooster'), # frog speedway
                                  # go through cathedral
                                  RomPatches.has(RomPatches.CathedralEntranceWallJump),
                                  self.haveItem('HiJump'),
                                  self.canFly()),
                         self.canHellRun('MainUpperNorfair'))

    def _canAccessCrocomire(self):
        # EXPLAINED: two options there, either:
        #             -from Bubble Mountain, hellrun to Crocomire's room. at Upper Norfair
        #              Farming room there's a blue gate which requires a gate glitch if no wave
        #             -the regular way, from Red Tower, power bomb in Ice Beam Gate room,
        #              then speed booster in Crocomire Speedway (easy hell run if no varia
        #              as we only have to go in straight line, so two ETanks are required)
        return self.wor(self.wand(self.canAccessHeatedNorfair(),
                                  self.wor(self.knowsGreenGateGlitch(), self.haveItem('Wave'))),
                        self.wand(self.canAccessRedBrinstar(),
                                  self.canUsePowerBombs(),
                                  self.haveItem('SpeedBooster'),
                                  self.energyReserveCountOk(2)))

    def _canDefeatCrocomire(self):
        return self.wand(self.canAccessCrocomire(),
                         self.enoughStuffCroc())


#    def canAccessLowerNorfair(self):
#        self.setSMBoolCache(self._canAccessLowerNorfairSMBool)
#        return self._canAccessLowerNorfairSMBool

    def _canAccessLowerNorfair(self):
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
        if self.getBool(self.heatProof()) == False:
            nTanks4Dive = 8
        return self.wand(self.canHellRun('LowerNorfair'),
                         self.canAccessRedBrinstar(),
                         self.canUsePowerBombs(),
                         self.wor(self.wand(self.haveItem('Gravity'), self.haveItem('SpaceJump')),
                                  self.wand(self.knowsGravityJump(), self.haveItem('Gravity')),
                                  self.wand(self.wor(self.wand(self.knowsLavaDive(),
                                                               self.haveItem('HiJump')),
                                                     self.knowsLavaDiveNoHiJump()),
                                            self.energyReserveCountOk(nTanks4Dive))))

    def _canPassWorstRoom(self):
        # https://www.youtube.com/watch?v=gfmEDDmSvn4
        return self.wand(self.canAccessLowerNorfair(),
                         self.wor(self.canFly(),
                                  self.wand(self.knowsWorstRoomIceCharge(),
                                            self.haveItem('Ice'),
                                            self.haveItem('Charge')),
                                  self.wand(self.knowsGetAroundWallJump(),
                                            self.haveItem('HiJump')),
                                  self.wand(self.knowsSpringBallJumpFromWall(),
                                            self.haveItem('SpringBall'))))

#    def canPassMtEverest(self):
#        self.setSMBoolCache(self._canPassMtEverestSMBool)
#        return self._canPassMtEverestSMBool

    def _canPassMtEverest(self):
        return self.wand(self.canAccessOuterMaridia(),
                         self.wor(self.wand(self.haveItem('Gravity'),
                                            self.wor(self.haveItem('Grapple'),
                                                     self.haveItem('SpeedBooster')),
                                            self.wor(self.canFly(),
                                                     self.knowsGravityJump(),
                                                     self.wand(self.haveItem('Ice'),
                                                               self.knowsTediousMountEverest()))),
                                  self.canDoSuitlessMaridia()))

#    def canAccessOuterMaridia(self):
#        self.setSMBoolCache(self._canAccessOuterMaridiaSMBool)
#        return self._canAccessOuterMaridiaSMBool

    def _canAccessOuterMaridia(self):
        # EXPLAINED: access Red Tower in red brinstar,
        #            power bomb to destroy the tunnel at Glass Tunnel,
        #            then to climb up Main Street, either:
        #             -have gravity (easy regular way)
        #             -freeze the enemies to jump on them, but without a strong gun in the upper left
        #              when the Sciser comes down you don't have enough time to hit it several times
        #              to freeze it, as such you have to either:
        #               -use the first Sciser from the ground and wait for it to come all the way up
        #               -do a double jump with spring ball
        return self.wand(self.canAccessRedBrinstar(),
                         self.canUsePowerBombs(),
                         self.wor(self.haveItem('Gravity'),
                                  self.wor(self.wand(self.haveItem('HiJump'),
                                                     self.haveItem('Ice'),
                                                     self.wor(self.knowsSuitlessOuterMaridiaNoGuns(),
                                                              self.wand(self.knowsSuitlessOuterMaridia(),
                                                                        self.haveItem('SpringBall'),
                                                                        self.knowsSpringBallJump()))),
                                           self.wand(self.knowsSuitlessOuterMaridia(),
                                                     self.haveItem('HiJump'),
                                                     self.haveItem('Ice'),
                                                     self.wor(self.haveItem('Wave'),
                                                              self.haveItem('Spazer'),
                                                              self.haveItem('Plasma'))))))

    def _canAccessInnerMaridia(self):
        # EXPLAINED: this is the easy regular way:
        #            access Red Tower in red brinstar,
        #            power bomb to destroy the tunnel at Glass Tunnel,
        #            gravity suit to move freely under water,
        #            at Mt Everest, no need for grapple to access upper right door:
        #            https://www.youtube.com/watch?v=2GPx-6ARSIw&t=2m28s
        return self.wand(self.canAccessRedBrinstar(),
                         self.canUsePowerBombs(),
                         self.haveItem('Gravity'))

    def _canDoSuitlessMaridia(self):
        # EXPLAINED: this is the harder way if no gravity,
        #            reach the Mt Everest then use the grapple to access the upper right door.
        #            it can also be done without gravity nor grapple but the randomizer will never
        #            require it (https://www.youtube.com/watch?v=lsbnUKcblPk).
        return self.wand(self.canAccessOuterMaridia(),
                         self.wor(self.haveItem('Grapple'),
                                  self.knowsTediousMountEverest()))

    def _canDefeatBotwoon(self):
        # EXPLAINED: access Aqueduct, either with or without gravity suit,
        #            then in Botwoon Hallway, either:
        #             -use regular speedbooster (with gravity)
        #             -do a mochtroidclip (https://www.youtube.com/watch?v=1z_TQu1Jf1I&t=20m28s)
        return self.wand(self.enoughStuffBotwoon(),
                         self.canPassMtEverest(),
                         self.wor(self.wand(self.haveItem('SpeedBooster'),
                                            self.haveItem('Gravity')),
                                  self.wand(self.knowsMochtroidClip(),
                                            self.haveItem('Ice'))))

    def _canCrystalFlash(self):
        return self.wand(self.canUsePowerBombs(),
                         self.itemCountOk('Missile', 2),
                         self.itemCountOk('Super', 2),
                         self.itemCountOk('PowerBomb', 3))

    def canDefeatDraygon(self):
        return self.canDefeatBotwoon()

    def getBeamDamage(self):
        standardDamage = 20

        if self.getBool(self.wand(self.haveItem('Ice'),
                                  self.haveItem('Wave'),
                                  self.haveItem('Plasma'))) == True:
            standardDamage = 300
        elif self.getBool(self.wand(self.haveItem('Wave'),
                                    self.haveItem('Plasma'))) == True:
            standardDamage = 250
        elif self.getBool(self.wand(self.haveItem('Ice'),
                                    self.haveItem('Plasma'))) == True:
            standardDamage = 200
        elif self.getBool(self.haveItem('Plasma')) == True:
            standardDamage = 150
        elif self.getBool(self.wand(self.haveItem('Ice'),
                                    self.haveItem('Wave'),
                                    self.haveItem('Spazer'))) == True:
            standardDamage = 100
        elif self.getBool(self.wand(self.haveItem('Wave'),
                                    self.haveItem('Spazer'))) == True:
            standardDamage = 70
        elif self.getBool(self.wand(self.haveItem('Ice'),
                                    self.haveItem('Spazer'))) == True:
            standardDamage = 60
        elif self.getBool(self.wand(self.haveItem('Ice'),
                                    self.haveItem('Wave'))) == True:
            standardDamage = 60
        elif self.getBool(self.haveItem('Wave')) == True:
            standardDamage = 50
        elif self.getBool(self.haveItem('Spazer')) == True:
            standardDamage = 40
        elif self.getBool(self.haveItem('Ice')) == True:
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
        if self.getBool(self.haveItem('Charge')) == True and charge == True:
            standardDamage = self.getBeamDamage()
        # charge triples the damage
        chargeDamage = standardDamage * 3.0

        # missile 100 damages, super missile 300 damages, PBs 200 dmg, 5 in each extension
        missilesAmount = self.itemCount('Missile') * 5
        missilesDamage = missilesAmount * 100
        supersAmount = self.itemCount('Super') * 5
        oneSuper = 300.0
        if doubleSuper == True:
            oneSuper *= 2
        supersDamage = supersAmount * oneSuper
        powerDamage = 0
        powerAmount = 0
        if power == True and self.getBool(self.haveItem('PowerBomb')) == True:
            powerAmount = self.itemCount('PowerBomb') * 5
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
        if self.getBool(self.haveItem('Gravity')) == True:
            suitsCoeff = 2
        elif self.getBool(self.haveItem('Varia')) == True:
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
        return SMBool(True, easy)

    def enoughStuffBotwoon(self):
        # say botwoon has 5000 energy : it is actually 3000 but account for missed shots
        (ammoMargin, secs) = self.canInflictEnoughDamages(5000, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)
        return SMBool(True, easy)

    def enoughStuffsRidley(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(18000, doubleSuper=True, givesDrops=False)
        if ammoMargin == 0:
            return SMBool(False)
        # print('RIDLEY', ammoMargin, secs)
        return SMBool(True, self.computeBossDifficulty(ammoMargin, secs,
                                                       Settings.bossesDifficulty['Ridley']))

    def enoughStuffsKraid(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(1000)
        if ammoMargin == 0:
            return SMBool(False)
        #print('KRAID True ', ammoMargin, secs)
        return SMBool(True, self.computeBossDifficulty(ammoMargin, secs,
                                                       Settings.bossesDifficulty['Kraid']))

    def enoughStuffsDraygon(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(6000)
        # print('DRAY', ammoMargin, secs)
        if ammoMargin > 0:
            fight = SMBool(True, self.computeBossDifficulty(ammoMargin, secs,
                                                            Settings.bossesDifficulty['Draygon']))
            if self.getBool(self.haveItem('Gravity')) == False:
                fight.difficulty *= Settings.algoSettings['draygonNoGravityMalus']
        else:
            fight = SMBool(False)
        return self.wor(fight,
                        self.wand(self.knowsDraygonGrappleKill(),
                                  self.haveItem('Grapple')),
                        self.wand(self.knowsMicrowaveDraygon(),
                                  self.haveItem('Plasma'),
                                  self.haveItem('Charge'),
                                  self.haveItem('XRayScope')),
                        self.wand(self.haveItem('Gravity'),
                                  self.knowsShortCharge(),
                                  self.haveItem('SpeedBooster')))

    def enoughStuffsPhantoon(self):
        (ammoMargin, secs) = self.canInflictEnoughDamages(2500, doubleSuper=True)
        if ammoMargin == 0:
            return SMBool(False)
        # print('PHANTOON', ammoMargin, secs)
        difficulty = self.computeBossDifficulty(ammoMargin, secs,
                                                Settings.bossesDifficulty['Phantoon'])
        hasCharge = self.getBool(self.haveItem('Charge'))
        if hasCharge or self.getBool(self.haveItem('ScrewAttack')) == True:
            difficulty /= Settings.algoSettings['phantoonFlamesAvoidBonus']
        elif not hasCharge and self.itemCount('Missile') <= 2: # few missiles is harder
            difficulty *= Settings.algoSettings['phantoonLowMissileMalus']
        fight = SMBool(True, difficulty)

        return self.wor(fight,
                        self.wand(self.knowsMicrowavePhantoon(),
                                  self.haveItem('Plasma'),
                                  self.haveItem('Charge'),
                                  self.haveItem('XRayScope')))

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
        nTanks = self.countEtank
        if self.getBool(self.haveItem('Varia')) == False:
            # "remove" 3 etanks (accounting for rainbow beam damage without varia)
            if nTanks < 6:
                return SMBool(False, 0)
            self.countEtank -= 3
        elif nTanks < 3:
            return SMBool(False, 0)

        diff = self.computeBossDifficulty(bossItems, ammoMargin, secs, Settings.bossesDifficulty['MotherBrain'])
        self.countEtank = nTanks
        return SMBool(True, diff)

    def canPassMetroids(self):
        return self.wand(self.canOpenRedDoors(),
                         self.wor(self.haveItem('Ice'),
                                  # to avoid leaving tourian to refill power bombs
                                  self.itemCountOk('PowerBomb', 3)))

    def canPassZebetites(self):
        # account for one zebetite, refill may be necessary
        return wor(self.wand(self.haveItem('Ice'), self.knowsIceZebSkip()),
                   self.wand(self.haveItem('SpeedBooster'), self.knowsSpeedZebSkip()),
                   SMBool(self.canInflictEnoughDamages(1100, charge=False, givesDrops=False)[0] >= 1, 0))

    def enoughStuffTourian(self):
        return self.wand(self.canPassMetroids(),
                         self.canPassZebetites(),
                         self.enoughStuffsMotherbrain())

class SMOptimBool(SMOptim):
    # only care about the bool, internaly: bool
    def __init__(self):
        super(SMOptimBool, self).__init__()

    def setSMBoolCache(self, smbool):
        self.curSMBool.bool = smbool.bool

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = getattr(self, item)
        return self.curSMBool.bool

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows[0]
        return self.curSMBool.bool

    def wand(self, a, b, c=True, d=True, difficulty=0):
        self.curSMBool.bool = a and b and c and d
        return self.curSMBool.bool

    def wor(self, a, b, c=False, d=False, difficulty=0):
        self.curSMBool.bool = a or b or c or d
        return self.curSMBool.bool

    def wnot(self, a):
        self.curSMBool.bool = not a
        return self.curSMBool.bool

    def itemCountOk(self, item, count, difficulty=0):
        self.curSMBool.bool = self.itemCount(item) >= count
        return self.curSMBool.bool

    def energyReserveCountOk(self, count, difficulty=0):
        self.curSMBool.bool = self.energyReserveCount() >= count
        return self.curSMBool.bool

class SMOptimDiff(SMOptim):
    # bool and diff here, internaly: only a tuple (bool, diff)
    def __init__(self):
        super(SMOptimDiff, self).__init__()

    def setSMBoolCache(self, smbool):
        self.curSMBool.bool = smbool.bool
        self.curSMBool.diff = smbool.diff

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = getattr(self, item)
        self.curSMBool.difficulty = difficulty
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows[0]
        self.curSMBool.difficulty = smKnows[1]
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wand2(self, a, b, difficulty=0):
        if a[0] == True and b[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = a[1] + b[1] + difficulty
        else:
            self.curSMBool.bool = False
            self.curSMBool.difficulty = 0
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wand(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            self.wand2(a, b)
        elif c is None:
            self.wand2(self.wand2(a, b), d)
        elif d is None:
            self.wand2(self.wand2(a, b), c)
        else:
            self.wand2(self.wand2(self.wand2(a, b), c), d)

        if self.curSMBool.bool == True and difficulty != 0:
            self.curSMBool.difficulty += difficulty

        #print("wand: {}".format(self.curSMBool.bool))
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wor2(self, a, b, difficulty=0):
        if a[0] == True and b[0] == True:
            if a[1] <= b[1]:
                self.curSMBool.bool = True
                self.curSMBool.difficulty = a[1] + difficulty
            else:
                self.curSMBool.bool = True
                self.curSMBool.difficulty = b[1] + difficulty
        elif a[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = a[1] + difficulty
        elif b[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = b[1] + difficulty
        else:
            self.curSMBool.bool = False
            self.curSMBool.difficulty = 0

        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def wor(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            self.wor2(a, b)
        elif c is None:
            self.wor2(self.wor2(a, b), d)
        elif d is None:
            self.wor2(self.wor2(a, b), c)
        else:
            self.wor2(self.wor2(self.wor2(a, b), c), d)

        if self.curSMBool.bool == True and difficulty != 0:
            self.curSMBool.difficulty += difficulty

        return (self.curSMBool.bool, self.curSMBool.difficulty)

    # negates boolean part of the SMBool
    def wnot(self, a):
        self.curSMBool.bool = not a[0]
        self.curSMBool.difficulty = a[1]
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def itemCountOk(self, item, count, difficulty=0):
        if self.itemCount(item) >= count:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = difficulty
        else:
            self.curSMBool.bool = False
        return (self.curSMBool.bool, self.curSMBool.difficulty)

    def energyReserveCountOk(self, count, difficulty=0):
        if self.energyReserveCount() >= count:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = difficulty
        else:
            self.curSMBool.bool = False
        return (self.curSMBool.bool, self.curSMBool.difficulty)

class SMOptimAll(SMOptimDiff):
    # full package, internaly: smbool
    def __init__(self):
        super(SMOptimAll, self).__init__()

    def setSMBoolCache(self, smbool):
        self.curSMBool.bool = smbool.bool
        self.curSMBool.difficulty = smbool.difficulty
        self.curSMBool.items = smbool.items[:]
        self.curSMBool.knows = smbool.knows[:]

    def haveItem(self, item, difficulty=0):
        self.curSMBool.bool = getattr(self, item)
        self.curSMBool.difficulty = difficulty
        if self.curSMBool.bool == True:
            self.curSMBool.items.append(item)
        return self.getSMBoolCopy()

    def knowsKnows(self, knows, smKnows):
        self.curSMBool.bool = smKnows[0]
        self.curSMBool.difficulty = smKnows[1]
        if self.curSMBool.bool == True:
            self.curSMBool.knows.append(knows)
            #print("knowsKnows len(knows)={}".format(len(self.curSMBool.knows)))
        #print("knowsKnows: bool={} knows={} smKnows={}".format(self.curSMBool.bool, knows, smKnows))
        return self.getSMBoolCopy()

    def wand2(self, a, b, difficulty=0):
        if a.bool == True and b.bool == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = a.difficulty + b.difficulty + difficulty
            self.curSMBool.knows = a.knows + b.knows
            self.curSMBool.items = a.items + b.items
        else:
            self.curSMBool.bool = False
            self.curSMBool.difficulty = 0
            self.curSMBool.knows = []
            self.curSMBool.items = []
        return self.getSMBoolCopy()

    def wand(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            self.wand2(a, b)
        elif c is None:
            self.wand2(self.wand2(a, b), d)
        elif d is None:
            self.wand2(self.wand2(a, b), c)
        else:
            self.wand2(self.wand2(self.wand2(a, b), c), d)

        if self.curSMBool.bool == True and difficulty != 0:
            self.curSMBool.difficulty += difficulty

        return self.getSMBoolCopy()

    def wor2(self, a, b, difficulty=0):
        if a.bool == True and b.bool == True:
            if a.difficulty < b.difficulty:
                self.curSMBool.bool = True
                self.curSMBool.difficulty = a.difficulty + difficulty
                self.curSMBool.knows = a.knows
                self.curSMBool.items = a.items
            elif a.difficulty > b.difficulty:
                self.curSMBool.bool = True
                self.curSMBool.difficulty = b.difficulty + difficulty
                self.curSMBool.knows = b.knows
                self.curSMBool.items = b.items
            else:
                self.curSMBool.bool = True
                self.curSMBool.difficulty = b.difficulty + difficulty
                self.curSMBool.knows = a.knows + b.knows
                self.curSMBool.items = a.items + b.items
        elif a.bool == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = a[1] + difficulty
            self.curSMBool.knows = a.knows
            self.curSMBool.items = a.items
        elif b[0] == True:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = b[1] + difficulty
            self.curSMBool.knows = b.knows
            self.curSMBool.items = b.items
        else:
            self.curSMBool.bool = False
            self.curSMBool.difficulty = 0
            self.curSMBool.knows = []
            self.curSMBool.items = []

        return self.getSMBoolCopy()

    def wor(self, a, b, c=None, d=None, difficulty=0):
        if c is None and d is None:
            self.wor2(a, b)
        elif c is None:
            self.wor2(self.wor2(a, b), d)
        elif d is None:
            self.wor2(self.wor2(a, b), c)
        else:
            self.wor2(self.wor2(self.wor2(a, b), c), d)

        if self.curSMBool.bool == True and difficulty != 0:
            self.curSMBool.difficulty += difficulty

        return self.getSMBoolCopy()

    # negates boolean part of the SMBool
    def wnot(self, a):
        self.curSMBool.bool = not a.bool
        self.curSMBool.difficulty = a.difficulty
        self.curSMBool.knows = a.knows
        self.curSMBool.items = a.items
        return self.getSMBoolCopy()

    def itemCountOk(self, item, count, difficulty=0):
        if self.itemCount(item) >= count:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = difficulty
            self.curSMBool.items.append(item)
        else:
            self.curSMBool.bool = False
        return self.getSMBoolCopy()

    def energyReserveCountOk(self, count, difficulty=0):
        if self.energyReserveCount() >= count:
            self.curSMBool.bool = True
            self.curSMBool.difficulty = difficulty
            self.curSMBool.items.append('ETank')
            self.curSMBool.items.append('Reserve')
        else:
            self.curSMBool.bool = False
        return self.getSMBoolCopy()

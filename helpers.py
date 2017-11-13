# the difficulties for each technics
from parameters import *

# we have to compare booleans, but with a weight (the difficulty)
# a and b type is: (bool, weight)
# if true, add given difficulty to output
def wand2(a, b, difficulty=0):
    if a[0] is True and b[0] is True:
        d = a[1] + b[1]
        return (True, d + difficulty)
    else:
        return (False, 0)

def wand(a, b, c=None, d=None, difficulty=0):
    if c is None and d is None:
        ret = wand2(a, b)
    elif c is None:
        ret = wand2(wand2(a, b), d)
    elif d is None:
        ret = wand2(wand2(a, b), c)
    else:
        ret = wand2(wand2(wand2(a, b), c), d)

    if ret[0] is True:
        return (ret[0], ret[1] + difficulty)
    else:
        return (False, 0)

def wor2(a, b, difficulty=0):
    if a[0] is True and b[0] is True:
        return (True, min(a[1], b[1]) + difficulty)
    elif a[0] is True:
        return (True, a[1] + difficulty)
    elif b[0] is True:
        return (True, b[1] + difficulty)
    else:
        return (False, 0)

def wor(a, b, c=None, d=None, difficulty=0):
    if c is None and d is None:
        ret = wor2(a, b)
    elif c is None:
        ret = wor2(wor2(a, b), d)
    elif d is None:
        ret = wor2(wor2(a, b), c)
    else:
        ret = wor2(wor2(wor2(a, b), c), d)

    if ret[0] is True:
        return (ret[0], ret[1] + difficulty)
    else:
        return (False, 0)

# check items and compute difficulty
# the second parameter returned is the difficulty:
def haveItemCount(items, item, count):
    return items.count(item) >= count

def haveItem(items, item, difficulty=0):
    return (item in items, difficulty)

def itemCount(items, item):
    return items.count(item)

def itemCountOk(items, item, count, difficulty=0):
    return (itemCount(items, item) >= count, difficulty)

def itemCountOkList(items, item, difficulties):
    # get a list: [(2, difficulty=hard), (4, difficulty=medium), (6, difficulty=easy)]
    difficulties = difficulties[:] # copy
    difficulty = difficulties.pop(0)
    result = itemCountOk(items, item, difficulty[0], difficulty=difficulty[1])
    while len(difficulties) > 0:
        difficulty = difficulties.pop(0)
        result = wor(result, itemCountOk(items, item, difficulty[0], difficulty=difficulty[1]))
    return result

def energyReserveCount(items):
    return itemCount(items, 'ETank') + itemCount(items, 'Reserve')

def energyReserveCountOk(items, count, difficulty=0):
    return (energyReserveCount(items) >= count, difficulty)

def energyReserveCountOkList(items, difficulties):
    # get a list: [(2, difficulty=hard), (4, difficulty=medium), (6, difficulty=easy)]
    difficulties = difficulties[:] # copy
    difficulty = difficulties.pop(0)
    result = energyReserveCountOk(items, difficulty[0], difficulty=difficulty[1])
    while len(difficulties) > 0:
        difficulty = difficulties.pop(0)
        result = wor(result, energyReserveCountOk(items, difficulty[0], difficulty=difficulty[1]))
    return result

def heatProof(items):
    return haveItem(items, 'Varia')

def canHellRun(items):
    if heatProof(items)[0]:
        return (True, easy)
    elif energyReserveCount(items) >= 3:
        return energyReserveCountOkList(items, hellRuns['MainUpperNorfair'])
    else:
        return (False, 0)

def canFly(items):
    if haveItem(items, 'SpaceJump')[0]:
        return (True, easy)
    elif haveItem(items, 'Morph')[0] and haveItem(items, 'Bomb')[0] and knowsInfiniteBombJump[0]:
        return knowsInfiniteBombJump
    else:
        return (False, 0)

def canFlyDiagonally(items):
    if haveItem(items, 'SpaceJump')[0]:
        return (True, easy)
    elif haveItem(items, 'Morph')[0] and haveItem(items, 'Bomb')[0] and knowsDiagonalBombJump[0]:
        return knowsDiagonalBombJump
    else:
        return (False, 0)

def canUseBombs(items, difficulty=0):
    return wand(haveItem(items, 'Morph'), haveItem(items, 'Bomb'), difficulty=difficulty)

def canOpenRedDoors(items):
    return wor(haveItem(items, 'Missile'), haveItem(items, 'Super'))

def canOpenGreenDoors(items):
    return haveItem(items, 'Super')

def canOpenYellowDoors(items):
    return wand(haveItem(items, 'Morph'), haveItem(items, 'PowerBomb'))

def canUsePowerBombs(items):
    return canOpenYellowDoors(items)

def canDestroyBombWalls(items):
    return wor(wand(haveItem(items, 'Morph'),
                    wor(haveItem(items, 'Bomb'),
                        haveItem(items, 'PowerBomb'))),
               haveItem(items, 'ScrewAttack'))

def canEnterAndLeaveGauntlet(items):
    # EXPLAINED: to access Gauntlet Entrance from Landing site we can either:
    #             -fly to it (infinite bomb jumps or space jump)
    #             -shinespark to it
    #             -wall jump with high jump boots
    #            then inside it to break the bomb wals:
    #             -use screw attack (easy way)
    #             -use power bombs
    #             -use bombs
    #             -perform a simple short charge on the way in
    #              and use power bombs on the way out
    return wand(wor(canFly(items),
                    haveItem(items, 'SpeedBooster'),
                    wand(knowsHiJumpGauntletAccess, haveItem(items, 'HiJump'))),
                wor(haveItem(items, 'ScrewAttack'),
                    wand(knowsGauntletWithPowerBombs,
                         canUsePowerBombs(items),
                         itemCountOk(items, 'PowerBomb', 2)),
                    wand(knowsGauntletWithBombs, canUseBombs(items)),
                    wand(haveItem(items, 'SpeedBooster'),
                         canUsePowerBombs(items),
                         energyReserveCountOk(items, 2),
                         wand(knowsSimpleShortCharge, knowsGauntletEntrySpark))))

def canPassBombPassages(items):
    return wor(canUseBombs(items),
               canUsePowerBombs(items))

def canAccessRedBrinstar(items):
    # EXPLAINED: we can go from Landing Site to Red Tower using two different paths:
    #             -break the bomb wall at left of Parlor and Alcatraz,
    #              open red door at Green Brinstar Main Shaft,
    #              morph at the lower part of Big Pink then use a super on the green door
    #             -open green door at the right of Landing Site, then open the yellow
    #              door at Crateria Keyhunter room
    return wand(haveItem(items, 'Super'),
                wor(wand(canDestroyBombWalls(items),
                         haveItem(items, 'Morph')),
                    canUsePowerBombs(items)))

def canAccessKraid(items):
    # EXPLAINED: from Red Tower we have to go to Warehouse Entrance, and there we have to
    #            access the upper right platform with either:
    #             -hijump boots (easy regular way)
    #             -fly (space jump or infinite bomb jump)
    #             -know how to wall jump on the platform without the hijump boots
    #            then we have to break a bomb block at Warehouse Zeela room
    return wand(canAccessRedBrinstar(items),
                wor(haveItem(items, 'HiJump'),
                    canFly(items),
                    knowsEarlyKraid),
                canPassBombPassages(items))

def canAccessWs(items):
    # EXPLAINED: from Landing Site we open the green door on the right, then in Crateria
    #            Keyhunter room we open the yellow door on the right to the Moat.
    #            In the Moat we can either:
    #             -use grapple or space jump (easy way)
    #             -do a continuous wall jump (https://www.youtube.com/watch?v=4HVhTwwax6g)
    #             -do a diagonal bomb jump from the middle platform (https://www.youtube.com/watch?v=5NRqQ7RbK3A&t=10m58s)
    #             -do a short charge from the Keyhunter room (https://www.youtube.com/watch?v=kFAYji2gFok)
    #             -do a gravity jump from below the right platform
    #             -do a mock ball and a bounce ball (https://www.youtube.com/watch?v=WYxtRF--834)
    return wand(haveItem(items, 'Super'),
                canUsePowerBombs(items),
                wor(wor(haveItem(items, 'Grapple'),
                        haveItem(items, 'SpaceJump'),
                        knowsContinuousWallJump),
                    wor(wand(knowsDiagonalBombJump, canUseBombs(items)),
                        wand(knowsSimpleShortCharge, haveItem(items, 'SpeedBooster')),
                        wand(knowsGravityJump, haveItem(items, 'Gravity')),
                        wand(knowsMockballWs, haveItem(items, 'Morph'), haveItem(items, 'SpringBall')))))

def canAccessHeatedNorfair(items):
    # EXPLAINED: from Red Tower, to go to Bubble Mountain we have to pass through
    #            heated rooms, which requires a hell run if we don't have gravity.
    #            this test is then used to access Speed, Norfair Reserve Tank, Wave and Crocomire
    #            as they are all hellruns from Bubble Mountain.
    return wand(canAccessRedBrinstar(items),
                canHellRun(items))

def canAccessCrocomire(items):
    # EXPLAINED: two options there, either:
    #             -from Bubble Mountain, hellrun to Crocomire's room. at Upper Norfair 
    #              Farming room there's a blue gate which requires a gate glitch if no wave
    #             -the regular way, from Red Tower, power bomb in Ice Beam Gate room,
    #              then speed booster in Crocomire Speedway (easy hell run if no varia
    #              as we only have to go in straight line, so two ETanks are required)
    return wor(wand(canAccessHeatedNorfair(items),
                    wor(knowsGreenGateGlitch, haveItem(items, 'Wave'))),
               wand(canAccessRedBrinstar(items),
                    canUsePowerBombs(items),
                    haveItem(items, 'SpeedBooster'),
                    energyReserveCountOk(items, 2)))

def canAccessLowerNorfair(items):
    # EXPLAINED: the randomizer never requires to pass it without the Varia suit.
    #            from Red Tower in Brinstar to access Lava Dive room we open the yellow door
    #            in Kronic Boost room with a power bomb then pass the Lava Dive room. 
    #            To pass Lava Dive room, either:
    #             -have gravity suit and space jump (easy way)
    #             -have gravity and perform a gravity jump
    #             -have hijump boots and knows the Lava Dive wall jumps, the wall jumps are
    #              a little easier with Ice and Plasma as we can freeze the Funes, we need
    #              at least three ETanks to do it without gravity
    return wand(heatProof(items),
                canAccessRedBrinstar(items),
                canUsePowerBombs(items),
                wor(wand(haveItem(items, 'Gravity'), haveItem(items, 'SpaceJump')),
                    wand(knowsGravityJump, haveItem(items, 'Gravity')),
                    wand(knowsLavaDive, haveItem(items, 'HiJump'), energyReserveCountOk(items, 3))))

def canPassWorstRoom(items):
    # https://www.youtube.com/watch?v=gfmEDDmSvn4
    return wand(canAccessLowerNorfair(items),
                wor(canFly(items),
                    wand(knowsWorstRoomIceCharge, haveItem(items, 'Ice'), haveItem(items, 'Charge')),
                    wand(knowsWorstRoomHiJump, haveItem(items, 'HiJump'))))

def canAccessOuterMaridia(items):
    # EXPLAINED: access Red Tower in red brinstar,
    #            power bomb to destroy the tunnel at Glass Tunnel,
    #            then to climb up Main Street, either:
    #             -have gravity (easy regular way)
    #             -freeze the enemies to jump on them, but without a strong gun in the upper left
    #              when the Sciser comes down you don't have enough time to hit it several times
    #              to freeze it, as such you have to either:
    #               -use the first Sciser from the ground and wait for it to come all the way up
    #               -do a double jump with spring ball
    return wand(canAccessRedBrinstar(items),
                canUsePowerBombs(items),
                wor(haveItem(items, 'Gravity'),
                    wor(wand(haveItem(items, 'HiJump'),
                             haveItem(items, 'Ice'),
                             wor(knowsSuitlessOuterMaridiaNoGuns,
                                 wand(knowsSuitlessOuterMaridia,
                                      haveItem(items, 'SpringBall'),
                                      knowsSpringBallJump))),
                        wand(knowsSuitlessOuterMaridia,
                             haveItem(items, 'HiJump'),
                             haveItem(items, 'Ice'),
                             wor(haveItem(items, 'Wave'),
                                 haveItem(items, 'Spazer'),
                                 haveItem(items, 'Plasma'))))))

def canAccessInnerMaridia(items):
    # EXPLAINED: this is the easy regular way:
    #            access Red Tower in red brinstar,
    #            power bomb to destroy the tunnel at Glass Tunnel,
    #            gravity suit to move freely under water,
    #            at Mt Everest, no need for grapple to access upper right door:
    #            https://www.youtube.com/watch?v=2GPx-6ARSIw&t=2m28s
    return wand(canAccessRedBrinstar(items),
                canUsePowerBombs(items),
                haveItem(items, 'Gravity'))

def canDoSuitlessMaridia(items):
    # EXPLAINED: this is the harder way if no gravity,
    #            reach the Mt Everest then use the grapple to access the upper right door.
    #            it can also be done without gravity nor grapple but the randomizer will never
    #            require it (https://www.youtube.com/watch?v=lsbnUKcblPk).
    return wand(canAccessOuterMaridia(items),
                haveItem(items, 'Grapple'))

def canDefeatBotwoon(items):
    # EXPLAINED: access Aqueduct, either with or without gravity suit,
    #            then in Botwoon Hallway, either:
    #             -use regular speedbooster (with gravity)
    #             -do a mochtroidclip (https://www.youtube.com/watch?v=1z_TQu1Jf1I&t=20m28s)
    return wand(wor(canAccessInnerMaridia(items),
                    canDoSuitlessMaridia(items)),
                wor(wand(haveItem(items, 'SpeedBooster'),
                         haveItem(items, 'Gravity')),
                    wand(knowsMochtroidClip, haveItem(items, 'Ice'))))


def canDefeatDraygon(items):
    # EXPLAINED: the randomizer considers that we need gravity to defeat Draygon
    return wand(canDefeatBotwoon(items),
                haveItem(items, 'Gravity'));

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
def canInflictEnoughDamages(items, bossEnergy, doubleSuper=False, charge=True, power=False, givesDrops=True):
    # TODO: handle special beam attacks ? (http://deanyd.net/sm/index.php?title=Charge_Beam_Combos)

    # http://deanyd.net/sm/index.php?title=Damage
    standardDamage = 0
    if haveItem(items, 'Charge')[0] and charge is True:
        if wand(haveItem(items, 'Ice'), haveItem(items, 'Wave'), haveItem(items, 'Plasma'))[0]:
            standardDamage = 300
        elif wand(haveItem(items, 'Wave'), haveItem(items, 'Plasma')):
            standardDamage = 250
        elif wand(haveItem(items, 'Ice'), haveItem(items, 'Plasma')):
            standardDamage = 200
        elif wand(haveItem(items, 'Plasma')):     
            standardDamage = 150
        elif wand(haveItem(items, 'Ice'), haveItem(items, 'Wave'), haveItem(items, 'Spazer')):
            standardDamage = 100
        elif wand(haveItem(items, 'Wave'), haveItem(items, 'Spazer')):
            standardDamage = 70
        elif wand(haveItem(items, 'Ice'), haveItem(items, 'Spazer')):
            standardDamage = 60
        elif wand(haveItem(items, 'Ice'), haveItem(items, 'Wave')):
            standardDamage = 60
        elif haveItem(items, 'Wave'):
            standardDamage = 50
        elif haveItem(items, 'Spazer'):
            standardDamage = 40
        elif haveItem(items, 'Ice'):
            standardDamage = 30
        else:
            standardDamage = 20

    # charge triples the damage
    chargeDPS = standardDamage * 3.0

    # missile 100 damages, super missile 300 damages, 5 missile in each extension
    missilesAmount = itemCount(items, 'Missile') * 5
    missilesDamage = missilesAmount * 100
    supersAmount = itemCount(items, 'Super') * 5
    oneSuper = 300.0
    if doubleSuper is True:
        oneSuper *= 2
    supersDamage = supersAmount * oneSuper    

    powerDamage = 0
    powerAmount = 0
    if power is True and haveItem(items, 'PowerBomb')[0]:
        # PBs come also in packs of 5
        powerAmount = itemCount(items, 'PowerBomb') * 5 
        powerDamage = powerAmount * 200

    canBeatBoss = chargeDPS > 0 or givesDrops or (missilesDamage + supersDamage + powerDamage) >= bossEnergy

    if not canBeatBoss:
        return (0, 0)
    ammoMargin = (missilesDamage + supersDamage + powerDamage) / bossEnergy
    if chargeDPS > 0:
        ammoMargin += 2

    missilesDPS = algoSettings['missilesPerSecond'] * 100.0
    supersDPS = algoSettings['supersPerSecond'] * 300.0
    if doubleSuper is True:
        supersDPS *= 2
    if powerDamage > 0:    
        powerDPS = algoSettings['powerBombsPerSecond'] * 200.0
    else:
        powerDPS = 0.0
    dpsDict = { missilesDPS : (missilesAmount, 100.0), supersDPS : (supersAmount, oneSuper), powerDPS : (powerAmount, 200.0), chargeDPS : (10000, chargeDPS) } # one charged shot per second. and no boss will take more 10000 charged shots
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
        # rely on missile/supers drops
        secs += bossEnergy * algoSettings['missileDropsPerMinute'] * 100 / 60
    #print('ammoMargin = ' + str(ammoMargin) + ', secs = ' + str(secs))
        
    return (ammoMargin, secs)

def computeBossDifficulty(items, ammoMargin, secs, diffTbl):
    # actual fight duration :
    rate = None
    if 'Rate' in diffTbl:
        rate = diffTbl['Rate']
    if rate is None:
        duration = 120.0
    else:
        duration = secs / rate
    suitsCoeff = 0.5
    if haveItem(items, 'Varia')[0]:
        suitsCoeff *= 2
    if haveItem(items, 'Gravity')[0]:
        suitsCoeff *= 2
    energy = suitsCoeff * energyReserveCount(items)
    #print('suitsCoeff = ' + str(suitsCoeff) + ', energy = ' + str(energy) + ', duration = ' + str(duration))
    energyDict = None
    if 'Energy' in diffTbl:
        energyDict = diffTbl['Energy']
    difficulty = medium
    # get difficulty by energy
    if energyDict:
        keyz = sorted(energyDict.keys())
        if len(keyz) > 0:
            difficulty = energyDict[keyz[0]]
            for k in keyz:
                if k > energy:
                    break
                difficulty = energyDict[k]
    # adjust by fight duration
    difficulty *= (duration / 120)
    # and by ammo margin
    # only augment difficulty in case of no charge, don't lower it.
    # if we have charge, ammoMargin will have a huge value (see canInflictEnoughDamages),
    # so this does not apply
    diffAdjust = (1 - (ammoMargin - algoSettings['ammoMarginIfNoCharge']))
    if diffAdjust > 1:
        difficulty *= diffAdjust
    #print('difficulty = ' + str(difficulty))
        
    return difficulty

def enoughStuffsRidley(items):
    #print('RIDLEY')
    (ammoMargin, secs) = canInflictEnoughDamages(items, 18000, doubleSuper=True, givesDrops=False)
    if ammoMargin == 0:
        return (False, 0)
    return (True, computeBossDifficulty(items, ammoMargin, secs, bossesDifficulty['Ridley']))

def enoughStuffsKraid(items):
    #print('KRAID')
    (ammoMargin, secs) = canInflictEnoughDamages(items, 1000)
    if ammoMargin == 0:
        return (False, 0)
    return (True, computeBossDifficulty(items, ammoMargin, secs, bossesDifficulty['Kraid']))    

def enoughStuffsDraygon(items):
    #print('DRAYGON')
    (ammoMargin, secs) = canInflictEnoughDamages(items, 6000)
    fight = (False, 0)
    if ammoMargin > 0:
        fight = (True, computeBossDifficulty(items, ammoMargin, secs, bossesDifficulty['Draygon']))    
    return wor(fight,
               wand(knowsDraygonGrappleKill,
                    haveItem(items, 'Grapple')),
               wand(knowsShortCharge,
                    haveItem(items, 'SpeedBooster')))

def enoughStuffsPhantoon(items):
    #print('PHANTOON')
    (ammoMargin, secs) = canInflictEnoughDamages(items, 2500, doubleSuper=True)
    if ammoMargin == 0:
        return (False, 0)
    difficulty = computeBossDifficulty(items, ammoMargin, secs, bossesDifficulty['Phantoon'])
    hasCharge = haveItem(items, 'Charge')[0]
    if hasCharge or haveItem(items, 'ScrewAttack')[0]:
        difficulty /= algoSettings['phantoonFlamesAvoidBonus']
    elif not hasCharge and itemCount(items, 'Missile') <= 2: # few missiles is harder
        difficulty *= algoSettings['phantoonLowMissileMalus']
        
    return (True, difficulty)

def enoughStuffsMotherbrain(items):
    #print('MB')
    # MB1 can't be hit by charge beam
    (ammoMargin, secs) = canInflictEnoughDamages(items, 3000, charge=False, givesDrops=False)
    if ammoMargin == 0:
        return (False, 0)
    # we actually don't give a shit about MB1 difficulty, since we embark its health in the following calc
    (ammoMargin, secs) = canInflictEnoughDamages(items, 18000 + 3000, givesDrops=False)
    if ammoMargin == 0:
        return (False, 0)
    return (True, computeBossDifficulty(items, ammoMargin, secs, bossesDifficulty['Mother Brain']))

def enoughMinors(items, minorLocations):
    if itemsPickup == '100%':
        # need them all
        return len(minorLocations) == 0
    else:
        canEnd = enoughStuffTourian(items)[0]
        if itemsPickup == "normal":
            return canEnd and haveItemCount(items, 'PowerBomb', 4)
        else: 
            return canEnd

def enoughMajors(items, majorLocations, visitedLocations):
    # the end condition
    if itemsPickup == '100%' or itemsPickup == 'normal':
        return len(majorLocations) == 0
    elif itemsPickup == 'minimal':
        return (haveItemCount(items, 'Morph', 1)
                and (haveItemCount(items, 'Bomb', 1)
                     or haveItemCount(items, 'PowerBomb', 1))
                and haveItemCount(items, 'ETank', 3)
                and haveItemCount(items, 'Varia', 1)
                and (haveItemCount(items, 'SpeedBooster', 1)
                     or haveItemCount(items, 'Ice', 1))
                and haveItemCount(items, 'Gravity', 1))

def canPassMetroids(items):
    return wand(canOpenRedDoors(items),
                wor(haveItem(items, 'Ice'),
                    (haveItemCount(items, 'PowerBomb', 3), 0))) # to avoid leaving tourian to refill power bombs

def canPassZebetites(items):
    return wor(wand(haveItem(items, 'Ice'), knowsIceZebSkip),
               wand(haveItem(items, 'SpeedBooster'), knowsSpeedZebSkip),
               (canInflictEnoughDamages(items, 1100*4, charge=False, givesDrops=False)[0] >= 1, 0)) # account for all the zebs to avoid constant refills

def allBossesDead():
    return wand(bossDead('Kraid'), bossDead('Phantoon'), bossDead('Draygon'), bossDead('Ridley'))

def enoughStuffTourian(items):
    return wand(canPassMetroids(items), canPassZebetites(items), enoughStuffsMotherbrain(items))

def canEndGame(items):
    # to finish the game you must :
    # - beat golden 4 : we force pickup of the 4 items
    #   behind the bosses to ensure that
    # - defeat metroids
    # - destroy/skip the zebetites
    # - beat Mother Brain
    return wand(allBossesDead(), enoughStuffTourian(items))

def getAvailableItemsList(locations, area, threshold):
    around = [loc for loc in locations if loc['Area'] == area and loc['difficulty'][1] <= threshold and not areaBossDead(area)]
    outside = [loc for loc in locations if not loc in around]
    around.sort(key=lambda loc: loc['difficulty'][1])
    # we want to sort the outside locations by putting the ones is the same area first, then we sort by remaining areas.
    outside.sort(key=lambda loc: (loc['difficulty'][1], 0 if loc['Area'] == area else 1, loc['Area']))

    return around + outside

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

def bossDead(boss):
    return (golden4Dead[boss], 0)

def beatBoss(boss):
    golden4Dead[boss] = True

def areaBossDead(area):
    if area not in areaBosses:
        return True
    return golden4Dead[areaBosses[area]]

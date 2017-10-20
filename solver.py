# https://itemrando.supermetroid.run/randomize

import sys
import struct

def get_item(rom_file, address, visibility):
    # return the hex code of the object at the given address

    rom_file.seek(address, 0)
    # value is in two bytes
    value1 = struct.unpack("B", rom_file.read(1))
    value2 = struct.unpack("B", rom_file.read(1))

    # match itemVisibility with
    # | Visible -> 0
    # | Chozo -> 0x54 (84)
    # | Hidden -> 0xA8 (168)
    if visibility == 'Visible':
        return hex(value2[0]*256+(value1[0]-0))
    elif visibility == 'Chozo':
        return hex(value2[0]*256+(value1[0]-84))
    elif visibility == 'Hidden':
        return hex(value2[0]*256+(value1[0]-168))
    else:
        # crash !
        manger.du(cul)

# we have to compare booleans, but with a weight (the difficulty)
# a and b type is: (bool, weight)
# if true, add given difficulty to output
def wand2(a, b, difficulty=0):
    if a[0] is True and b[0] is True:
        return (True, a[1] + b[1] + difficulty)
    else:
        return (False, 0)

# they must be a better pythonic way of doing that...
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
easy = 0
medium = 3
hard = 5
harder = 7
hardcore = 10
mania = 15

def haveItem(items, item, difficulty=0):
    return (item in items, difficulty)

def itemCount(items, item):
    return items.count(item)

def itemCountOk(items, item, count):
    return (itemCount(items, item) >= count, 0)

def energyReserveCount(items):
    return itemCount(items, 'ETank') + itemCount(items, 'Reserve')

def energyReserveCountOk(items, count, difficulty=0):
    return (energyReserveCount(items) >= count, difficulty)

def heatProof(items):
    return haveItem(items, 'Varia')

def canHellRun(items):
    if heatProof(items)[0]:
        return (True, easy)
    elif energyReserveCount(items) >= 3:
        return (True, medium)
    else:
        return (False, 0)

def canFly(items):
    if haveItem(items, 'SpaceJump')[0]:
        return (True, easy)
    elif haveItem(items, 'Morph')[0] and haveItem(items, 'Bomb')[0]:
        return (True, hard)
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
    return wand(wor(canFly(items), haveItem(items, 'HiJump'), haveItem(items, 'SpeedBooster')),
                wor(canUseBombs(items, difficulty=hard),
                    wand(canUsePowerBombs(items), itemCountOk(items, 'PowerBomb', 2), difficulty=medium),
                    haveItem(items, 'ScrewAttack'),
                    wand(haveItem(items, 'SpeedBooster'), canUsePowerBombs(items), energyReserveCountOk(items, 2), difficulty=hard)))

def canPassBombPassages(items):
    return wor(canUseBombs(items), canUsePowerBombs(items))

def canAccessRedBrinstar(items):
    return wand(haveItem(items, 'Super'),
                wor(wand(canDestroyBombWalls(items),
                         haveItem(items, 'Morph')),
                    canUsePowerBombs(items)))

def canAccessKraid(items):
    return wand(canAccessRedBrinstar(items),
                canPassBombPassages(items))

def canAccessWs(items):
    # that's hard without space jump or grappling beam (horizontal bomb jump or continuous wall jump)
    # TODO: check difficulties set:
    #   horizontal bomb jump: mania
    #   grapple or space jump: easy
    #   continuous wall jump (no items): mania
    return wand(canUsePowerBombs(items), haveItem(items, 'Super'), wor(canUseBombs(items, difficulty=mania), haveItem(items, 'Grapple'), haveItem(items, 'SpaceJump'), (True, mania)))
    
def canAccessHeatedNorfair(items):
    return wand(canAccessRedBrinstar(items), canHellRun(items))
    
def canAccessCrocomire(items):
    return wor(canAccessHeatedNorfair(items),
               wand(canAccessKraid(items),
                    canUsePowerBombs(items),
                    haveItem(items, 'SpeedBooster'),
                    energyReserveCountOk(items, 2)))
    
def canAccessLowerNorfair(items):
    return wand(canAccessHeatedNorfair(items),
                canUsePowerBombs(items),
                haveItem(items, 'Varia'),
                wor(haveItem(items, 'HiJump', difficulty=hardcore), # lava dive without gravity
                    haveItem(items, 'Gravity')))
    
def canPassWorstRoom(items):
    # TODO: don't know how difficult is just Ice or just HiJump, but it must be hard given the name of the room
    return wand(canAccessLowerNorfair(items),
                wor(canFly(items),
                    haveItem(items, 'Ice', difficulty=mania),
                    haveItem(items, 'HiJump', difficulty=hardcore)))

def canAccessOuterMaridia(items):
    # even harder if without gravity and without stronger gun
    return wand(canAccessRedBrinstar(items),
                canUsePowerBombs(items),
                wor(haveItem(items, 'Gravity'),
                    wand(haveItem(items, 'HiJump'),
                         haveItem(items, 'Ice'),
                         difficulty=mania),
                    wand(haveItem(items, 'HiJump'),
                         haveItem(items, 'Ice'),
                         wor(haveItem(items, 'Wave'),
                             haveItem(items, 'Spazer'),
                             haveItem(items, 'Plasma')),
                         difficulty=hardcore)))
    
def canAccessInnerMaridia(items):
    return wand(canAccessRedBrinstar(items),
                canUsePowerBombs(items),
                haveItem(items, 'Gravity'))
    
def canDoSuitlessMaridia(items):
    return wand(haveItem(items, 'HiJump'),
                haveItem(items, 'Ice'),
                haveItem(items, 'Grapple'),
                difficulty=hardcore)

def canDefeatBotwoon(items):
    return wand(canAccessInnerMaridia(items),
                wor(haveItem(items, 'Ice', difficulty=hard),
                    haveItem(items, 'SpeedBooster')))

def canDefeatDraygon(items):
    return wand(canDefeatBotwoon(items),
                haveItem(items, 'Gravity'));

def enough_stuff(items):
    # check that we have 60 super, 10 bomb, 5 missiles
    return itemCount(items, 'Missile') >= 1 and itemCount(items, 'Super') >= 12 and itemCount(items, 'PowerBomb') >= 2

def get_difficulty(locations):

    # loop on the available locations depending on the collected items
    # before getting a new item, loop on all of them and get their difficulty, the next collected item is the one with the smallest difficulty, if equality between major and minor, take major first

    major_locations = filter(lambda location: location["Class"] == "Major", locations)
    minor_locations = filter(lambda location: location["Class"] == "Minor", locations)

    visited_locations = []
    collected_items = []

    # TODO: not all major are usefull to complete the game, get the minimum list
    while len(major_locations) > 0 or not enough_stuff(collected_items):
        # print(str(collected_items))

        # compute the difficulty of all the locations
        for loc in major_locations:
            loc['difficulty'] = loc['Available'](collected_items)
        enough = enough_stuff(collected_items)
        if not enough:
            for loc in minor_locations:
                loc['difficulty'] = loc['Available'](collected_items)

        # keep only the available locations
        major_available = filter(lambda loc: loc["difficulty"][0] == True, major_locations)
        if not enough:
            minor_available = filter(lambda loc: loc["difficulty"][0] == True, minor_locations)

        # that shouldn't happen
        if len(major_available) == 0 and enough is True:
            print('ERROR: no more major item available')
            boire.dela(chiasse)

        # sort them on difficulty
        major_available.sort(key=lambda loc: loc['difficulty'][1])
        if not enough:
            minor_available.sort(key=lambda loc: loc['difficulty'][1])

        # first take major items with no difficulty
        major_picked = False
        while len(major_available) > 0 and major_available[0]["difficulty"][1] == easy:
            loc = major_available.pop(0)
            major_locations.remove(loc)
            visited_locations.append(loc)
            collected_items.append(items[loc["item"]]["name"])
            major_picked = True

        # if we take at least one major, recompute the difficulty
        if major_picked is True:
            continue

        # if enough stuff, take the next available major
        if enough is True:
            # take first major
            loc = major_available.pop(0)
            major_locations.remove(loc)
            visited_locations.append(loc)
            collected_items.append(items[loc["item"]]["name"])
        else:
            if len(major_available) == 0:
                next_major_difficulty = 100
            else:
                next_major_difficulty = major_available[0]["difficulty"][1]

            # take the minors easier than the next major, check if we don't get too much stuff
            minor_picked = False
            while len(minor_available) > 0 and minor_available[0]["difficulty"][1] < next_major_difficulty and not enough_stuff(collected_items):
                loc = minor_available.pop(0)
                minor_locations.remove(loc)
                visited_locations.append(loc)
                collected_items.append(items[loc["item"]]["name"])
                minor_picked = True

            # if we take at least one minor, recompute the difficulty
            if minor_picked is True:
                continue

            # take the next available major
            if len(major_available) > 0:
                loc = major_available.pop(0)
                major_locations.remove(loc)
                visited_locations.append(loc)
                collected_items.append(items[loc["item"]]["name"])

    # print generated path
    print("Generated path:")
    print('{:>50}: {:>12} {:>16} {}'.format("Location Name", "Area", "Item", "Difficulty"))
    print('-'*92)
    for location in visited_locations:
        print('{:>50}: {:>12} {:>16} {}'.format(location['Name'], location['Area'], items[location['item']]['name'], location['difficulty'][1]))

    # sum difficulty for all visited locations
    difficulty = 0
    for loc in visited_locations:
        difficulty = difficulty + loc['difficulty'][1]

    return difficulty

items = {
    '0xeed7': {'name' : 'ETank'},
    '0xeedb': {'name' : 'Missile'},
    '0xeedf': {'name' : 'Super'},
    '0xeee3': {'name' : 'PowerBomb'},
    '0xeee7': {'name' : 'Bomb'},
    '0xeeeb': {'name' : 'Charge'},
    '0xeeef': {'name' : 'Ice'},
    '0xeef3': {'name' : 'HiJump'},
    '0xeef7': {'name' : 'SpeedBooster'},
    '0xeefb': {'name' : 'Wave'},
    '0xeeff': {'name' : 'Spazer'},
    '0xef03': {'name' : 'SpringBall'},
    '0xef07': {'name' : 'Varia'},
    '0xef13': {'name' : 'Plasma'},
    '0xef17': {'name' : 'Grapple'},
    '0xef23': {'name' : 'Morph'},
    '0xef27': {'name' : 'Reserve'},
    '0xef0b': {'name' : 'Gravity'},
    '0xef0f': {'name' : 'XRayScope'},
    '0xef1b': {'name' : 'SpaceJump'},
    '0xef1f': {'name' : 'ScrewAttack'},
}

# generated with:
# sed -e "s+\([A-Z][a-z]*\) =+'\1' =+" -e 's+ =+:+' -e 's+: \([A-Z][a-z]*\);+: "\1",+' -e 's+";+",+' -e 's+\(0x[0-9A-D]*\);+\1,+' -e 's+fun items -> +lambda items: +' -e 's+};+},+' -e 's+^            ++' locations.fs > locations.py
locations = [
{
    'Area': "Crateria",
    'Name': "Power Bomb (Crateria surface)",
    'Class': "Minor",
    'Address': 0x781CC,
    'Visibility': "Visible",
    'Available': lambda items: wand(canUsePowerBombs(items), wor(haveItem(items, 'SpeedBooster'), canFly(items)))
},
{
    'Area': "Crateria",
    'Name': "Missile (outside Wrecked Ship bottom)",
    'Class': "Minor",
    'Address': 0x781E8,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (outside Wrecked Ship top)",
    'Class': "Minor",
    'Address': 0x781EE,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (outside Wrecked Ship middle)",
    'Class': "Minor",
    'Address': 0x781F4,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria moat)",
    'Class': "Minor",
    'Address': 0x78248,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "Crateria",
    'Name': "Energy Tank, Gauntlet",
    'Class': "Major",
    'Address': 0x78264,
    'Visibility': "Visible",
    # DONE: difficulty already added in the canEnterAndLeaveGauntlet function
    'Available': lambda items: canEnterAndLeaveGauntlet(items)
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria bottom)",
    'Class': "Minor",
    'Address': 0x783EE,
    'Visibility': "Visible",
    'Available': lambda items: canDestroyBombWalls(items)
},
{
    'Area': "Crateria",
    'Name': "Bomb",
    'Address': 0x78404,
    'Class': "Major",
    'Visibility': "Chozo",
    # DONE: easy with bomb, hard with hijump, mania without it
    'Available': lambda items: wand(haveItem(items, 'Morph'), canOpenRedDoors(items), wor(haveItem(items, 'HiJump', difficulty=hard), haveItem(items, 'Bomb'), (True, mania)))
},
{
    'Area': "Crateria",
    'Name': "Energy Tank, Terminator",
    'Class': "Major",
    'Address': 0x78432,
    'Visibility': "Visible",
    # DONE: easy one, nothing to add
    'Available': lambda items: wor(canDestroyBombWalls(items), haveItem(items, 'SpeedBooster'))
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria gauntlet right)",
    'Class': "Minor",
    'Address': 0x78464,
    'Visibility': "Visible",
    'Available': lambda items: wand(canEnterAndLeaveGauntlet(items), canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria gauntlet left)",
    'Class': "Minor",
    'Address': 0x7846A,
    'Visibility': "Visible",
    'Available': lambda items: wand(canEnterAndLeaveGauntlet(items), canPassBombPassages(items))
},
{
    'Area': "Crateria",
    'Name': "Super Missile (Crateria)",
    'Class': "Minor",
    'Address': 0x78478,                
    'Visibility': "Visible",
    'Available': lambda items: wand(canUsePowerBombs(items), haveItem(items, 'SpeedBooster'), wor(haveItem(items, 'ETank'), haveItem(items, 'Varia'), haveItem(items, 'Gravity')))
},
{
    'Area': "Crateria",
    'Name': "Missile (Crateria middle)",
    'Class': "Minor",
    'Address': 0x78486,
    'Visibility': "Visible",
    'Available': lambda items: canPassBombPassages(items)
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (green Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x784AC,
    'Visibility': "Chozo",
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Super Missile (pink Brinstar)",
    'Class': "Minor",
    'Address': 0x784E4,
    'Visibility': "Chozo",
    'Available': lambda items: wand(canPassBombPassages(items), haveItem(items, 'Super'))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar below super missile)",
    'Class': "Minor",
    'Address': 0x78518,
    'Visibility': "Visible",
    'Available': lambda items: wand(canPassBombPassages(items), canOpenRedDoors(items))
},
{
    'Area': "Brinstar",
    'Name': "Super Missile (green Brinstar top)",
    'Class': "Minor",
    'Address': 0x7851E,
    'Visibility': "Visible",
    'Available': lambda items: wand(wor(haveItem(items, 'SpeedBooster'), canDestroyBombWalls(items)), canOpenRedDoors(items), wor(haveItem(items, 'Morph'), haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'Name': "Reserve Tank, Brinstar",
    'Class': "Major",
    'Address': 0x7852C,
    'Visibility': "Chozo",
    # DONE: mock ball for early retreval
    'Available': lambda items: wand(wor(haveItem(items, 'SpeedBooster'), canDestroyBombWalls(items)), canOpenRedDoors(items), wor(haveItem(items, 'Morph', difficulty=medium), haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar behind missile)",
    'Class': "Minor",
    'Address': 0x78532,
    'Visibility': "Hidden",
    'Available': lambda items: wand(canPassBombPassages(items), canOpenRedDoors(items))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar behind reserve tank)",
    'Class': "Minor",
    'Address': 0x78538,
    'Visibility': "Visible",
    'Available': lambda items: wand(canDestroyBombWalls(items), canOpenRedDoors(items), haveItem(items, 'Morph'))
},
{
    'Area': "Brinstar",
    'Name': "Missile (pink Brinstar top)",
    'Class': "Minor",
    'Address': 0x78608,
    'Visibility': "Visible",
    'Available': lambda items: wor(wand(canDestroyBombWalls(items), canOpenRedDoors(items)), canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Missile (pink Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x7860E,
    'Visibility': "Visible",
    'Available': lambda items: wor(wand(canDestroyBombWalls(items), canOpenRedDoors(items)), canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Charge Beam",
    'Class': "Major",
    'Address': 0x78614,
    'Visibility': "Chozo",
    # DONE: no difficulty
    'Available': lambda items: wor(wand(canPassBombPassages(items), canOpenRedDoors(items)), canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (pink Brinstar)",
    'Class': "Minor",
    'Address': 0x7865C,
    'Visibility': "Visible",
    'Available': lambda items: wand(canUsePowerBombs(items), haveItem(items, 'Super'))
},
{
    'Area': "Brinstar",
    'Name': "Missile (green Brinstar pipe)",
    'Class': "Minor",
    'Address': 0x78676,
    'Visibility': "Visible",
    'Available': lambda items: wor(wand(canPassBombPassages(items), canOpenGreenDoors(items)), canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Morphing Ball",
    'Class': "Major",
    'Address': 0x786DE,
    'Visibility': "Visible",
    # DONE: no difficulty
    'Available': lambda items: (True, 0)
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (blue Brinstar)",
    'Class': "Minor",
    'Address': 0x7874C,
    'Visibility': "Visible",
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar middle)",
    'Address': 0x78798,
    'Class': "Minor",
    'Visibility': "Visible",
    'Available': lambda items: haveItem(items, 'Morph')
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Brinstar Ceiling",
    'Class': "Major",
    'Address': 0x7879E,
    'Visibility': "Hidden",
    # DONE: using enemy damage is medium difficulty
    'Available': lambda items: wor((True, medium), canFly(items), haveItem(items, 'HiJump'))
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Etecoons",
    'Class': "Major",
    'Address': 0x787C2,
    'Visibility': "Visible",
    # DONE: no difficulty
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Super Missile (green Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x787D0,
    'Visibility': "Visible",
    'Available': lambda items: wand(canUsePowerBombs(items), canOpenGreenDoors(items))
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Waterway",
    'Class': "Major",
    'Address': 0x787FA,
    'Visibility': "Visible",
    # DONE: easy with gravity, medium without
    'Available': lambda items: wand(canUsePowerBombs(items), canOpenRedDoors(items), haveItem(items, 'SpeedBooster'), wor(haveItem(items, 'Gravity'), (True, medium)))
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar bottom)",
    'Class': "Minor",
    'Address': 0x78802,
    'Visibility': "Chozo",
    'Available': lambda items: haveItem(items, 'Morph')
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Brinstar Gate",
    'Class': "Major",
    'Address': 0x78824,
    'Visibility': "Visible",
    # DONE: easy with wave, medium without
    'Available': lambda items: wand(canUsePowerBombs(items), wor(haveItem(items, 'Wave'), wand(haveItem(items, 'Super'), haveItem(items, 'HiJump'), difficulty=medium)))
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar top)",
    'Class': "Minor",
    'Address': 0x78836,
    'Visibility': "Visible",
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "Missile (blue Brinstar behind missile)",
    'Class': "Minor",
    'Address': 0x7883C,
    'Visibility': "Hidden",
    'Available': lambda items: canUsePowerBombs(items)
},
{
    'Area': "Brinstar",
    'Name': "X-Ray Scope",
    'Class': "Major",
    'Address': 0x78876,
    'Visibility': "Chozo",
    # TODO: what's the difficulty of the different cases ?
    # original condition (easier to read, I have to pu the lambda function on one line):
    #                Available = fun items ->canAccessRedBrinstar items && 
    #                                        canUsePowerBombs items &&
    #                                        (haveItem items Grapple ||
    #                                         haveItem items SpaceJump ||
    #                                         (haveItem items Varia && energyReserveCount items >= 4) ||
    #                                         (energyReserveCount items >= 6))
    'Available': lambda items: wand(canAccessRedBrinstar(items), canUsePowerBombs(items), wor(haveItem(items, 'Grapple'), haveItem(items, 'SpaceJump'), wand(haveItem(items, 'Varia'), energyReserveCountOk(items, 4), difficulty=medium), energyReserveCountOk(items, 6, difficulty=hard)))
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (red Brinstar sidehopper room)",
    'Class': "Minor",
    'Address': 0x788CA,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessRedBrinstar(items), canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Power Bomb (red Brinstar spike room)",
    'Class': "Minor",
    'Address': 0x7890E,
    'Visibility': "Chozo",
    'Available': lambda items: wand(canAccessRedBrinstar(items), canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Missile (red Brinstar spike room)",
    'Class': "Minor",
    'Address': 0x78914,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessRedBrinstar(items), canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Spazer",
    'Class': "Major",
    'Address': 0x7896E,
    'Visibility': "Chozo",
    # DONE: no difficulty
    'Available': lambda items: canAccessRedBrinstar(items)
},
{
    'Area': "Brinstar",
    'Name': "Energy Tank, Kraid",
    'Class': "Major",
    'Address': 0x7899C,
    'Visibility': "Hidden",
    # DONE: no difficulty
    'Available': lambda items: canAccessKraid(items)
},
{
    'Area': "Brinstar",
    'Name': "Missile (Kraid)",
    'Class': "Minor",
    'Address': 0x789EC,
    'Visibility': "Hidden",
    'Available': lambda items: wand(canAccessKraid(items), canUsePowerBombs(items))
},
{
    'Area': "Brinstar",
    'Name': "Varia Suit",
    'Class': "Major",
    'Address': 0x78ACA,
    'Visibility': "Chozo",
    # DONE: no difficulty
    'Available': lambda items: canAccessKraid(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (lava room)",
    'Class': "Minor",
    'Address': 0x78AE4,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Ice Beam",
    'Class': "Major",
    'Address': 0x78B24,
    'Visibility': "Chozo",
    # DONE: harder without varia
    'Available': lambda items: wand(canAccessKraid(items), wor(heatProof(items), energyReserveCountOk(items, 2, difficulty=hard)))
},
{
    'Area': "Norfair",
    'Name': "Missile (below Ice Beam)",
    'Class': "Minor",
    'Address': 0x78B46,
    'Visibility': "Hidden",
    'Available': lambda items: wand(canAccessKraid(items), canUsePowerBombs(items), canHellRun(items))
},
{
    'Area': "Norfair",
    'Name': "Energy Tank, Crocomire",
    'Class': "Major",
    'Address': 0x78BA4,
    'Visibility': "Visible",
    # DONE: difficulty already set in canHellRun
    'Available': lambda items: canAccessCrocomire(items)
},
{
    'Area': "Norfair",
    'Name': "Hi-Jump Boots",
    'Class': "Major",
    'Address': 0x78BAC,
    'Visibility': "Chozo",
    # DONE: no difficulty
    'Available': lambda items: canAccessRedBrinstar(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (above Crocomire)",
    'Class': "Minor",
    'Address': 0x78BC0,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessCrocomire(items), wor(canFly(items), haveItem(items, 'Grapple'), wand(haveItem(items, 'HiJump'), haveItem(items, 'SpeedBooster'))))
},
{
    'Area': "Norfair",
    'Name': "Missile (Hi-Jump Boots)",
    'Class': "Minor",
    'Address': 0x78BE6,
    'Visibility': "Visible",
    'Available': lambda items: canAccessRedBrinstar(items)
},
{
    'Area': "Norfair",
    'Name': "Energy Tank (Hi-Jump Boots)",
    'Class': "Minor",
    'Address': 0x78BEC,
    'Visibility': "Visible",
    'Available': lambda items: canAccessRedBrinstar(items)
},
{
    'Area': "Norfair",
    'Name': "Power Bomb (Crocomire)",
    'Class': "Minor",
    'Address': 0x78C04,
    'Visibility': "Visible",
    'Available': lambda items: canAccessCrocomire(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (below Crocomire)",
    'Class': "Minor",
    'Address': 0x78C14,
    'Visibility': "Visible",
    'Available': lambda items: canAccessCrocomire(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (Grapple Beam)",
    'Class': "Minor",
    'Address': 0x78C2A,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessCrocomire(items), wor(canFly(items), haveItem(items, 'Grapple'), haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Norfair",
    'Name': "Grapple Beam",
    'Class': "Major",
    'Address': 0x78C36,
    'Visibility': "Chozo",
    # TODO: what's the difficulty without speedbooster ?
    'Available': lambda items: wand(canAccessCrocomire(items), wor(canFly(items), haveItem(items, 'Ice'), haveItem(items, 'SpeedBooster')))
},
{
    'Area': "Norfair",
    'Name': "Reserve Tank, Norfair",
    'Class': "Major",
    'Address': 0x78C3E,
    'Visibility': "Chozo",
    # TODO: the one in the bubbles, how hard is it depending on the items ?
    'Available': lambda items: wand(canAccessHeatedNorfair(items), wor(canFly(items), haveItem(items, 'Grapple'), haveItem(items, 'HiJump')))
},
{
    'Area': "Norfair",
    'Name': "Missile (Norfair Reserve Tank)",
    'Class': "Minor",
    'Address': 0x78C44,
    'Visibility': "Hidden",
    'Available': lambda items: wand(canAccessHeatedNorfair(items), wor(canFly(items), haveItem(items, 'Grapple'), haveItem(items, 'HiJump')))
},
{
    'Area': "Norfair",
    'Name': "Missile (bubble Norfair green door)",
    'Class': "Minor",
    'Address': 0x78C52,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessHeatedNorfair(items), wor(canFly(items), haveItem(items, 'Grapple'), haveItem(items, 'HiJump')))
},
{
    'Area': "Norfair",
    'Name': "Missile (bubble Norfair)",
    'Class': "Minor",
    'Address': 0x78C66,
    'Visibility': "Visible",
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (Speed Booster)",
    'Class': "Minor",
    'Address': 0x78C74,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Speed Booster",
    'Class': "Major",
    'Address': 0x78C82,
    'Visibility': "Chozo",
    # DONE: difficulty already done in the function
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Missile (Wave Beam)",
    'Class': "Minor",
    'Address': 0x78CBC,
    'Visibility': "Visible",
    'Available': lambda items: canAccessHeatedNorfair(items)
},
{
    'Area': "Norfair",
    'Name': "Wave Beam",
    'Class': "Major",
    'Address': 0x78CCA,
    'Visibility': "Chozo",
    # DONE: this one is not easy without grapple beam nor space jump, with hijump medium wall jump is required
    'Available': lambda items: wand(canAccessHeatedNorfair(items), wor(haveItem(items, 'Grapple'), haveItem(items, 'SpaceJump'), haveItem(items, 'HiJump', difficulty=medium), (True, hard)))
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (Gold Torizo)",
    'Class': "Minor",
    'Address': 0x78E6E,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessLowerNorfair(items), haveItem(items, 'SpaceJump'))
},
{
    'Area': "LowerNorfair",
    'Name': "Super Missile (Gold Torizo)",
    'Class': "Minor",
    'Address': 0x78E74,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessLowerNorfair(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (Mickey Mouse room)",
    'Class': "Minor",
    'Address': 0x78F30,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (lower Norfair above fire flea room)",
    'Class': "Minor",
    'Address': 0x78FCA,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Power Bomb (lower Norfair above fire flea room)",
    'Class': "Minor",
    'Address': 0x78FD2,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Power Bomb (Power Bombs of shame)",
    'Class': "Minor",
    'Address': 0x790C0,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Missile (lower Norfair near Wave Beam)",
    'Class': "Minor",
    'Address': 0x79100,
    'Visibility': "Visible",
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Energy Tank, Ridley",
    'Class': "Major",
    'Address': 0x79108,
    'Visibility': "Hidden",
    # DONE: already set in function
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Screw Attack",
    'Class': "Major",
    'Address': 0x79110,
    'Visibility': "Chozo",
    # DONE: easy with green gate glitch
    'Available': lambda items: canAccessLowerNorfair(items)
},
{
    'Area': "LowerNorfair",
    'Name': "Energy Tank, Firefleas",
    'Class': "Major",
    'Address': 0x79184,
    'Visibility': "Visible",
    # TODO: how hard is it further than the requirements for the worst room ?
    'Available': lambda items: canPassWorstRoom(items)
},
{
    'Area': "WreckedShip",
    'Name': "Missile (Wrecked Ship middle)",
    'Class': "Minor",
    'Address': 0x7C265,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "WreckedShip",
    'Name': "Reserve Tank, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C2E9,
    'Visibility': "Chozo",
    # DONE: easy
    'Available': lambda items: wand(canAccessWs(items), haveItem(items, 'SpeedBooster'), wor(haveItem(items, 'Varia'), energyReserveCountOk(items, 1)))
},
{
    'Area': "WreckedShip",
    'Name': "Missile (Gravity Suit)",
    'Class': "Minor",
    'Address': 0x7C2EF,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessWs(items), wor(haveItem(items, 'Varia'), energyReserveCountOk(items, 1)))
},
{
    'Area': "WreckedShip",
    'Name': "Missile (Wrecked Ship top)",
    'Class': "Minor",
    'Address': 0x7C319,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "WreckedShip",
    'Name': "Energy Tank, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C337,
    'Visibility': "Visible",
    # TODO: what's the difficult for each case ?
    'Available': lambda items: wand(canAccessWs(items), wor(wor(haveItem(items, 'Bomb'), haveItem(items, 'PowerBomb'), haveItem(items, 'HiJump')), wor(haveItem(items, 'SpaceJump'), haveItem(items, 'SpeedBooster'), haveItem(items, 'SpringBall'))))
},
{
    'Area': "WreckedShip",
    'Name': "Super Missile (Wrecked Ship left)",
    'Class': "Minor",
    'Address': 0x7C357,
    'Visibility': "Visible",
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "WreckedShip",
    'Name': "Right Super, Wrecked Ship",
    'Class': "Major",
    'Address': 0x7C365,
    'Visibility': "Visible",
    # DONE: easy once WS is accessible
    'Available': lambda items: canAccessWs(items)
},
{
    'Area': "WreckedShip",
    'Name': "Gravity Suit",
    'Class': "Major",
    'Address': 0x7C36D,
    'Visibility': "Chozo",
    # DONE: easy
    'Available': lambda items: wand(canAccessWs(items), wor(haveItem(items, 'Varia'), energyReserveCountOk(items, 1)))
},
{
    'Area': "Maridia",
    'Name': "Missile (green Maridia shinespark)",
    'Class': "Minor",
    'Address': 0x7C437,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessRedBrinstar(items), canUsePowerBombs(items), haveItem(items, 'Gravity'), haveItem(items, 'SpeedBooster'))
},
{
    'Area': "Maridia",
    'Name': "Super Missile (green Maridia)",
    'Class': "Minor",
    'Address': 0x7C43D,
    'Visibility': "Visible",
    'Available': lambda items: canAccessOuterMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Energy Tank, Mama turtle",
    'Class': "Major",
    'Address': 0x7C47D,
    'Visibility': "Visible",
    # DONE: difficulty already handled in canAccessOuterMaridia
    'Available': lambda items: wand(canAccessOuterMaridia(items), wor(canFly(items), haveItem(items, 'SpeedBooster'), haveItem(items, 'Grapple')))
},
{
    'Area': "Maridia",
    'Name': "Missile (green Maridia tatori)",
    'Class': "Minor",
    'Address': 0x7C483,
    'Visibility': "Hidden",
    'Available': lambda items: canAccessOuterMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Super Missile (yellow Maridia)",
    'Class': "Minor",
    'Address': 0x7C4AF,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (yellow Maridia super missile)",
    'Class': "Minor",
    'Address': 0x7C4B5,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Missile (yellow Maridia false wall)",
    'Class': "Minor",
    'Address': 0x7C533,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Plasma Beam",
    'Class': "Major",
    'Address': 0x7C559,
    'Visibility': "Chozo",
    # TODO: what's the difficulty for each cases ?
    'Available': lambda items: wand(canDefeatDraygon(items), wor(haveItem(items, 'SpeedBooster'), wand(wor(haveItem(items, 'Charge'), haveItem(items, 'ScrewAttack')), wor(canFly(items), haveItem(items, 'HiJump')))))
},
{
    'Area': "Maridia",
    'Name': "Missile (left Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5DD,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Reserve Tank, Maridia",
    'Class': "Major",
    'Address': 0x7C5E3,
    'Visibility': "Chozo",
    # DONE: difficulty already handled in the two functions
    'Available': lambda items: wand(canAccessOuterMaridia(items), wor(canDoSuitlessMaridia(items), haveItem(items, 'Gravity')))
},
{
    'Area': "Maridia",
    'Name': "Missile (right Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5EB,
    'Visibility': "Visible",
    'Available': lambda items: canAccessInnerMaridia(items)
},
{
    'Area': "Maridia",
    'Name': "Power Bomb (right Maridia sand pit room)",
    'Class': "Minor",
    'Address': 0x7C5F1,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessOuterMaridia(items), haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'Name': "Missile (pink Maridia)",
    'Address': 0x7C603,
    'Class': "Minor",
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessOuterMaridia(items), haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'Name': "Super Missile (pink Maridia)",
    'Class': "Minor",
    'Address': 0x7C609,
    'Visibility': "Visible",
    'Available': lambda items: wand(canAccessOuterMaridia(items), haveItem(items, 'Gravity'))
},
{
    'Area': "Maridia",
    'Name': "Spring Ball",
    'Class': "Major",
    'Address': 0x7C6E5,
    'Visibility': "Chozo",
    # TODO: how is it possible to destroy the grapple fix point without the grapple beam ?
    'Available': lambda items: wand(canAccessInnerMaridia(items), wor(haveItem(items, 'Ice'), wand(haveItem(items, 'Grapple'), wor(canFly(items), haveItem(items, 'HiJump')))))
},
{
    'Area': "Maridia",
    'Name': "Missile (Draygon)",
    'Class': "Minor",
    'Address': 0x7C74D,
    'Visibility': "Hidden",
    'Available': lambda items: canDefeatBotwoon(items)
},
{
    'Area': "Maridia",
    'Name': "Energy Tank, Botwoon",
    'Class': "Major",
    'Address': 0x7C755,
    'Visibility': "Visible",
    # DONE: difficulty already handled in the functions
    'Available': lambda items: wor(canDefeatBotwoon(items), wand(canAccessOuterMaridia(items), canDoSuitlessMaridia(items)))
},
{
    'Area': "Maridia",
    'Name': "Space Jump",
    'Class': "Major",
    'Address': 0x7C7A7,
    'Visibility': "Chozo",
    # DONE: difficulty already handled in the function
    'Available': lambda items: canDefeatDraygon(items)
}
]


if len(sys.argv) != 2:
    print("missing param: rom file")
    sys.exit(0)

rom_name = sys.argv[1]
#rom_name = 'TX4371551.sfc'
print("rom_name=" + rom_name)

rom_file = open(rom_name, "r")

for location in locations:
    location["item"] = get_item(rom_file, location["Address"], location["Visibility"])
    #print('{:>50}: {:>16}'.format(location["Name"], items[location["item"]]['name']))

rom_file.close()

difficulty = get_difficulty(locations)

print("Estimated difficulty: {}".format(difficulty))

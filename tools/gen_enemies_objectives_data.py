#!/usr/bin/python3

import sys, os, json
from collections import defaultdict

sys.path.append(os.path.dirname(sys.path[0]))

from rooms import rooms

from rom.rom import RealROM, pc_to_snes
from rom.leveldata import Room

enemyIds = {
    "Space Pirates": [0xf353, 0xf393, 0xf3d3, 0xf413, 0xf453, 0xf493,
                      0xf4d3, 0xf513, 0xf553, 0xf593, 0xf5d3,# 0xf613,
                      0xf653, 0xf693, 0xf6d3, 0xf693, 0xf6d3, 0xf713,
                      0xf753, 0xf793, 0xf7d3],
    "Ki Hunters": [0xeabf, 0xeb3f, 0xebbf],
    "Beetoms": [0xe87f],
    "Cacatacs": [0xcfff],
    "Kagos": [0xe7ff],
    "Yapping Maws": [0xe7bf]
}

MAX_EVENTS = 280

enemyTypes = {}

for nmyType, ids in enemyIds.items():
    for nmyId in ids:
        enemyTypes[nmyId] = nmyType

vanilla = RealROM(sys.argv[1])

class EnemyCounter:
    total = 0
    event = 0
    enemies = defaultdict(int)

    def getEvent():
        ret = EnemyCounter.event
        EnemyCounter.event += 1
        return ret
    
    def countEnemy(nmyType):
        EnemyCounter.total += 1
        EnemyCounter.enemies[nmyType] += 1

nmyObjData = {}

for nmyType in enemyIds:
    nmyObjData[nmyType] = {"event": EnemyCounter.getEvent(), "areas": {}}

for roomDef in rooms:
    area = roomDef["GraphArea"]
    if area in ["Ceres", "Tourian"]:
        continue
    print(roomDef["Name"])
    room = Room(vanilla, pc_to_snes(roomDef["Address"]))
    roomEnemiesByType = defaultdict(list)
    for statePtr, enemies in room.enemies.items():
        specialEnemies = [nmy for nmy in enemies if nmy.enemyId in enemyTypes]
        for nmy in specialEnemies:
            roomEnemiesByType[enemyTypes[nmy.enemyId]].append(nmy)
    for nmyType, enemies in roomEnemiesByType.items():
        if area not in nmyObjData[nmyType]["areas"]:
            nmyObjData[nmyType]["areas"][area] = {
                "count": 0,
                "room_events": {},
                "enemies": defaultdict(list)
            }
        areaData = nmyObjData[nmyType]['areas'][area]
        areaData["room_events"][roomDef["Name"]] = EnemyCounter.getEvent()
        for nmy in enemies:
            entry = {"event": EnemyCounter.getEvent(), "props_snes_addr": nmy.dataAddr+10, "props": nmy.extraProperties}
            areaData["enemies"][roomDef["Name"]].append(entry)
            EnemyCounter.countEnemy(nmyType)
            areaData["count"] += 1

print(EnemyCounter.total)
print(EnemyCounter.event)
print(EnemyCounter.enemies)

assert EnemyCounter.event < MAX_EVENTS, "Too many events: %d" % EnemyCounter.event

with open("enemies_objectives_data.json", "w") as fp:
    json.dump(nmyObjData, fp, indent=4)

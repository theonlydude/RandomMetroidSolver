#!/usr/bin/env python

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from utils import randGaussBounds
from itemrandomizerweb.Items import ItemManager
from smboolmanager import SMBoolManager
import random
import log

fun = ['HiJump', 'SpeedBooster', 'Plasma', 'ScrewAttack', 'Wave', 'Spazer', 'SpringBall']

if __name__ == "__main__":
#    log.init(True) # debug mode
    log.init(False)
    logger = log.get('ItemsTest')
    sm = SMBoolManager()
    with open("itemStats.csv", "w") as csvOut:
        csvOut.write("energyQty;minorQty;nFun;strictMinors;MissProb;SuperProb;PowerProb;nItems;nTanks;nTanksTotal;nMinors;nMissiles;nSupers;nPowers;MissAccuracy;SuperAccuracy;PowerAccuracy;AmmoAccuracy\n")
        for i in range(10000):
            logger.debug('SEED ' + str(i))
            if (i+1) % 100 == 0:
                print(i+1)
            isVanilla = random.random() < 0.5
            strictMinors = bool(random.randint(0, 2))
            minQty = 100
            energyQty = 'vanilla'
            forbidden = []
            if not isVanilla:
                minQty = random.randint(1, 99)
                if random.random() < 0.5:
                    energyQty = 'medium'
                else:
                    energyQty = 'sparse'
                funPick = fun[:]
                for i in range(randGaussBounds(len(fun))):
                    item = funPick[random.randint(0, len(funPick)-1) if len(funPick) > 1 else 0]
                    forbidden.append(item)
                    funPick.remove(item)
            missProb = random.randint(1, 9)
            superProb = random.randint(1, 9)
            pbProb = random.randint(1, 9)
            qty = {
                'minors' : minQty,
                'energy' : energyQty,
                'ammo' : {
                    'Missile' : missProb,
                    'Super' : superProb,
                    'PowerBomb' : pbProb
                },
                'strictMinors' : strictMinors
            }
            # write params
            csvOut.write("%s;%d;%d;%s;%d;%d;%d;" % (energyQty, minQty, len(forbidden), str(strictMinors), missProb, superProb, pbProb))
            # get items
            splits = ['Full', 'Major', 'Chozo']
            split = splits[random.randint(0, len(splits)-1) if len(splits) > 1 else 0]
            itemManager = ItemManager(split, qty, sm)
            itemPool = itemManager.createItemPool()
            itemPool = itemManager.removeForbiddenItems(forbidden)
            # compute stats
            nItems = len([item for item in itemPool if item['Category'] != 'Nothing'])
            nTanks = len([item for item in itemPool if item['Category'] == 'Energy'])
            nEnergyTotal = len([item for item in itemPool if item['Category'] == 'Energy' or item['Type'] == 'NoEnergy']) - len(forbidden)
            nMinors = len([item for item in itemPool if item['Category'] == 'Ammo'])
            nMissiles = len([item for item in itemPool if item['Type'] == 'Missile'])
            nSupers = len([item for item in itemPool if item['Type'] == 'Super'])
            nPowers = len([item for item in itemPool if item['Type'] == 'PowerBomb'])
            csvOut.write("%d;%d;%d;%d;%d;%d;%d;" % (nItems, nTanks, nEnergyTotal, nMinors, nMissiles, nSupers, nPowers))
            totalProbs = missProb + superProb + pbProb
            def getAccuracy(prob, res):
                th = float(prob)/totalProbs
                actual = float(res)/nMinors
                return actual/th * 100
            missAcc = getAccuracy(missProb, nMissiles)
            supersAcc = getAccuracy(superProb, nSupers)
            pbAcc = getAccuracy(pbProb, nPowers)
            ammoAcc = (float(nMinors)/66.0) / minQty * 100
            csvOut.write("%f;%f;%f;%f\n" % (missAcc, supersAcc, pbAcc, ammoAcc))
            if len(itemPool) != 105:
                raise ValueError("Not 105 items !!! " + str(len(itemPool)))
            if isVanilla and nItems != 100:
                raise ValueError("Not 100 actual items in vanilla !!! " + str(nItems))
            if energyQty == 'sparse' and (nTanks < 4 or nTanks > 6):
                raise ValueError("Energy qty invalid for sparse !! " + str(nTanks))
            if energyQty == 'medium' and (nTanks < 8 or nTanks > 12):
                raise ValueError("Energy qty invalid for medium !! " + str(nTanks))

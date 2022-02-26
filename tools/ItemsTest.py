#!/usr/bin/env python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
sys.path.append(os.path.dirname(sys.path[0]))

from utils.utils import randGaussBounds
from rando.Items import ItemManager
from logic.smboolmanager import SMBoolManager
from logic.logic import Logic

import random
import utils.log

fun = ['HiJump', 'SpeedBooster', 'Plasma', 'ScrewAttack', 'Wave', 'Spazer', 'SpringBall']
maxLocs = 109
bossesItems = ['Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain', 'SporeSpawn', 'Crocomire', 'Botwoon', 'GoldenTorizo']

if __name__ == "__main__":
#    utils.log.init(True) # debug mode
    utils.log.init(False)
    logger = utils.log.get('ItemsTest')
    Logic.factory('vanilla')
    sm = SMBoolManager()
    with open("itemStats.csv", "w") as csvOut:
        csvOut.write("nLocs;energyQty;minorQty;nFun;strictMinors;MissProb;SuperProb;PowerProb;split;nItems;nTanks;nTanksTotal;nMinors;nMissiles;nSupers;nPowers;MissAccuracy;SuperAccuracy;PowerAccuracy;AmmoAccuracy\n")
        for i in range(10000):
            logger.debug('SEED ' + str(i))
            if (i+1) % 100 == 0:
                print(i+1)
            isVanilla = random.random() < 0.5
            strictMinors = bool(random.getrandbits(1))
            minQty = 100
            energyQty = 'vanilla'
            forbidden = []
            if not isVanilla:
                minQty = random.randint(1, 99)
                r = random.random()
                if r < 0.33:
                    energyQty = 'medium'
                elif r > 0.66:
                    energyQty = 'sparse'
                else:
                    energyQty = 'ultra sparse'
                funPick = fun[:]
                for i in range(randGaussBounds(len(fun))):
                    item = random.choice(funPick)
                    forbidden.append(item)
                    funPick.remove(item)
            nLocs = maxLocs
            if random.random() < 0.25:
                nLocs = random.randint(40, 80)
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
            # get items
            splits = ['Full', 'Major', 'Chozo']
            split = random.choice(splits) if nLocs == maxLocs else 'Full'
            # write params
            csvOut.write("%d;%s;%d;%d;%s;%d;%d;%d;%s;" % (nLocs, energyQty, minQty, len(forbidden), str(strictMinors), missProb, superProb, pbProb, split))
            itemManager = ItemManager(split, qty, sm, nLocs, bossesItems, 100)
            itemPool = itemManager.createItemPool()
            itemPool = itemManager.removeForbiddenItems(forbidden)
            # compute stats
            nItems = len([item for item in itemPool if item.Category != 'Nothing'])
            nTanks = len([item for item in itemPool if item.Category == 'Energy'])
            nEnergyTotal = len([item for item in itemPool if item.Category == 'Energy' or item.Type == 'NoEnergy']) - len(forbidden)
            nMinors = len([item for item in itemPool if item.Category == 'Ammo'])
            nMissiles = len([item for item in itemPool if item.Type == 'Missile'])
            nSupers = len([item for item in itemPool if item.Type == 'Super'])
            nPowers = len([item for item in itemPool if item.Type == 'PowerBomb'])
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
            if len(itemPool) != nLocs:
                raise ValueError("Not " + str(nLocs) + " items !!! " + str(len(itemPool)))
            if isVanilla and nItems != nLocs:
                raise ValueError("Not " + str(nLocs) + " actual items in vanilla !!! " + str(nItems))
            if energyQty == 'ultra sparse' and (nTanks > 1):
                raise ValueError("Energy qty invalid for ultra sparse !! " + str(nTanks))
            if energyQty == 'sparse' and (nTanks < 4 or nTanks > 6):
                raise ValueError("Energy qty invalid for sparse !! " + str(nTanks))
            if nLocs == 105 and energyQty == 'medium' and (nTanks < 8 or nTanks > 12):
                raise ValueError("Energy qty invalid for medium !! " + str(nTanks))

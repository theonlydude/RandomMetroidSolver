#!/bin/bash

# launch from project root

[ -z "$VANILLA" ] && VANILLA=vanilla.sfc

qties="30 40 50 60"
areas="GreenPinkBrinstar RedBrinstar Kraid WestMaridia Crateria Norfair Crocomire WreckedShip EastMaridia LowerNorfair Tourian"

declare -A areas_count
nseeds=100

for q in $qties; do
    min_locs=1000
    max_locs=0
    total_locs=0
    nerrs=0
    for a in $areas; do areas_count[$a]=0; done
    for i in $(seq 1 $nseeds); do
	printf "\r$q locs. seed $i/$nseeds"
	./randomizer.py  -r $VANILLA --runtime 20 --param standard_presets/regular.json --missileQty 3 --superQty 2 --powerBombQty 1 --minorQty 100 --majorsSplit Full --progressionSpeed medium --progressionDifficulty normal --morphPlacement normal --energyQty vanilla --startLocation random --startLocationList 'Landing Site,Gauntlet Top,Green Brinstar Elevator,Big Pink,Etecoons Supers,Wrecked Ship Main,Firefleas Top,Business Center,Bubble Mountain,Mama Turtle,Watering Hole,Aqueduct,Red Brinstar Elevator,Golden Four' --maxDifficulty hardcore -c itemsounds.ips --areaRandomization full --bosses --minimizer $q --tourian Fast --jm --debug > minimizer.log
	if [ $? -eq 0 ]; then
	    nLocs=$(grep 'FINAL MINIMIZER nLocs' minimizer.log | tail -n 1 | cut -d ':' -f 4 | awk '{print $1}')
	    if [ $nLocs -lt $min_locs ]; then
		min_locs=$nLocs
	    fi
	    if [ $nLocs -gt $max_locs ]; then
		max_locs=$nLocs
	    fi
	    let total_locs=total_locs+nLocs
	    areaList=$(grep 'FINAL MINIMIZER areas' minimizer.log | tail -n 1 | cut -d ':' -f 4)
	    for a in $areas; do
		echo $areaList | grep $a > /dev/null
		[ $? -eq 0 ] && {
		    let c="${areas_count[$a]}+1"
		    areas_count[$a]="$c"
		}
	    done
	else
	    let nerrs=nerrs+1
	    l="minimizer_${q}_${i}.log"
	    mv minimizer.log $l
	    printf "\nError during seed generation. Log : $l\n"
	fi
    done
    let n=nseeds-nerrs
    let avg_locs=total_locs/n
    printf "\n** For $q locations :\n"
    echo "min_locs=$min_locs, max_locs=$max_locs, avg_locs=$avg_locs"
    echo "Areas :"
    for a in $areas; do
	echo "$a : ${areas_count[$a]}"
    done
done

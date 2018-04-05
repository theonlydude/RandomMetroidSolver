#!/bin/bash

> test_jm.log
#> test_jm.err
#> test_jm.csv

if [ $# -ne 2 ]; then
    echo "params: ROM LOOPS"
    exit -1
fi

#ROM=~/supermetroid_random/Super_Metroid_JU.smc
#ROM=~/downloads/samus/roms/Super_Metroid_orig.smc
ROM=$1
LOOPS=$2

PATCHES="-c AimAnyButton.ips -c itemsounds.ips -c spinjumprestart.ips -c supermetroid_msu1.ips -c elevators_doors_speed.ips"
PRESETS=("manu" "noob" "speedrunner")
SUPERFUNS=("" "" "" "--superFun Movement" "--superFun Combat" "--superFun Suits" "--superFun Movement --superFun Combat")
ENERGIES=("sparse" "medium" "vanilla")
SPREADS=("" "--spreadItems")
FULLS=("" "--fullRandomization")
SUITS=("" "--suitsRestriction")
SPEEDS=("" "--speedScrewRestriction")
DIFFS=("" "" "" "" "" "" "--maxDifficulty easy" "--maxDifficulty medium" "--maxDifficulty hard" "--maxDifficulty harder" "--maxDifficulty hardcore" "--maxDifficulty mania")

function generate_params {
    SEED="$1"
    PRESET="$2"

    PROG_SPEED="--progressionSpeed random"

    let S=$RANDOM%${#SUPERFUNS[@]}
    SUPERFUN=${SUPERFUNS[$S]}

    let QTY=1+$RANDOM%100
    MINORS="--minorQty ${QTY}"
    let QTY=1+$RANDOM%9
    MISSILES="--missileQty ${QTY}"
    let QTY=1+$RANDOM%9
    SUPERS="--superQty ${QTY}"
    let QTY=1+$RANDOM%9
    POWERBOMBS="--powerBombQty ${QTY}"
    let QTY=1+$RANDOM%3
    ENERGY="--energyQty ${ENERGIES[$QTY]}"

    let S=$RANDOM%${#SPREADS[@]}
    SPREAD=${SPREADS[$S]}
    let S=$RANDOM%${#FULLS[@]}
    FULL=${FULLS[$S]}
    let S=$RANDOM%${#SUITS[@]}
    SUIT=${SUITS[$S]}
    let S=$RANDOM%${#SPEEDS[@]}
    SPEED=${SPEEDS[$S]}

    let S=$RANDOM%${#DIFFS[@]}
    DIFF=${DIFFS[$S]}

    echo "-r ${ROM} --param diff_presets/${PRESET}.json ${PATCHES} --seed ${SEED} ${PROG_SPEED} ${SUPERFUN} ${MINORS} ${MISSILES} ${SUPERS} ${POWERBOMBS} ${ENERGY} ${SPREAD} ${FULL} ${SUIT} ${SPEED} ${DIFF}"
}

if [ -z test_jm.csv ]; then
    echo "seed;params;old/new;time;stuck;md5sum;mismatch" > test_jm.csv
fi

MISMATCH_FOUND=1
for i in $(seq 1 ${LOOPS}); do
    let P=$RANDOM%${#PRESETS[@]}
    PRESET=${PRESETS[$P]}
    SEED="$RANDOM"

    PARAMS=$(generate_params "${SEED}" "${PRESET}")
    OUT=$(/usr/bin/time -f "\t%E real" pypy ./randomizer.py ${PARAMS} 2>&1)

    echo "${OUT}" | grep -q STUCK
    if [ $? -eq 0 ]; then
        STUCK="yes"
    else
        STUCK="no"
    fi
    TIME=$(echo "${OUT}" | grep real | awk '{print $1}')
    SUM_OLD=$(md5sum VARIA_Randomizer_*X${SEED}_${PRESET}.sfc | cut -d ' ' -f 1)
    rm -f VARIA_Randomizer_*X${SEED}_${PRESET}.sfc

    echo "${SEED};${PARAMS};OLD;${TIME};${STUCK};${SUM_OLD};" | tee -a test_jm.csv

    OUT=$(/usr/bin/time -f "\t%E real" python2 ./randomizer_optim.py ${PARAMS} 2>&1)

    echo "${OUT}" | grep -q STUCK
    if [ $? -eq 0 ]; then
        STUCK="yes"
    else
        STUCK="no"
    fi
    TIME=$(echo "${OUT}" | grep real | awk '{print $1}')
    SUM_NEW=$(md5sum VARIA_Randomizer_*X${SEED}_${PRESET}.sfc | cut -d ' ' -f 1)
    rm -f VARIA_Randomizer_*X${SEED}_${PRESET}.sfc

    if [ "$SUM_OLD" != "$SUM_NEW" ]; then
        MIS="MISMATCH !!!!!"
        echo "Mismatch for ${SEED}" | tee -a test_jm.err
        MISMATCH_FOUND=0
    else
        MIS=""
    fi

    echo "${SEED};${PARAMS};NEW;${TIME};${STUCK};${SUM_NEW};${MIS}" | tee -a test_jm.csv

done | tee test_jm.log

if [ ${MISMATCH_FOUND} -eq 0 ]; then
    echo "WARNING_Mismatch found !"
else
    echo "No mismatch found"
fi

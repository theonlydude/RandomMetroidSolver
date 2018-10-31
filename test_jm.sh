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

# get git head
TEMP_DIR=$(mktemp)
rm -f ${TEMP_DIR}
mkdir -p ${TEMP_DIR}
(
    cd ${TEMP_DIR}
    git clone git@github.com:theonlydude/RandomMetroidSolver.git
)
ORIG=${TEMP_DIR}/RandomMetroidSolver/
#ORIG=/tmp/tmp.KtU7aob2Ba/RandomMetroidSolver/
#ORIG=.

PRESETS=("regular" "noob" "master")
AREAS=("" "--area")

function generate_params {
    SEED="$1"
    PRESET="$2"

    let S=$RANDOM%${#AREAS[@]}
    AREA=${AREAS[$S]}

    echo "-r ${ROM} --param standard_presets/${PRESET}.json --seed ${SEED} --progressionSpeed random --morphPlacement random --progressionDifficulty random --missileQty 0 --superQty 0 --powerBombQty 0 --minorQty 0 --energyQty random --fullRandomization random --suitsRestriction random --hideItems random --strictMinors random --superFun CombatRandom --superFun MovementRandom --superFun SuitsRandom --maxDifficulty random ${AREA}"
}

function computeSeed {
    # generate seed
    let P=$RANDOM%${#PRESETS[@]}
    PRESET=${PRESETS[$P]}
    SEED="$RANDOM"

    PARAMS=$(generate_params "${SEED}" "${PRESET}")
    CSV=test_jm.csv
    if [ ! -f "${CSV}" ]; then
	echo "seed;diff_cap;rtime old;rtime new;stime old;stime new;;md5sum ok;params;" | tee -a ${CSV}
    fi

    OLD_MD5="old n/a"
    OUT=$(/usr/bin/time -f "\t%E real" python2 ${ORIG}/randomizer.py ${PARAMS} 2>&1)
    if [ $? -ne 0 ]; then
	RTIME_OLD="n/a"
    else
	RTIME_OLD=$(echo "${OUT}" | grep real | awk '{print $1}')
	ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc 2>/dev/null)
	if [ $? -eq 0 ]; then
	    OLD_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
	fi
    fi

#    NEW_MD5="new n/a"
#    OUT=$(/usr/bin/time -f "\t%E real" python2 ./randomizer.py ${PARAMS} 2>&1)
#    if [ $? -ne 0 ]; then
#	RTIME_NEW="n/a"
#    else
#	RTIME_NEW=$(echo "${OUT}" | grep real | awk '{print $1}')
#	ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc 2>/dev/null)
#	if [ $? -eq 0 ]; then
#	    NEW_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
#	fi
#    fi

#    if [ "${OLD_MD5}" != "${NEW_MD5}" ]; then
#	if [ "${OLD_MD5}" = "old n/a" ] && [ "${NEW_MD5}" = "new n/a" ]; then
#	    MD5="n/a"
#	else
#	    MD5="mismatch"
#	    echo "OLD: ${OLD_MD5} NEW: ${NEW_MD5}"
#	    STOP="now"
#	fi
#    else
#	MD5=${OLD_MD5}
#    fi

    # solve seed
    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc)
    if [ $? -ne 0 ]; then
	return
    fi

    OUT=$(/usr/bin/time -f "\t%E real" python2 ${ORIG}/solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g 2>&1) > ${ROM_GEN}.old
    if [ $? -ne 0 ]; then
        echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${PARAMS};" | tee -a ${CSV}
        echo "Can't solve ${ROM_GEN}" | tee -a ${CSV}
        exit 0
	STIME_OLD="n/a"
    else
	STIME_OLD=$(echo "${OUT}" | grep real | awk '{print $1}')
    fi
#    OUT=$(/usr/bin/time -f "\t%E real" python2 ./solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g 2>&1) > ${ROM_GEN}.new
#    if [ $? -ne 0 ]; then
#        echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${PARAMS};" | tee -a ${CSV}
#        echo "Can't solve ${ROM_GEN}" | tee -a ${CSV}
#        exit 0
#	STIME_NEW="n/a"
#    else
#	STIME_NEW=$(echo "${OUT}" | grep real | awk '{print $1}')
#    fi

    echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${PARAMS};" | tee -a ${CSV}

#    DIFF=$(diff ${ROM_GEN}.old ${ROM_GEN}.new)
#
#    if [ -z "${DIFF}" ]; then
	rm -f ${ROM_GEN} ${ROM_GEN}.new ${ROM_GEN}.old
#	echo "${SEED};${ROM_GEN};SOLVER;${PRESET};OK;" | tee -a test_jm.csv
#    else
#	echo "${SEED};${ROM_GEN};SOLVER;${PRESET};NOK;" | tee -a test_jm.csv
#	STOP="now"
#    fi
}

STOP=""
let LOOPS=${LOOPS}/4
for i in $(seq 1 ${LOOPS}); do
    computeSeed &
    computeSeed &
    computeSeed &
    computeSeed &
    wait

    if [ "${STOP}" = "now" ]; then
	exit 1
    fi
done | tee test_jm.log

echo "DONE"
#rm -rf ${TEMP_DIR}

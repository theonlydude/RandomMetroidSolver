#!/bin/bash

# cd to root dir
CWD=$(dirname $0)/..
cd ${CWD}
CWD=$(pwd)
[ -z $PYTHON ] && PYTHON=python3.7

LOG_DIR=${CWD}/logs
mkdir -p ${LOG_DIR}
LOG=${LOG_DIR}/test_jm.log
CSV=${LOG_DIR}/test_jm.csv
> ${LOG}
#> ${CSV}

if [ $# -ne 2 -a $# -ne 3 ]; then
    echo "params: ROM LOOPS [COMPARE]"
    exit -1
fi

ROM=$1
LOOPS=$2
if [ -n "$3" ]; then
    COMPARE=0
else
    COMPARE=1
fi

# get git head
if [ ${COMPARE} -eq 0 ]; then
    TEMP_DIR=$(mktemp)
    rm -f ${TEMP_DIR}
    mkdir -p ${TEMP_DIR}
    (
	cd ${TEMP_DIR}
	git clone git@github.com:theonlydude/RandomMetroidSolver.git
	cd RandomMetroidSolver
	#git reset --hard 14e9088f07f64e093c53b773b016f5042765044b
    )
    ORIG=${TEMP_DIR}/RandomMetroidSolver/
else
    ORIG=.
fi

PRESETS=("regular" "noob" "master")
SUITS=("" "--nogravheatPatch" "--progressiveSuits")
CHARGES=("" "--nerfedCharge")
TWEAKS=("" "--novariatweaks")
LAYOUTS=("" "--nolayout")
STARTAPS=("" "--startAP random")
AREAS=("" "" "--area" "--area --areaLayoutBase")

function generate_params {
    SEED="$1"
    PRESET="$2"

    # optional patches
    let S=$RANDOM%${#SUITS[@]}
    SUIT=${SUITS[$S]}
    let S=$RANDOM%${#CHARGES[@]}
    CHARGE=${CHARGES[$S]}
    let S=$RANDOM%${#TWEAKS[@]}
    TWEAK=${TWEAKS[$S]}
    let S=$RANDOM%${#LAYOUTS[@]}
    LAYOUT=${LAYOUTS[$S]}
    let S=$RANDOM%${#STARTAPS[@]}
    STARTAP=${STARTAPS[$S]}
    let S=$RANDOM%${#AREAS[@]}
    AREA=${AREAS[$S]}

    echo "-r ${ROM} --param standard_presets/${PRESET}.json --seed ${SEED} --progressionSpeed random --morphPlacement random --progressionDifficulty random --missileQty 0 --superQty 0 --powerBombQty 0 --minorQty 0 --energyQty random --majorsSplit random --suitsRestriction random --hideItems random --strictMinors random --superFun CombatRandom --superFun MovementRandom --superFun SuitsRandom --maxDifficulty random --runtime 20 --bosses random ${SUIT} ${CHARGE} ${TWEAK} ${LAYOUT} ${STARTAP} ${AREA}"
}

function computeSeed {
    # generate seed
    let P=$RANDOM%${#PRESETS[@]}
    PRESET=${PRESETS[$P]}
    SEED="$RANDOM$RANDOM$RANDOM$RANDOM"

    PARAMS=$(generate_params "${SEED}" "${PRESET}")

    if [ ${COMPARE} -eq 0 ]; then
	OLD_MD5="old n/a"
	OUT=$(/usr/bin/time -f "\t%E real" $PYTHON ${ORIG}/randomizer.py ${PARAMS} 2>&1)
	if [ $? -ne 0 ]; then
	    echo "${OUT}" >> ${LOG}
	else
	    RTIME_OLD=$(echo "${OUT}" | grep real | awk '{print $1}')
	    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc 2>/dev/null)
	    if [ $? -eq 0 ]; then
		OLD_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
	    fi
	fi
    fi

    NEW_MD5="new n/a"
    OUT=$(/usr/bin/time -f "\t%E real" $PYTHON ./randomizer.py ${PARAMS} 2>&1)
    if [ $? -ne 0 ]; then
	echo "${OUT}" >> ${LOG}
    else
	RTIME_NEW=$(echo "${OUT}" | grep real | awk '{print $1}')
	ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc 2>/dev/null)
	if [ $? -eq 0 ]; then
	    NEW_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
	fi
    fi
    STARTAP_NEW=$(echo "${OUT}" | grep startAP | cut -d ':' -f 2)
    PROGSPEED_NEW=$(echo "${OUT}" | grep progressionSpeed | cut -d ':' -f 2)
    MAJORSSPLIT_NEW=$(echo "${OUT}" | grep majorsSplit | cut -d ':' -f 2)
    MORPH_NEW=$(echo "${OUT}" | grep morphPlacement | cut -d ':' -f 2)

    if [ "${OLD_MD5}" != "${NEW_MD5}" -a ${COMPARE} -eq 0 ]; then
	if [ "${OLD_MD5}" = "old n/a" ] && [ "${NEW_MD5}" = "new n/a" ]; then
	    MD5="n/a"
	else
	    MD5="mismatch"
	    echo "OLD: ${OLD_MD5} NEW: ${NEW_MD5}"
	fi
    else
	MD5=${NEW_MD5}
    fi

    # solve seed
    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc)
    if [ $? -ne 0 ]; then
	echo "error;${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${PARAMS};" | tee -a ${CSV}
	exit 0
    fi

    if [ ${COMPARE} -eq 0 ]; then
	OUT=$(/usr/bin/time -f "\t%E real" $PYTHON ${ORIG}/solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g --checkDuplicateMajor 2>&1)
	if [ $? -ne 0 ]; then
            echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${PARAMS};" | tee -a ${CSV}
            echo "Can't solve ${ROM_GEN}" | tee -a ${CSV}
            exit 0
	    STIME_OLD="n/a"
	else
	    STIME_OLD=$(echo "${OUT}" | grep real | awk '{print $1}')
	    echo "${OUT}" | grep -q "has already been picked up"
	    DUP_OLD=$?
	    echo "${OUT}" | grep -v 'real' > ${ROM_GEN}.old
	fi
    else
	DUP_OLD=1
    fi

    OUT=$(/usr/bin/time -f "\t%E real" $PYTHON ./solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g --checkDuplicateMajor 2>&1)
    if [ $? -ne 0 ]; then
        echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${PARAMS};" | tee -a ${CSV}
        echo "Can't solve ${ROM_GEN}" | tee -a ${CSV}
        exit 0
	STIME_NEW="n/a"
    else
	STIME_NEW=$(echo "${OUT}" | grep real | awk '{print $1}')
	echo "${OUT}" | grep -q "has already been picked up"
	DUP_NEW=$?

	if [ ${COMPARE} -eq 0 ]; then
	    echo "${OUT}" | grep -v 'real' > ${ROM_GEN}.new
	fi
    fi

    if [ ${DUP_NEW} -eq 0 -o ${DUP_OLD} -eq 0 ]; then
	DUP="dup major detected"
    fi
    echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${PARAMS};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${DUP}" | tee -a ${CSV}

    if [ ${COMPARE} -eq 0 ]; then
	DIFF=$(diff ${ROM_GEN}.old ${ROM_GEN}.new)

	if [ -z "${DIFF}" ]; then
	    rm -f ${ROM_GEN} ${ROM_GEN}.new ${ROM_GEN}.old
	    echo "${SEED};${ROM_GEN};SOLVER;${PRESET};OK;" | tee -a ${CSV}
	else
	    echo "${SEED};${ROM_GEN};SOLVER;${PRESET};NOK;" | tee -a ${CSV}
	fi
    else
	rm -f ${ROM_GEN}
    fi
}

function wait_for_a_child {
    PIDS="$1"

    while true; do
	for PID in $PIDS; do
	    kill -0 $PID 2>/dev/null
	    if [ $? -ne 0 ]; then
		PIDS=$(echo "$PIDS" | sed -e "s+ $PID ++")
		return
	    fi
	done
	sleep 1
    done
}

NB_CPU=$(cat /proc/cpuinfo  | grep 'processor' | wc -l)
CUR_JOBS=0
CUR_LOOP=0
PIDS=""
while true; do
    while [ ${CUR_JOBS} -lt ${NB_CPU} -a ${CUR_LOOP} -lt ${LOOPS} ]; do
	computeSeed &
	PIDS="$PIDS $! "
	let CUR_JOBS=$CUR_JOBS+1
	let CUR_LOOP=$CUR_LOOP+1
    done

    wait_for_a_child "${PIDS}"
    let CUR_JOBS=$CUR_JOBS-1

    if [ $CUR_JOBS -eq 0 -a $CUR_LOOP -ge $LOOPS ]; then
	break
    fi
done

echo "DONE"

echo ""
echo "Start AP"
for AP in "Ceres" "Landing Site" "Gauntlet Top" "Green Brinstar Elevator" "Big Pink" "Etecoons Supers" "Wrecked Ship Main" "Business Center" "Bubble Mountain" "Watering Hole" "Red Brinstar Elevator" "Golden Four" "Aqueduct" "Mama Turtle" "Firefleas Top"; do
    TOTAL=$(grep "${AP}" ${CSV}  | wc -l)
    ERROR=$(grep "${AP}" ${CSV} | grep -E '^error' | wc -l)
    PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc)
    printf "%-24s" "${AP}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done
echo ""
echo "Prog speed"
for PROGSPEED in "speedrun" "slowest" "slow" "medium" "fast" "fastest" "VARIAble" "basic"; do
    TOTAL=$(grep "${PROGSPEED}" ${CSV}  | wc -l)
    ERROR=$(grep "${PROGSPEED}" ${CSV} | grep -E '^error' | wc -l)
    PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc)
    printf "%-24s" "${PROGSPEED}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done
echo ""
echo "Majors split"
for MAJORSPLIT in "Major" "Full" "Chozo"; do
    TOTAL=$(grep "${MAJORSPLIT}" ${CSV}  | wc -l)
    ERROR=$(grep "${MAJORSPLIT}" ${CSV} | grep -E '^error' | wc -l)
    PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc)
    printf "%-24s" "${MAJORSPLIT}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done
echo ""
echo "Morph placement"
for MORPH in "early" "normal" "late"; do
    TOTAL=$(grep "${MORPH}" ${CSV}  | wc -l)
    ERROR=$(grep "${MORPH}" ${CSV} | grep -E '^error' | wc -l)
    PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc)
    printf "%-24s" "${MORPH}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done

echo "total: $(wc -l logs/test_jm.csv)"

echo "errors:"
grep -E "NOK|mismatch|Can't solve" ${CSV}
grep Traceback ${LOG}

rm -rf ${TEMP_DIR}

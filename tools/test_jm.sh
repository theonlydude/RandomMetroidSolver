#!/bin/bash
# this script will randomize seeds with random params and solve them to detect mismatch and bugs.
# to monitor a running jm:
# cd logs/
# while true; do grep -v SOLVER test_jm.csv | wc -l ; grep -E "NOK|mismatch|Can't solve" test_jm.csv | grep -v ';speedrun;' ; grep Traceback test_jm.log ; sleep 3; done

# cd to root dir
CWD=$(dirname $0)/..
cd ${CWD}
CWD=$(pwd)
[ -z "$PYTHON" ] && PYTHON=pyston3.8
[ -z "$OLD_PYTHON" ] && OLD_PYTHON=pyston3.8

LOG_DIR=${CWD}/logs
mkdir -p ${LOG_DIR}
LOG=${LOG_DIR}/test_jm.log
CSV=${LOG_DIR}/test_jm.csv
date > ${LOG}
> ${CSV}

if [ $# -ne 2 -a $# -ne 3 ]; then
    echo "params: ROM LOOPS [COMPARE]"
    exit -1
fi

ROM=$1
if [ -n "$3" ]; then
    # add more loops as we filter them out afterward
    FILTER_HEAD=32
    FILTER_TAIL=16
    let LOOPS=$2+${FILTER_HEAD}+${FILTER_TAIL}
    COMPARE=0
else
    FILTER_HEAD=0
    FILTER_TAIL=0
    LOOPS=$2
    COMPARE=1
fi

# get git head
if [ ${COMPARE} -eq 0 ]; then
    TEMP_DIR=$(mktemp)
    rm -f ${TEMP_DIR}
    mkdir -p ${TEMP_DIR}
    (
	cd ${TEMP_DIR}
	git clone --recurse-submodules git@github.com:theonlydude/RandomMetroidSolver.git
	cd RandomMetroidSolver
	#git reset --hard 14e9088f07f64e093c53b773b016f5042765044b
    )
    ORIG=${TEMP_DIR}/RandomMetroidSolver/
else
    ORIG=.
fi

function get_time {
    case $(uname -s) in
        "Darwin")
            echo "gtime"
            ;;
        *)
            echo "/usr/bin/time"
            ;;
    esac
}
TIME=$(get_time)

PRESETS=("regular" "newbie" "master")
CHARGES=("" "--nerfedCharge")
TWEAKS=("" "--novariatweaks")
LAYOUTS=("" "--nolayout")
STARTAPS=("" "--startAP random")
AREAS=("" "" "--area" "--area --areaLayoutBase")
MINIMIZERS=("--bosses random" "--bosses random" "--bosses random" "--area --bosses --minimizer " "--area --bosses --minimizerTourian --minimizer ")
DOORS=("" "" "" "--doorsColorsRando")

function generate_random_list {
    FIRST=0
    while [ $# -ne 0 ]; do
        if [ ${RANDOM} -gt 10000 ]; then
            if [ ${FIRST} -eq 0 ]; then
                FIRST=1
                echo -en "${1}"
            else
                echo -en ",${1}"
            fi
        fi
        shift
    done
}

function generate_multi_select {
    NAME="${1}"
    shift

    MULTISELECTLIST=$(generate_random_list $*)

    if [ -n "${MULTISELECTLIST}" ]; then
        echo "--${NAME}List ${MULTISELECTLIST}"
    fi
}

function generate_params {
    SEED="$1"
    PRESET="$2"

    # optional patches
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
    let S=$RANDOM%${#MINIMIZERS[@]}
    MINIMIZER=${MINIMIZERS[$S]}
    if(echo "${MINIMIZER}" | grep -q minimizer); then
        MINIMIZER="${MINIMIZER} $(echo 35+$RANDOM%65 | bc)"
    fi
    let S=$RANDOM%${#DOORS[@]}
    DOOR=${DOORS[$S]}

    MAJORS_SPLIT_LIST=$(generate_multi_select "majorsSplit" 'Full' 'Major' 'Chozo')
    PROGRESSION_DIFFICULTY_LIST=$(generate_multi_select "progressionDifficulty" 'easier' 'normal' 'harder')
    MORPH_PLACEMENT_LIST=$(generate_multi_select "morphPlacement" 'early' 'late' 'normal')
    ENERGY_QTY_LIST=$(generate_multi_select "energyQty" 'ultra_sparse' 'sparse' 'medium' 'vanilla')
    GRAVITY_BEHAVIOUR_LIST=$(generate_multi_select "gravityBehaviour" 'Vanilla' 'Balanced' 'Progressive')

    if [ -n "${STARTAP}" ]; then
        START_LOCATION_LIST=$(generate_multi_select "startLocation" "Ceres" "Landing_Site" "Gauntlet_Top" "Green_Brinstar_Elevator" "Big_Pink" "Etecoons_Supers" "Wrecked_Ship_Main" "Firefleas_Top" "Business_Center" "Bubble_Mountain" "Mama_Turtle" "Watering_Hole" "Aqueduct" "Red_Brinstar_Elevator" "Golden_Four")
    fi

    echo "-r ${ROM} --param standard_presets/${PRESET}.json --seed ${SEED} --progressionSpeed random --progressionSpeedList slowest,slow,medium,fast,fastest,VARIAble,speedrun --morphPlacement random ${MORPH_PLACEMENT_LIST} --progressionDifficulty random ${PROGRESSION_DIFFICULTY_LIST} --missileQty 0 --superQty 0 --powerBombQty 0 --minorQty 0 --energyQty random ${ENERGY_QTY_LIST} --majorsSplit random ${MAJORS_SPLIT_LIST} --suitsRestriction random --hideItems random --strictMinors random --superFun CombatRandom --superFun MovementRandom --superFun SuitsRandom --maxDifficulty random --runtime 20 --escapeRando random --gravityBehaviour random ${GRAVITY_BEHAVIOUR_LIST} ${CHARGE} ${TWEAK} ${LAYOUT} ${STARTAP} ${START_LOCATION_LIST} ${AREA} ${MINIMIZER} ${DOOR} --jm"
}

function computeSeed {
    # generate seed
    let P=$RANDOM%${#PRESETS[@]}
    PRESET=${PRESETS[$P]}
    SEED="$RANDOM$RANDOM$RANDOM$RANDOM"

    PARAMS=$(generate_params "${SEED}" "${PRESET}")

    if [ ${COMPARE} -eq 0 ]; then
	OLD_MD5="old n/a"
	RANDO_OUT=$(${TIME} -f "\t%E real" $OLD_PYTHON ${ORIG}/randomizer.py ${PARAMS} 2>&1)
	if [ $? -ne 0 ]; then
	    echo "${RANDO_OUT}" >> ${LOG}
	else
	    RTIME_OLD=$(echo "${RANDO_OUT}" | grep real | awk '{print $1}')
	    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc 2>/dev/null)
	    if [ $? -eq 0 ]; then
		OLD_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
	    fi
	fi
    fi

    NEW_MD5="new n/a"
    echo $PYTHON ./randomizer.py ${PARAMS}
    RANDO_OUT=$(${TIME} -f "\t%E real" $PYTHON ./randomizer.py ${PARAMS} 2>&1)
    if [ $? -ne 0 ]; then
	echo "${RANDO_OUT}" >> ${LOG}
    else
	RTIME_NEW=$(echo "${RANDO_OUT}" | grep real | awk '{print $1}')
	ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}.sfc 2>/dev/null)
	if [ $? -eq 0 ]; then
	    NEW_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
	fi
    fi
    STARTAP_NEW=$(echo "${RANDO_OUT}" | grep startAP | cut -d ':' -f 2)
    PROGSPEED_NEW=$(echo "${RANDO_OUT}" | grep progressionSpeed | cut -d ':' -f 2)
    MAJORSSPLIT_NEW=$(echo "${RANDO_OUT}" | grep majorsSplit | cut -d ':' -f 2)
    MORPH_NEW=$(echo "${RANDO_OUT}" | grep morphPlacement | cut -d ':' -f 2)

    if [ "${OLD_MD5}" != "${NEW_MD5}" -a ${COMPARE} -eq 0 ]; then
	if [ "${OLD_MD5}" = "old n/a" ] && [ "${NEW_MD5}" = "new n/a" ]; then
	    MD5="n/a"
	else
            if [ "${OLD_MD5}" = "old n/a" ]; then
                MD5="old too slow"
            else
	        MD5="mismatch"
	        echo "OLD: ${OLD_MD5} NEW: ${NEW_MD5}"
            fi
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
	SOLVER_OUT=$(${TIME} -f "\t%E real" $OLD_PYTHON ${ORIG}/solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g --checkDuplicateMajor 2>&1)
	if [ $? -ne 0 ]; then
            echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${PARAMS};" | tee -a ${CSV}
            echo "Can't solve ${ROM_GEN}" | tee -a ${CSV}
            echo "${RANDO_OUT}" >> ${LOG}
            echo "${SOLVER_OUT}" >> ${LOG}
            exit 0
	    STIME_OLD="n/a"
	else
	    STIME_OLD=$(echo "${SOLVER_OUT}" | grep real | awk '{print $1}')
	    echo "${SOLVER_OUT}" | grep -q "has already been picked up"
	    DUP_OLD=$?
	    echo "${SOLVER_OUT}" | grep -v 'real' > ${ROM_GEN}.old
	fi
    else
	DUP_OLD=1
    fi

    SOLVER_OUT=$(${TIME} -f "\t%E real" $PYTHON ~/RandomMetroidSolver/solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g --checkDuplicateMajor 2>&1)
    if [ $? -ne 0 ]; then
        echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${PARAMS};" | tee -a ${CSV}
        echo "Can't solve ${ROM_GEN}" | tee -a ${CSV}
        echo "${RANDO_OUT}" >> ${LOG}
        echo "${SOLVER_OUT}" >> ${LOG}
        exit 0
	STIME_NEW="n/a"
    else
	STIME_NEW=$(echo "${SOLVER_OUT}" | grep real | awk '{print $1}')
	echo "${SOLVER_OUT}" | grep -q "has already been picked up"
	DUP_NEW=$?

	if [ ${COMPARE} -eq 0 ]; then
	    echo "${SOLVER_OUT}" | grep -v 'real' > ${ROM_GEN}.new
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

function get_cpu {
    case $(uname -s) in
        "Darwin")
            sysctl -n hw.ncpu
            ;;
        *)
            cat /proc/cpuinfo  | grep 'processor' | wc -l
            ;;
    esac
}

NB_CPU=$(get_cpu)
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
date >> ${LOG}

echo ""
echo "Start AP"
for AP in "Ceres" "Landing Site" "Gauntlet Top" "Green Brinstar Elevator" "Big Pink" "Etecoons Supers" "Wrecked Ship Main" "Business Center" "Bubble Mountain" "Watering Hole" "Red Brinstar Elevator" "Golden Four" "Aqueduct" "Mama Turtle" "Firefleas Top"; do
    TOTAL=$(grep ";${AP};" ${CSV}  | wc -l)
    ERROR=$(grep ";${AP};" ${CSV} | grep -E '^error' | wc -l)
    [ ${TOTAL} -ne 0 ] && PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc) || PERCENT='n/a'
    printf "%-24s" "${AP}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done
echo ""
echo "Prog speed"
for PROGSPEED in "speedrun" "slowest" "slow" "medium" "fast" "fastest" "VARIAble"; do
    TOTAL=$(grep ";${PROGSPEED};" ${CSV}  | wc -l)
    ERROR=$(grep ";${PROGSPEED};" ${CSV} | grep -E '^error' | wc -l)
    [ ${TOTAL} -ne 0 ] && PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc) || PERCENT='n/a'
    printf "%-24s" "${PROGSPEED}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done
echo ""
echo "Majors split"
for MAJORSPLIT in "Major" "Full" "Chozo"; do
    TOTAL=$(grep ";${MAJORSPLIT};" ${CSV}  | wc -l)
    ERROR=$(grep ";${MAJORSPLIT};" ${CSV} | grep -E '^error' | wc -l)
    [ ${TOTAL} -ne 0 ] && PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc) || PERCENT='n/a'
    printf "%-24s" "${MAJORSPLIT}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done
echo ""
echo "Morph placement"
for MORPH in "early" "normal" "late"; do
    TOTAL=$(grep ";${MORPH};" ${CSV}  | wc -l)
    ERROR=$(grep ";${MORPH};" ${CSV} | grep -E '^error' | wc -l)
    [ ${TOTAL} -ne 0 ] && PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc) || PERCENT='n/a'
    printf "%-24s" "${MORPH}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done

TOTAL_COUNT=$(wc -l ${CSV} | awk '{print $1}')
echo "total: ${TOTAL_COUNT}"
ERRORS_COUNT=$(grep -E "^error" ${CSV} | wc -l)
echo "errors: ${ERRORS_COUNT}/${TOTAL_COUNT}"
grep DIAG ${LOG} | sed -e 's+\*++g' -e 's+Super Fun : Could not remove any suit++' | sort | uniq -c

echo "errors detail:"
if [ ${COMPARE} -eq 0 ]; then
    # speedrun seeds are non deterministic, so filter them out in compare mode.
    grep -E "NOK|mismatch|Can't solve" ${CSV} | grep -v ';speedrun;'
else
    grep -E "NOK|Can't solve" ${CSV}
fi
grep Traceback ${LOG}

function getTime {
    # speedrun seeds are non deterministics, filter them out.
    # ignore the first and last lines, as there's always a big time difference in them.
    COLUMN="${1}"
    KEEP_SPEEDRUN="${2}"
    if [ -n "${KEEP_SPEEDRUN}" ]; then
        SPEEDRUN=""
        GREP_V=""
    else
        SPEEDRUN="|;speedrun;"
        GREP_V="-v"
    fi

    grep -v SOLVER ${CSV} | tail -n +${FILTER_HEAD} | head -n -${FILTER_TAIL} | grep -v -E "^error${SPEEDRUN}" | grep ${GREP_V} '^[0-9]*;;;' | cut -d ';' -f ${COLUMN} | sed -e 's+0:++g' | awk -F';' '{sum+=$1;} END{print sum}'
}

if [ ${COMPARE} -eq 0 ]; then
    RANDOTIME_BEFORE=$(getTime 3)
    RANDOTIME_AFTER=$(getTime 4)
    SOLVERTIME_BEFORE=$(getTime 5)
    SOLVERTIME_AFTER=$(getTime 6)
    RANDO_PERCENT=$(echo "scale=4; (${RANDOTIME_AFTER} - ${RANDOTIME_BEFORE}) / ${RANDOTIME_BEFORE} * 100" | bc -l)
    SOLVER_PERCENT=$(echo "scale=4; (${SOLVERTIME_AFTER} - ${SOLVERTIME_BEFORE}) / ${SOLVERTIME_BEFORE} * 100" | bc -l)
    echo "Speed increase/decrease:"
    echo "rando:  ${RANDO_PERCENT}%"
    echo "solver: ${SOLVER_PERCENT}%"
else
    # display average randomizer and solver time
    RANDOTIME=$(getTime 4 "keep")
    SOLVERTIME=$(getTime 6 "keep")
    OK_SEEDS=$(grep -v SOLVER ${CSV} | grep -v -E "^error" | grep '^[0-9]*;;;' | wc -l)
    AVG_RANDO=$(echo "scale=2; ${RANDOTIME}/${OK_SEEDS}" | bc -l)
    AVG_SOLVER=$(echo "scale=2; ${SOLVERTIME}/${OK_SEEDS}" | bc -l)

    echo "Avg times:"
    echo "rando: ${AVG_RANDO}"
    echo "solver: ${AVG_SOLVER}"
fi

rm -rf ${TEMP_DIR}

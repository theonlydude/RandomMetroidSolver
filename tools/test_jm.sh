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

function generate_random_list {
    FIRST=0
    while [ $# -ne 0 ]; do
        if [ ${RANDOM} -ge 16384 ]; then
            if [ ${FIRST} -eq 0 ]; then
                FIRST=1
                echo -en "\"${1}\""
            else
                echo -en ", \"${1}\""
            fi
        fi
        shift
    done
}

function generate_multi_select {
    NAME="${1}"
    shift

    # have to use '_' for values with space in them
    MULTISELECTLIST=$(generate_random_list $* | sed -e 's+_+ +g')

    if [ -n "${MULTISELECTLIST}" ]; then
        echo "\"${NAME}MultiSelect\": [${MULTISELECTLIST}],"
    fi
}

function generate_params {
    local SEED="$1"
    local PRESET="$2"
    local RANDO_PRESET="$3"

    echo "-r ${ROM} --param standard_presets/${PRESET}.json --seed ${SEED} --randoPreset ${RANDO_PRESET} --jm --runtime 20"
}

function random_switch {
    if [ ${RANDOM} -ge 16384 ]; then
        echo -en "on"
    else
        echo -en "off"
    fi
}

function random_select {
    local MIN=1
    local MAX=$#
    local CHOICE=$(shuf -i ${MIN}-${MAX} -n 1)
    echo "\"`eval echo \"$\"\"$CHOICE\"`\""
}

function generate_rando_presets {
    local SEED="$1"
    local PRESET="$2"
    local RANDO_PRESET=$(mktemp)

    cat > ${RANDO_PRESET} <<EOF
{
    "seed": "${SEED}",
    "preset": "${PRESET}",
    "startLocation": "random",
    $(generate_multi_select "startLocation" "Ceres" "Landing_Site" "Gauntlet_Top" "Green_Brinstar_Elevator" "Big_Pink" "Etecoons_Supers" "Wrecked_Ship_Main" "Firefleas_Top" "Business_Center" "Bubble_Mountain" "Mama_Turtle" "Watering_Hole" "Aqueduct" "Red_Brinstar_Elevator" "Golden_Four")
    "majorsSplit": "random",
    $(generate_multi_select "majorsSplit" 'Full' 'Major' 'Chozo' 'FullWithHUD' 'Scavenger')
    "scavNumLocs": "$(shuf -i 4-10 -n 1)",
    "scavRandomized": "$(random_switch)",
    "maxDifficulty": "random",
    "progressionSpeed": "random",
    $(generate_multi_select "progressionSpeed" 'slowest' 'slow' 'medium' 'fast' 'fastest' 'VARIAble' 'speedrun')
    "progressionDifficulty": "random",
    $(generate_multi_select "progressionDifficulty" 'easier' 'normal' 'harder')
    "morphPlacement": "random",
    $(generate_multi_select "morphPlacement" 'early' 'late' 'normal')
    "suitsRestriction": "$(random_switch)",
    "hideItems": "$(random_switch)",
    "strictMinors": "$(random_switch)",
    "missileQty": "0",
    "superQty": "0",
    "powerBombQty": "0",
    "minorQty": "0",
    "energyQty": "random",
    $(generate_multi_select "energyQty" 'ultra_sparse' 'sparse' 'medium' 'vanilla')
    "objective": "random",
    $(generate_multi_select "objective" "kill_kraid" "kill_phantoon" "kill_draygon" "kill_ridley" "kill_one_G4" "kill_two_G4" "kill_three_G4" "kill_all_G4" "kill_spore_spawn" "kill_botwoon" "kill_crocomire" "kill_golden_torizo" "kill_one_miniboss" "kill_two_minibosses" "kill_three_minibosses" "kill_all_mini_bosses" "nothing" "collect_25%_items" "collect_50%_items" "collect_75%_items" "collect_100%_items" "collect_all_upgrades" "clear_crateria" "clear_green_brinstar" "clear_red_brinstar" "clear_wrecked_ship" "clear_kraid's_lair" "clear_upper_norfair" "clear_croc's_lair" "clear_lower_norfair" "clear_west_maridia" "clear_east_maridia" "tickle_the_red_fish" "kill_the_orange_geemer" "kill_shaktool" "activate_chozo_robots" "visit_the_animals" "kill_king_cacatac")
    "areaRandomization": "random",
    "areaLayout": "$(random_switch)",
    "doorsColorsRando": "$(random_switch)",
    "allowGreyDoors": "$(random_switch)",
    "bossRandomization": "$(random_switch)",
    "minimizer": "$(random_switch)",
    "minimizerQty": "$(shuf -i 35-100 -n 1)",
    "tourian": "random",
    $(generate_multi_select "tourian" "Vanilla" "Fast" "Disabled")
    "escapeRando": "$(random_switch)",
    "removeEscapeEnemies": "$(random_switch)",
    "funCombat": "$(random_switch)",
    "funMovement": "$(random_switch)",
    "funSuits": "$(random_switch)",
    "layoutPatches": "$(random_switch)",
    "variaTweaks": "$(random_switch)",
    "nerfedCharge": "$(random_switch)",
    "relaxed_round_robin_cf": "$(random_switch)",
    "gravityBehaviour":  "random",
    $(generate_multi_select "gravityBehaviour" 'Vanilla' 'Balanced' 'Progressive')
    "itemsounds": "$(random_switch)",
    "elevators_speed": "$(random_switch)",
    "fast_doors": "$(random_switch)",
    "spinjumprestart": "$(random_switch)",
    "rando_speed": "$(random_switch)",
    "Infinite_Space_Jump": "$(random_switch)",
    "refill_before_save": "$(random_switch)",
    "hud": "$(random_switch)",
    "animals": "$(random_switch)",
    "No_Music": "$(random_switch)",
    "random_music": "$(random_switch)"
}
EOF

    echo -en "${RANDO_PRESET}"
}

function computeSeed {
    # generate seed
    let P=$RANDOM%${#PRESETS[@]}
    local PRESET=${PRESETS[$P]}
    local SEED=$(od -vAn -N8 -t u8 < /dev/urandom | awk '{print $1}')

    local RANDO_PRESET=$(generate_rando_presets "${SEED}" "${PRESET}")
    local PARAMS=$(generate_params "${SEED}" "${PRESET}" "${RANDO_PRESET}")

    if [ ${COMPARE} -eq 0 ]; then
	OLD_MD5="old n/a"
	RANDO_OUT=$(${TIME} -f "\t%E real" $OLD_PYTHON ${ORIG}/randomizer.py ${PARAMS} 2>&1)
	if [ $? -ne 0 ]; then
	    echo "${RANDO_OUT}" >> ${LOG}
	else
	    RTIME_OLD=$(echo "${RANDO_OUT}" | grep real | awk '{print $1}')
	    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}*.sfc 2>/dev/null)
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
	ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}*.sfc 2>/dev/null)
	if [ $? -eq 0 ]; then
	    NEW_MD5=$(md5sum ${ROM_GEN} | awk '{print $1}')
	fi
    fi
    STARTAP_NEW=$(echo "${RANDO_OUT}" | grep ^startLocation | cut -d ':' -f 2)
    PROGSPEED_NEW=$(echo "${RANDO_OUT}" | grep ^progressionSpeed | cut -d ':' -f 2)
    MAJORSSPLIT_NEW=$(echo "${RANDO_OUT}" | grep ^majorsSplit | cut -d ':' -f 2)
    MORPH_NEW=$(echo "${RANDO_OUT}" | grep ^morphPlacement | cut -d ':' -f 2)
    OBJECTIVES=$(echo "${RANDO_OUT}" | grep ^objectives | cut -d ':' -f 2)

    RANDO_PRESET_NEW="logs/${SEED}_${PRESET}_${PROGSPEED_NEW}.json"

    if [ "${OLD_MD5}" != "${NEW_MD5}" -a ${COMPARE} -eq 0 ]; then
	if [ "${OLD_MD5}" == "old n/a" ] && [ "${NEW_MD5}" == "new n/a" ]; then
	    MD5="n/a"
	else
            if [ "${OLD_MD5}" == "old n/a" ]; then
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
    ROM_GEN=$(ls -1 VARIA_Randomizer_*X${SEED}_${PRESET}*.sfc)
    if [ $? -ne 0 ]; then
	echo "error;${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${PRESET};${OBJECTIVES}" | tee -a ${CSV}
        mv ${RANDO_PRESET} ${RANDO_PRESET_NEW}
	exit 0
    fi

    RANDO_PRESET_NEW="logs/${ROM_GEN}.json"
    mv ${RANDO_PRESET} ${RANDO_PRESET_NEW}

    if [ ${COMPARE} -eq 0 ]; then
	SOLVER_OUT=$(${TIME} -f "\t%E real" $OLD_PYTHON ${ORIG}/solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g --checkDuplicateMajor --runtime 10 --pickupStrategy all 2>&1)
	if [ $? -ne 0 ]; then
            echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${PRESET};${OBJECTIVES}" | tee -a ${CSV}
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

    SOLVER_OUT=$(${TIME} -f "\t%E real" $PYTHON ~/RandomMetroidSolver/solver.py -r ${ROM_GEN} --preset standard_presets/${PRESET}.json -g --checkDuplicateMajor --runtime 10 --pickupStrategy all 2>&1)
    if [ $? -ne 0 ]; then
        echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${PRESET}" | tee -a ${CSV}
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
    echo "${SEED};${DIFF_CAP};${RTIME_OLD};${RTIME_NEW};${STIME_OLD};${STIME_NEW};${MD5};${STARTAP_NEW};${PROGSPEED_NEW};${MAJORSSPLIT_NEW};${MORPH_NEW};${DUP};${PRESET};${OBJECTIVES}" | tee -a ${CSV}

    if [ ${COMPARE} -eq 0 ]; then
	DIFF=$(diff ${ROM_GEN}.old ${ROM_GEN}.new)

	if [ -z "${DIFF}" ]; then
	    rm -f ${ROM_GEN} ${ROM_GEN}.new ${ROM_GEN}.old ${RANDO_PRESET_NEW}
	    echo "${SEED};${ROM_GEN};SOLVER;${PRESET};OK;" | tee -a ${CSV}
	else
	    echo "${SEED};${ROM_GEN};SOLVER;${PRESET};NOK;" | tee -a ${CSV}
	fi
    else
	rm -f ${ROM_GEN} ${ROM_GEN}.json
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
for MAJORSPLIT in "Major" "Full" "Chozo" "FullWithHUD" "Scavenger"; do
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
echo ""
echo "Objectives"
for OBJ in "kill kraid" "kill phantoon" "kill draygon" "kill ridley" "kill one G4" "kill two G4" "kill three G4" "kill all G4" "kill spore spawn" "kill botwoon" "kill crocomire" "kill golden torizo" "kill one miniboss" "kill two minibosses" "kill three minibosses" "kill all mini bosses" "collect 25% items" "collect 50% items" "collect 75% items" "collect 100% items" "collect all upgrades" "clear crateria" "clear green brinstar" "clear red brinstar" "clear wrecked ship" "clear kraid's lair" "clear upper norfair" "clear croc's lair" "clear lower norfair" "clear west maridia" "clear east maridia" "tickle the red fish" "kill the orange geemer" "kill shaktool" "activate chozo robots" "visit the animals" "kill king cacatac"; do
    TOTAL=$(grep "${OBJ}" ${CSV}  | wc -l)
    ERROR=$(grep "${OBJ}" ${CSV} | grep -E '^error' | wc -l)
    [ ${TOTAL} -ne 0 ] && PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc) || PERCENT='n/a'
    printf "%-24s" "${OBJ}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done
echo ""
echo "Skill preset"
for PRESET in "regular" "newbie" "master"; do
    TOTAL=$(grep "${PRESET}" ${CSV}  | wc -l)
    ERROR=$(grep "${PRESET}" ${CSV} | grep -E '^error' | wc -l)
    [ ${TOTAL} -ne 0 ] && PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc) || PERCENT='n/a'
    printf "%-24s" "${PRESET}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
done

echo ""
echo "Parameters combinations failure"
for PROGSPEED in "speedrun" "slowest" "slow" "medium" "fast" "fastest" "VARIAble"; do
    for MAJORSPLIT in "Major" "Full" "Chozo" "FullWithHUD" "Scavenger"; do
        TOTAL=$(grep ";${MAJORSPLIT};" ${CSV} | grep ";${PROGSPEED};" | wc -l)
        ERROR=$(grep ";${MAJORSPLIT};" ${CSV} | grep ";${PROGSPEED};" | grep -E '^error' | wc -l)
        if [ ${TOTAL} -ne 0 -a ${ERROR} -ne 0 ]; then
            PERCENT=$(echo "${ERROR}*100/${TOTAL}" | bc)
            printf "%-24s" "${PROGSPEED}:${MAJORSPLIT}"; echo "error ${ERROR}/${TOTAL} = ${PERCENT}%"
        fi
    done
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

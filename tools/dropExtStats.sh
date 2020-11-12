#!/bin/bash

CWD=$(dirname $0)/..
cd ${CWD}
CWD=$(pwd)

[ -f "db_params.py" ] || exit 1


function getDBParam {
    PARAM="$1"

    sed -e "s+.*${PARAM}=\([^,)]*\).*+\1+" ${CWD}/db_params.py | sed -e "s+'++g"
}

function info {
    MSG="$*"
    echo "$(date '+%Y/%m/%d_%H:%M:%S'): ${MSG}"
}

info "Get database parameters"

host=$(getDBParam "host")
user=$(getDBParam "user")
database=$(getDBParam "database")
password=$(getDBParam "password")
port=$(getDBParam "port")

info "Dropping extended stats"

SQL="truncate table difficulties;
truncate table extended_stats;
truncate table item_locs;
truncate table solver_stats;
truncate table techniques;"
echo "${SQL}" | mysql -h ${host} -u ${user} -p${password} -P${port} ${database}

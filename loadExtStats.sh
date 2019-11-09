#!/bin/bash

CWD=$(dirname $0)
cd ${CWD}

[ -f "db_params.py" ] || exit 1

function getDBParam {
    PARAM="$1"

    sed -e "s+.*${PARAM}='\([^']*\)'.*+\1+" db_params.py
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

info "Start loading extended stats"

for SQL in $(ls -1 extStats_*.sql); do
    echo "source ${SQL};" | mysql -h ${host} -u ${user} -p${password} ${database} > ${SQL}.log 2>&1 &
done

wait

info "Done"

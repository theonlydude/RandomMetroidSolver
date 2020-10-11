#!/bin/bash
# build and run mysql & varia docker images
# ./build_run.sh -b master [-d path/to/dump.sql] [-t path/to/token_file]
# -b branch: optional  branch to checkout on varia git repo (default to master)
# -d dump: optional dump to import in db to populate it with data
# -t token_file: optional github token to git clone and git pull.
#                if not provided download the repo as a zip.

# cd to root dir
CWD=$(dirname $0)
cd ${CWD}
CWD=$(pwd)

BRANCH="master"
DUMP=""
GITHUB_TOKEN=""
while getopts "b:d:t:" ARG; do
    case ${ARG} in
        b) export BRANCH="${OPTARG}";;
        d) export DUMP="${OPTARG}";;
        t) export GITHUB_TOKEN="${OPTARG}";;
	*) echo "Unknown option ${ARG}"; exit 0;;
    esac
done

# custom network
docker network create varia-network

# mysql init files
if [ -z "${DUMP}" ]; then
    touch mysql/dump.sql
else
    cp -p ${DUMP} mysql/dump.sql
fi
# tables creation
cp ../database/*.sql mysql/

# mysql image build & run
docker build --tag varia-mysql -f mysql/Dockerfile mysql/ &&
docker run --network varia-network --link varia-mysql:varia-mysql --name varia-mysql --publish 3366:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=varia -e MYSQL_USER=varia -e MYSQL_PASSWORD=varia -d varia-mysql

# web2py + varia image build & run
if [ -n "${GITHUB_TOKEN}" ]; then
    GITHUB_TOKEN=$(cat ${GITHUB_TOKEN})
fi
docker build --tag varia-${BRANCH} --build-arg BRANCH=${BRANCH} --build-arg GITHUB_TOKEN=${GITHUB_TOKEN} -f web2py/Dockerfile web2py/ &&
docker run --network varia-network --link varia-${BRANCH}:varia-${BRANCH} -d --publish 8000:8000 --name varia-${BRANCH} varia-${BRANCH}

rm -f mysql/*.sql

# to check web2py logs:
# docker exec varia-master ls -lhrt /var/log/supervisor/
# docker exec varia-master cat /var/log/supervisor/web2py-stdout---supervisor-xxxxxx.log

# to update git repo:
# docker exec -w /root/RandomMetroidSolver varia-master git pull

#!/bin/bash
# build mysql & varia docker images
# ./build.sh -b master [-d path/to/dump.sql] [-t path/to/token_file]
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
LOCAL=1
while getopts "b:d:t:l" ARG; do
    case ${ARG} in
        b) export BRANCH="${OPTARG}";;
        d) export DUMP="${OPTARG}";;
        t) export GITHUB_TOKEN="${OPTARG}";;
        l) export LOCAL=0;;
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

# mysql image build
docker build --tag varia-mysql -f mysql/Dockerfile mysql/ &&

# web2py + varia image build
if [ -n "${GITHUB_TOKEN}" ]; then
    GITHUB_TOKEN=$(cat ${GITHUB_TOKEN})
fi
rm -f web2py/RandomMetroidSolver.tar.gz
if [ ${LOCAL} -eq 0 ]; then
    tar zcf web2py/RandomMetroidSolver.tar.gz --exclude=RandomMetroidSolver.tar.gz --exclude=.git --exclude=*.pyc ../..
else
    touch web2py/RandomMetroidSolver.tar.gz
fi
docker build --tag varia-${BRANCH} --build-arg BRANCH=${BRANCH} --build-arg GITHUB_TOKEN=${GITHUB_TOKEN} --build-arg LOCAL=${LOCAL} -f web2py/Dockerfile web2py/ &&

rm -f mysql/*.sql web2py/RandomMetroidSolver.tar.gz

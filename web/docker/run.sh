#!/bin/bash
# run mysql & varia docker images
# ./run.sh -b master
# -b branch: optional branch checkouted during build (default to master)
# -l local: if set, the docker image will use the local files instead of cloning
#           the repository from github

BRANCH="master"
LOCAL=""
while getopts "b:l:" ARG; do
    case ${ARG} in
        b) export BRANCH="${OPTARG}";;
        l) export LOCAL="${OPTARG}";;
	*) echo "Unknown option ${ARG}"; exit 0;;
    esac
done

# mysql image run
docker run --network varia-network --link varia-mysql:varia-mysql --name varia-mysql --publish 0.0.0.0:3366:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=varia -e MYSQL_USER=varia -e MYSQL_PASSWORD=varia -d varia-mysql

if [ -n "${LOCAL}" ]; then
    echo "local mode"
    # TODO: Figure out how to get this path dynamically
    docker run -v $(pwd)/web:/root/RandomMetroidSolver/web --network varia-network --link varia-${BRANCH}:varia-${BRANCH} -d --publish 0.0.0.0:8000:8000 --name varia-${BRANCH} varia-${BRANCH}
else
    echo "production mode"
    docker run --network varia-network --link varia-${BRANCH}:varia-${BRANCH} -d --publish 0.0.0.0:8000:8000 --name varia-${BRANCH} varia-${BRANCH}
fi

# to check web2py logs:
# docker exec varia-master ls -lhrt /var/log/supervisor/
# docker exec varia-master cat /var/log/supervisor/web2py-stdout---supervisor-xxxxxx.log

# to update git repo:
# docker exec -w /root/RandomMetroidSolver varia-master git pull

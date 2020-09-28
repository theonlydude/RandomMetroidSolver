#!/bin/bash
# build and run mysql & varia docker images
# parameter1: the branch to checkout on varia git repo
# parameter2: optional dump to import in db

# cd to root dir
CWD=$(dirname $0)
cd ${CWD}
CWD=$(pwd)

BRANCH="${1:-master}"
DUMP="${2}"

# mysql init files
if [ -z "${DUMP}" ]; then
    touch mysql/dump.sql
else
    cp -p ${DUMP} mysql/dump.sql
fi
cp ../database/*.sql mysql/

# mysql image build & run
docker build --tag varia-mysql --build-arg DUMP="${DUMP}" -f mysql/Dockerfile mysql/ &&
docker run --name varia-mysql --publish 3366:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=varia -e MYSQL_USER=varia -e MYSQL_PASSWORD=varia -d varia-mysql &&

# web2py + varia image build & run
HOSTNAME=127.0.0.1
docker build --tag varia-${BRANCH} --build-arg BRANCH=${BRANCH} --build-arg HOSTNAME=${HOSTNAME} -f web2py/Dockerfile web2py/ &&
docker run -d --name varia-${BRANCH} --network="host" varia-${BRANCH}

# to check web2py logs:
# docker exec varia-master ls -lhrt /var/log/supervisor/
# docker exec varia-master cat /var/log/supervisor/web2py-stdout---supervisor-xxxxxx.log

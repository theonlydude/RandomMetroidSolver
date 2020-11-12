#!/bin/bash
# remove all varia containers/images/network

docker container ls -a | grep 'varia' | awk '{print $1}' | while read CONTAINER_ID; do docker container rm -f ${CONTAINER_ID}; done
docker image ls | grep varia | awk '{print $3}' | while read IMAGE_ID; do docker image rm ${IMAGE_ID}; done
docker network ls | grep varia | awk '{print $1}' | while read NETWORK_ID; do docker network rm ${NETWORK_ID}; done

echo "done"

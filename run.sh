#!/bin/bash -eu

export ENV=${1:-dev}

cleanup() {
  docker-compose -p tldrify-$ENV down
}

trap cleanup EXIT

[ -d vol/mysql_data ] || mkdir -p vol/mysql_data

exec docker-compose -p tldrify-$ENV up \
  --force-recreate --build --abort-on-container-exit

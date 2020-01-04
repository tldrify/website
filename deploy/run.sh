#!/bin/bash -eu

if [ ! -f LICENSE ]; then
  echo "ERROR: The script must be invoked from the project root!"
  exit 1
fi

export ENV=${ENV:-dev}

cleanup() {
  docker-compose -p tldrify-$ENV -f deploy/docker-compose.yml down
}

trap cleanup EXIT

[ -d deploy/vol ] || mkdir -p deploy/vol

exec docker-compose -p tldrify-$ENV -f deploy/docker-compose.yml up \
  --remove-orphans --force-recreate --build --abort-on-container-exit

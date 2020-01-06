#!/bin/bash -eu

if [ ! -f LICENSE ]; then
  echo "ERROR: The script must be invoked from the project root!"
  exit 1
fi

cleanup() {
  docker-compose -p tldrify-test -f ci/docker-compose.yml down
  docker-compose -p tldrify-test -f ci/docker-compose.yml rm
}

trap cleanup EXIT

exec docker-compose -p tldrify-test -f ci/docker-compose.yml up \
  --remove-orphans --force-recreate --build --abort-on-container-exit --exit-code-from test

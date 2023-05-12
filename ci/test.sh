#!/bin/bash -eu

if [ ! -f LICENSE ]; then
  echo "ERROR: The script must be invoked from the project root!"
  exit 1
fi

if which docker-compose >/dev/null 2>&1; then
  COMPOSE=docker-compose
elif which podman-compose >/dev/null 2>&1; then
  COMPOSE=podman-compose
else
  echo "ERROR: You must install 'docker-compose' or 'podman-compose' first!"
  exit 1
fi

cleanup() {
  $COMPOSE -p tldrify-test -f ci/docker-compose.yml down
  $COMPOSE -p tldrify-test -f ci/docker-compose.yml rm
}

trap cleanup EXIT

exec $COMPOSE -p tldrify-test -f ci/docker-compose.yml up \
  --remove-orphans --force-recreate --build --abort-on-container-exit --exit-code-from test

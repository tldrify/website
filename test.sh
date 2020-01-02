#!/bin/bash -eu

cleanup() {
  docker-compose -p tldrify-test -f docker-compose-test.yml down
  docker-compose -p tldrify-test -f docker-compose-test.yml rm
}

trap cleanup EXIT

exec docker-compose -p tldrify-test -f docker-compose-test.yml up \
  --force-recreate --build --abort-on-container-exit --exit-code-from test

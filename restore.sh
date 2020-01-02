#!/bin/bash -eu

file=$1
container=tldrify-prd_db_1

if ! [[ $file == *.sql ]]; then
  echo "ERROR: restore file must have '.sql' extension"
  exit 1
fi

docker cp $file $container:/tmp
docker exec -ti -e MYSQL_PWD=tldr $container mysql -u tldr tldr -e "source /tmp/$(basename $file)"

#!/bin/bash -eu

cmd=$1
file=$2
ENV=${ENV:-dev}
container=tldrify-${ENV}_db_1

case $cmd in
  backup)
    docker exec -ti -e MYSQL_PWD=tldr $container mysqldump -u tldr tldr 2>/dev/null >$file
    ;;
  restore)
    docker cp $file $container:/tmp
    docker exec -ti -e MYSQL_PWD=tldr $container mysql -u tldr tldr -e "source /tmp/$(basename $file)"
    ;;
  upload)
    gzip $file && ./dropbox-upload.py $file
    ;;
esac

#!/bin/bash -eu

cmd=$1
file=$2
ENV=${ENV:-dev}
container=tldrify-${ENV}_db_1

case $cmd in
  backup)
    docker exec -ti $container mysqldump -u tldr tldr 2>/dev/null >$file
    ;;
  upload)
    gzip $file && ./dropbox-upload.py $file
    ;;
esac

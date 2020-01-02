#!/bin/bash -eu

file=/tmp/tldr-mysql.sql.gz
container=tldrify-prd_db_1

docker exec -ti -e MYSQL_PWD=tldr $container mysqldump -u tldr tldr 2>/dev/null | gzip - > $file && ./dropbox-upload.py $file

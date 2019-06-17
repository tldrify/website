#!/bin/sh

tmpfile=/tmp/tldr-mysql.sql.gz
mysqldump -u tldr -ptldr tldr | gzip - > $tmpfile && ./dropbox-upload.py $tmpfile
s=$?
rm -f $tmpfile
exit $s


#!/bin/sh -eu

run_wsgi()
{
  sleep 5
  retries=60
  while ! ./init-db.py; do
    echo "Waiting before initializing DB..."
    sleep 5
    retries=$(($retries-1))
    if [ $retries -le 0 ]; then
      echo "ERROR: Timeout waiting for the DB"
      exit 1
    fi
  done

  nginx && uwsgi --ini wsgi.ini
}

case $1 in
  mailer)
    ./send-mails.py
    ;;
  report)
    ./daily-report.py
    ;;
  wsgi)
    run_wsgi
    ;;
  *)
    echo "ERROR: unknown mode ($@)"
    exit 1
esac

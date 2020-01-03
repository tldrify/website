#!/bin/sh -eu

# Someone would say: "One Docker container - one job, to schedule things use host cron daemon!"
# But I don't care, base the following works, and less setup is needed :-P

schedule_mailer()
{
  set +e
  echo "Running periodic mail sending job"
  while true; do
    sleep 20
    timeout 10s ./send-mails.py
  done
}

schedule_report()
{
  set +e
  echo "Scheduling periodic daily report"
  last_run=
  while true; do
    sleep 55
    if [ "$(date +"%H%M")" == "0500" ] && [ "$last_run" != "$(date +"%d")" ]; then
      timeout 15s ./daily-report.py
      last_run="$(date +"%d")"
    fi
  done
}

run_wsgi()
{
  sleep 5
  retries=60
  while ! ./init-db.py; do
    echo "Waiting before initializing DB"
    sleep 5
    retries=$(($retries-1))
    if [ $retries -le 0 ]; then
      echo "ERROR: Timeout waiting for the DB"
      exit 1
    fi
  done

  schedule_mailer&
  schedule_report&
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

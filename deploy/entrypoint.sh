#!/bin/sh -eu

# Someone would say: "One Docker container - one job, to schedule things use host cron daemon!"
# But I don't care, base the following works, and less setup is needed :-P

schedule_mailer()
{
  set +e
  echo "[$(date -Is)] Scheduling periodic mail sending job"

  while true; do
    sleep 30
    echo "[$(date -Is)] Sending out e-mails"
    timeout 10s ./send-mails.py
  done
}

schedule_report()
{
  set +e
  echo "[$(date -Is)] Scheduling periodic daily report"

  last_run=
  while true; do
    sleep 55
    if [ "$(date +"%H%M")" == "0500" ] && [ "$last_run" != "$(date +"%d")" ]; then
      echo "[$(date -Is)] Issuing daily report"
      timeout 15s ./daily-report.py
      last_run="$(date +"%d")"
    fi
  done
}

schedule_backups()
{
  set +e
  echo "[$(date -Is)] Scheduling periodic backup"

  backup_file=/tmp/tldrify-sqlite.db
  sleep 60
  while true; do
    echo "[$(date -Is)] Running periodic backup"
    sqlite3 /tmp/sqlite.db ".clone ${backup_file}"
    gzip -f $backup_file
    if [ -z "${DROPBOX_TOKEN}" ]; then
      echo "[$(date -Is)] WARNING: Skipping upload to Dropbox since DROPBOX_TOKEN is undefined"
    else
      ./dropbox-upload.py ${backup_file}.gz
    fi
    sleep 3600
  done
}

run_wsgi()
{
  retries=60
  while ! ./init-db.py; do
    echo "[$(date -Is)] Waiting before initializing DB"
    sleep 5
    retries=$(($retries-1))
    if [ $retries -le 0 ]; then
      echo "ERROR: Timeout waiting for the DB"
      exit 1
    fi
  done

  schedule_mailer&
  if [ "${ENV}" == "prd" ]; then
    schedule_report&
    schedule_backups&
  fi
  nginx && exec uwsgi --ini wsgi.ini
}

case $1 in
  wsgi)
    run_wsgi
    ;;
  *)
    echo "ERROR: unknown mode ($@)"
    exit 1
esac

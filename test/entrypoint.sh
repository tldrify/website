#!/bin/sh -eu

sleep 5
retries=10
while ! curl -fsS http://web:8080 >/dev/null; do
  echo "Web service is not available yet... waiting"
  sleep 5
  retries=$(($retries - 1))
  if [ $retries -le 0 ]; then
    echo "ERROR: Timeout waiting for the Web service"
    exit 1
  fi
done

echo "Creating a citation"
curl -fsS "http://web:8080/api/create.js?url=http%3A%2F%2Flocalhost%3A8080%2F&data=%5B%7B%22start%22%3A%7B%22xpaths%22%3A%5B%22%2F%2Fdd%5B2%5D%2Fp%22%5D%2C%22offset%22%3A0%2C%22checksum%22%3A%228d409d88%22%2C%22nodeIndex%22%3A0%2C%22text%22%3A%22Go%20to%20the%20Website%20th%22%7D%2C%22end%22%3A%7B%22xpaths%22%3A%5B%22%2F%2Fdd%5B2%5D%2Fp%22%5D%2C%22offset%22%3A54%2C%22checksum%22%3A%228d409d88%22%2C%22nodeIndex%22%3A0%2C%22text%22%3A%22Go%20to%20the%20Website%20th%22%7D%7D%5D&_=1577990860829" >/dev/null

echo "Opening shortened URI"
curl -fsS "http://web:8080/rt" >/dev/null

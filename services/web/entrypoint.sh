#!/bin/sh
while true; do
    flask db upgrade
    if [ "$?" = "0" ]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
flask translate compile

sleep 20

curl http://scrapyd:6800/schedule.json -d project=scraping -d spider=forecast

cron -f &
exec "$@"

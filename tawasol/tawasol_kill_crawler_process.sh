#!/usr/bin/env bash

kill $(ps aux | grep tawasol_twitter_crawler.py | awk '{print $2}')
now=$(date+"%T")
echo "tawasol_twitter_crawler process is killed at: $now"
/export/sc-urbcomp/apps/tawasol/tawasol/venv_prod/bin/python /export/sc-urbcomp/apps/tawasol/tawasol/tawasol_twitter_crawler.py &
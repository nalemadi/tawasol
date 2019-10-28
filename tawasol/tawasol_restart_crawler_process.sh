#!/usr/bin/env bash

kill $(ps aux | grep tawasol_twitter_crawler.py | awk '{print $2}' | xargs kill -9)
now=$(date+"%T")
echo "tawasol_twitter_crawler process is killed at: $now"
cd [REDACTED_FPATH]tawasol/
venv_prod2/bin/python tawasol_twitter_crawler.py &
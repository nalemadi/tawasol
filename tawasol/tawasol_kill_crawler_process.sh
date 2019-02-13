#!/usr/bin/env bash

kill $(ps aux | grep tawasol_twitter_crawler.py | awk '{print $2}')
/export/sc-urbcomp/apps/tawasol/tawasol/venv_prod/bin/python /export/sc-urbcomp/apps/tawasol/tawasol/tawasol_twitter_crawler.py &
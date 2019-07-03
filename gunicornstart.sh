#!/bin/bash

# Prepare log files and start outputting logs to stdout
mkdir -p srv/bot_api/logs
touch srv/bot_api/logs/gunicorn.log
touch srv/bot_api/logs/gunicorn-access.log
tail -n 0 -f srv/bot_api/logs/gunicorn*.log &

# export DJANGO_SETTINGS_MODULE=django_docker_azure.settings
export NLTK_DATA=/srv/bot_api/nltk_data/

exec gunicorn app:app \
    --bind 0.0.0.0:8080 \
    --workers 5 \
    --log-level=info \
    --log-file=srv/bot_api/logs/gunicorn.log \
    --access-logfile=srv/bot_api/logs/gunicorn-access.log \
"$@"
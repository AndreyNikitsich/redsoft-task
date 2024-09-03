#!/bin/bash
set -e
set -x

python $BASE_PATH/app/manage.py migrate &
MIGRATION_PID=$!

wait $MIGRATION_PID

# use exec to handle SIGINT to speed up the container shutdown process
if [ "$ENVIRONMENT" = "PROD" ]; then
    # need install gcc for uwsgi in dockerfile
    exec uwsgi --strict --ini "$BASE_PATH"/uwsgi.ini
elif [ "$ENVIRONMENT" = "LOCAL" ]; then
    exec python $BASE_PATH/app/manage.py runserver 0.0.0.0:${APP_PORT}
else
    echo You are required to specify the ENVIRONMENT
fi

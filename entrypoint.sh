#!/bin/bash
if [ "$DATABASE" = "mssql" ]
then
    echo "======= Waiting for MSSQL======="

    while ! nc -z $MSSQL_HOST $MSSQL_PORT; do
      sleep 0.1
    done
    echo "======= MSSQL SERVER STARTED ========"
fi

python3 manage.py flush --no-input
python3 manage.py migrate
exec "$@"
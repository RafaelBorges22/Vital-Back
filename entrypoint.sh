#!/bin/sh
set -x  
python3 -c "import flask_migrate"

echo "Waiting for database..."
sleep 10

export FLASK_APP=src.main:app

until /usr/local/bin/python3 -m flask db upgrade 2>&1
do
  echo "Database migration failed. Retrying in 5 seconds..."
  sleep 5
done

echo "Migration successful. Starting application..."

exec "$@"
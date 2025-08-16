#!/bin/sh

export FLASK_APP=src.main:app

echo "Waiting for database..."
sleep 10

until /usr/local/bin/python3 -m flask db upgrade
do
  echo "Database migration failed. Retrying in 5 seconds..."
  sleep 5
done

echo "Migration successful. Starting application..."
exec "$@"
#!/usr/bin/env bash

wait_for_db() {
  if [ -z "$POSTGRES_HOST" ]; then
    echo "No Django database host, not waiting for db."
  else
    echo "Waiting for database"
    dockerize -wait tcp://"$POSTGRES_HOST":5432 -timeout 30s
  fi
}

if [ "$1" == "runserver" ]; then
  exec gunicorn yoyoproject.wsgi:application --bind "${@:2}"
fi

if [ "$1" == "init" ]; then
  wait_for_db
  python manage.py migrate
  python manage.py collectstatic
  python manage.py cities_light --progress
  python manage.py createsuperuser --username $DJANGO_SUPERUSER_NAME --email $DJANGO_SUPERUSER_EMAIL --password $DJANGO_SUPERUSER_PASSWORD
fi

if [ "$1" == "update" ]; then
  wait_for_db
  python manage.py migrate
  python manage.py collectstatic --noinput
fi

exec "$@"

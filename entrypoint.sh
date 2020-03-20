#!/usr/bin/env bash

create_superuser="
import configurations; configurations.setup()
import django; django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    User.objects.create_superuser('$DJANGO_SUPERUSER_NAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
except Exception:
    pass
"

create_superuser() {
  if [ -z "$DJANGO_SUPERUSER_NAME" ] || [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Environment variables for datatabase not set, not creating superuser."
  else
    echo "Creating superuser"
    python -c "$create_superuser"
  fi
}

wait_for_db() {
  if [ -z "$POSTGRES_HOST" ]; then
    echo "No Django database host, not waiting for db."
  else
    echo "Waiting for database"
    dockerize -wait tcp://"$POSTGRES_HOST":5432 -timeout 30s
  fi
}

if [ "$1" == "runserver" ]; then
  wait_for_db

  echo "Running migrations",
  # Apply database migrations
  python manage.py migrate
  # Collect static files
  echo "Running collectstatic"
  python manage.py collectstatic --noinput

  create_superuser

  exec gunicorn yoyoproject.wsgi:application --bind "${@:2}"
fi

if [ "$1" == "nomigrate" ]; then
  wait_for_db

  echo "Running collectstatic"
  python manage.py collectstatic --noinput

  create_superuser

  exec gunicorn yoyoproject.wsgi:application --bind "${@:2}"
fi

if [ "$1" == "migrate" ]; then
    wait_for_db

    echo "Running migrations"
    # Apply database migrations
    python manage.py "$@"
fi

if [ "$1" == "makemigrations" ];then
    wait_for_db
    exec python manage.py "$@"
fi

if [ "$1" == "loadtestdata" ];then
    wait_for_db
    exec python manage.py "$@"
fi

exec "$@"

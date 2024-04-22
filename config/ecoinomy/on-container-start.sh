#!/usr/bin/env bash

# Create migrations based on django models
# python manage.py makemigrations

# Migrate created migrations to database
# python manage.py migrate

python manage.py collectstatic --noinput &&\

# Start gunicorn server at port 8000 and keep an eye for app code changes
# If changes occur, kill worker and start a new one
# gunicorn --reload medical_advice.wsgi:application --timeout 120 -b 0.0.0.0:8000
uvicorn --host 0.0.0.0 --port 8000 --reload --proxy-headers ecoinomy.asgi:application
#!/bin/sh
chmod a+x static/
python manage.py collectstatic --noinput
python manage.py migrate

#run server
gunicorn project.wsgi:application --bind 0.0.0.0:8000
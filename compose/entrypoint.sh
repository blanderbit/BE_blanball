#!/bin/bash -x
cd project

Backend()
{
    python manage.py collectstatic --noinput
    python manage.py makemigrations 
    python manage.py migrate
    uwsgi --ini uwsgi.ini
}

Daphne()
{
    daphne -u project.asgi:application --port 8000 --bind 0.0.0.0 -v2
}

CeleryWorker()
{
    celery -A project worker --loglevel=INFO --concurrency=8 -O fair -P prefork -n cel_app_worker
}


CeleryBeat()
{
    celery -A project beat -l info 
}


case $1
in
    api-start) Backend ;;
    celery-worker-start) CeleryWorker ;;
    celery-beat-start) CeleryBeat ;;
    daphne-start) Daphne;;
    *) exit 1 ;;
esac
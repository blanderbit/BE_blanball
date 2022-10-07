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
    rm -f /usr/src/blanball/daphne.sock
    rm -f /usr/src/blanball/daphne.sock.lock
    daphne -u /usr/src/blanball/daphne.sock --proxy-headers project.asgi:application
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
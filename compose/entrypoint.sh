#!/bin/bash -x
cd project

BackendDeploy()
{
    python manage.py migrate
    uwsgi --ini uwsgi.ini
}

Backend()
{
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic --noinput
    python manage.py runserver 0.0.0.0:8000
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
    api) Backend ;;
    api-deploy) BackendDeploy;;
    celery-worker) CeleryWorker ;;
    celery-beat) CeleryBeat ;;
    daphne) Daphne;;
    *) exit 1 ;;
esac
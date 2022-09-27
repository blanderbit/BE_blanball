cd project
celery -A project worker --loglevel=INFO --concurrency=8 -O fair -P prefork -n cel_app_worker

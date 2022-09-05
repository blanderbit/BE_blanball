sudo docker rm api db redis celery-beat celery-worker
sudo docker image rmi be_blanball_celery-beat be_blanball_celery-worker be_blanball_api postgres python
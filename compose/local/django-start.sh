python3 project/manage.py collectstatic --noinput
python3 project/manage.py makemigrations 
python3 project/manage.py migrate
python3 project/manage.py test
python3 project/manage.py runserver 0.0.0.0:8000

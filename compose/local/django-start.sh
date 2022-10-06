cd project
python manage.py collectstatic --noinput
python manage.py makemigrations 
python manage.py migrate
# python manage.py test
# gunicorn project.wsgi:application --bind 0.0.0.0:8000
python3 manage.py runserver 0.0.0.0:8000
# uwsgi --ini uwsgi.ini
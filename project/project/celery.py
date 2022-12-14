import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings',namespace ='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'delete_expire_codes': {
        'task':'authentication.tasks.delete_expire_codes',
        'schedule': crontab(minute ='*/10')
    },
    'delete_uproved_requests_to_participation': {
        'task':'events.tasks.delete_uproved_requests_to_participation',
        'schedule': crontab(minute ='*/20')
    },
    'check_event_start_time': {
        'task':'events.tasks.check_event_start_time',
        'schedule': crontab(minute ='*/1')
    },
    'check_user_age': {
        'task':'authentication.tasks.check_user_age',
        'schedule': crontab(minute=0, hour=0)
    },
}

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings',namespace ='CELERY')
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'delete-expire-codes': {
        'task':'authentication.tasks.delete_expire_codes',
        'schedule': crontab(minute ='*/10')
    },
    'check_event_start_time': {
        'task':'notifications.tasks.check_event_start_time',
        'schedule': crontab(minute ='*/1')
    }
}
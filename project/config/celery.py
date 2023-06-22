import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery = Celery("config")

celery.config_from_object("django.conf:settings", namespace="CELERY")
celery.autodiscover_tasks()

celery.conf.beat_schedule = {
    "delete_expire_codes": {
        "task": "authentication.tasks.delete_expire_codes",
        "schedule": crontab(minute="*/10"),
    },
    "check_event_start_time": {
        "task": "events.tasks.check_event_start_time",
        "schedule": crontab(minute="*/1"),
    },
    "check_user_age": {
        "task": "authentication.tasks.check_user_age",
        "schedule": crontab(minute=0, hour=0),
    },
    "delete_expire_notifications": {
        "task": "notifications.tasks.delete_expire_notifications",
        "schedule": crontab(minute=0, hour=0),
    },
    "delete_expired_api_keys": {
        "task": "api_keys.tasks.delete_expired_api_keys",
        "schedule": crontab(minute=0, hour=0),
    },
    "reset_outstanding_jwt_tokens": {
        "task": "config.tasks.reset_outstanding_jwt_tokens",
        "schedule": crontab(minute=0, hour=0),
    },
    "remove_expired_invitations_to_friends": {
        "task": "friends.tasks.remove_expired_invitations_to_friends",
        "schedule": crontab(hour="*/8"),
    },
}

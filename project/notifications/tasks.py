from channels.db import database_sync_to_async
from notifications.models import Notification
from project.celery import app

@database_sync_to_async
# @app.task
def create_notification(user,text):
    Notification.objects.create(user = user,text = text)
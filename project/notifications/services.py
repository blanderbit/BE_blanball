import json
from tkinter.messagebox import NO
from authentication.models import User
from typing import Any
from django.db.models.query import QuerySet
from notifications.tasks import send_to_user

from notifications.constaints import (CHANGE_MAINTENANCE_MESSAGE_TYPE, MAINTENANCE_FALSE_NOTIFICATION_TEXT, 
MAINTENANCE_TRUE_NOTIFICATION_TEXT)

from notifications.models import Notification

def update_maintenance(data: dict[str, str]) -> None:

    with open('./project/config.json', 'r') as f:
        json_data = json.load(f)
        json_data['isMaintenance'] = data['isMaintenance']

    with open('./project/config.json', 'w') as f:
        f.write(json.dumps(json_data))

        for user in User.objects.all():
            if json_data['isMaintenance'] == True:
                notification_text = MAINTENANCE_TRUE_NOTIFICATION_TEXT.format(
                username = user.profile.name)
            else:
                notification_text = MAINTENANCE_FALSE_NOTIFICATION_TEXT.format(
                username = user.profile.name)
            send_to_user(user = user, notification_text = notification_text, 
                message_type = CHANGE_MAINTENANCE_MESSAGE_TYPE)

def bulk_delete_notifications(data: dict[str, Any], queryset: QuerySet, user: User) -> dict[str, int]:
    deleted: list[int] = [] 
    for notification in data:
        try:
            notify = queryset.get(id = notification)
            if notify.user == user:
                notify.delete()
                deleted.append(notification)
        except Notification.DoesNotExist:
            pass
    return {'delete success': deleted}

def bulk_read_notifications(data: dict[str, Any], queryset: QuerySet) -> dict[str, int]:
    success: list[int] = [] 
    for notification in data:
        try: 
            notify = queryset.get(id = notification)
            if notify.type != 'Read':
                notify.type = 'Read'
                notify.save()
                success.append(notification)
        except Notification.DoesNotExist:
            pass
    return {'read success': success}
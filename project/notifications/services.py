import json
from authentication.models import User
from typing import Any
from django.db.models.query import QuerySet
from notifications.tasks import send_to_user

from notifications.constaints import (CHANGE_MAINTENANCE_MESSAGE_TYPE, MAINTENANCE_FALSE_NOTIFICATION_TEXT, 
MAINTENANCE_TRUE_NOTIFICATION_TEXT)

def update_maintenance(data: dict[str, str]) -> None:
    with open('./project/config.json', 'w') as f:
        json.dump(data,f)
        for user in User.objects.all():
            if data["isMaintenance"] == True:
                notification_text = MAINTENANCE_TRUE_NOTIFICATION_TEXT.format(
                username = user.profile.name, last_name = user.profile.last_name)
            else:
                notification_text = MAINTENANCE_FALSE_NOTIFICATION_TEXT.format(
                username = user.profile.name, last_name = user.profile.last_name)
            send_to_user(user = user,notification_text = notification_text, 
                message_type = CHANGE_MAINTENANCE_MESSAGE_TYPE)

def bulk_delete_notifications(data: dict[str, Any], queryset: QuerySet, user: User) -> dict[str, int]:
    deleted: list[int] = [] 
    not_deleted: list[int] = []
    for notification in data:
        notify = queryset.filter(id = notification)
        if notify:
            notify = queryset.get(id = notification)
            if notify.user == user:
                notify.delete()
                deleted.append(notification)
            else:
                not_deleted.append(notification)
        else:
            not_deleted.append(notification)
    return {"delete success": deleted, "delete error":  not_deleted}

def bulk_read_notifications(data: dict[str, Any], queryset: QuerySet) -> dict[str, int]:
    read: list[int] = [] 
    not_read: list[int] = []
    for notification in data:
        notify = queryset.filter(id = notification)
        if notify:
            notify = queryset.get(id = notification)
            if notify.type != 'Read':
                notify.type = 'Read'
                notify.save()
                read.append(notification)
            else:
                not_read.append(notification) 
        else:
            not_read.append(notification)
    return {"read success": read, "read error": not_read}
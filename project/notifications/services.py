import json

from typing import Any, Optional, TypeVar, Generator

from authentication.models import User
from django.db.models.query import QuerySet
from notifications.tasks import send_to_user

from notifications.constaints import (CHANGE_MAINTENANCE_MESSAGE_TYPE, MAINTENANCE_FALSE_NOTIFICATION_TEXT, 
MAINTENANCE_TRUE_NOTIFICATION_TEXT)

from notifications.models import Notification

bulk = TypeVar(Optional[Generator[list[dict[str, int]], None, None]])

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

def bulk_delete_notifications(data: dict[str, Any], queryset: QuerySet[Notification], user: User) -> bulk:
    for notification in data:
        try:
            notify = queryset.get(id = notification)
            if notify.user == user:
                notify.delete()
                yield {'success': notification}
        except Notification.DoesNotExist:
            pass

def bulk_read_notifications(data: dict[str, Any], queryset: QuerySet[Notification]) -> bulk:
    for notification in data:
        try: 
            notify = queryset.get(id = notification)
            if notify.type != 'Read':
                notify.type = 'Read'
                notify.save()
                yield {'success': notification}
        except Notification.DoesNotExist:
            pass
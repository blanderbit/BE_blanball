import json

from typing import Any, Optional, TypeVar, Generator

from authentication.models import User
from django.db.models.query import QuerySet
from notifications.tasks import send_to_user

from notifications.constants import (
    CHANGE_MAINTENANCE_MESSAGE_TYPE,
)

from notifications.models import Notification

bulk = TypeVar(Optional[Generator[list[dict[str, int]], None, None]])

def update_maintenance(data: dict[str, str]) -> None:

    with open('./project/config.json', 'r') as f:
        json_data = json.load(f)
        json_data['isMaintenance'] = data['isMaintenance']

    with open('./project/config.json', 'w') as f:
        f.write(json.dumps(json_data))

        for user in User.get_all():
            send_to_user(user = user, 
                message_type = CHANGE_MAINTENANCE_MESSAGE_TYPE,
                data = {
                    'recipient':{
                        'id': user.id,
                        'name': user.profile.name,
                        'last_name': user.profile.last_name,
                    },
                    'maintenance': {
                        'type': data['isMaintenance'],
                    }
                })

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
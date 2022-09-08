from project.celery import app
from notifications.models import Notification
from authentication.models  import ActiveUser
from authentication.tasks import Util

from django.template.loader import render_to_string

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_to_user(user,notification_text):
    channel_layer = get_channel_layer()
    Notification.objects.create(user=user,notification_text=f'{notification_text}')
    if ActiveUser.objects.filter(user = user.id):
        async_to_sync(channel_layer.group_send)(
            user.group_name,
            {
                'type': 'kafka.message',
                'message': notification_text,
            }
        )
    else:
        # context = ({'code': list(code.value),'name':user.profile.name,'surname':user.profile.last_name})
        template = render_to_string('email_message.html')
        Util.send_email.delay(data = {'email_subject': 'Blanball','email_body': template,
        'to_email': user.email})



def send_notification_to_subscribe_event_user(event,notification_text):
    for user in event.current_users.all():
        send_to_user(user=user,notification_text=notification_text)

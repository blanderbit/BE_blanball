from project.celery import app
from notifications.models import Notification
from authentication.models  import User,ActiveUser
from authentication.tasks import Util
from events.models import Event

from django.template.loader import render_to_string

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_to_user(user:User,notification_text:str,message_type:str) -> None:
    channel_layer = get_channel_layer()
    Notification.objects.create(user=user,notification_text=f'{notification_text}')
    if ActiveUser.objects.filter(user = user.id):
        async_to_sync(channel_layer.group_send)(
            user.group_name,
            {
                'type': 'kafka.message',
                'message': notification_text,
                'message_type': message_type, 
            }
        )
    else:
        if user.configuration['send_email']:
            # context = ({'code': list(code.verify_code),'name':user.profile.name,'surname':user.profile.last_name})
            template = render_to_string('email_message.html')
            Util.send_email.delay(data = {'email_body': template,
            'to_email': user.email})



def send_notification_to_subscribe_event_user(event:Event,notification_text:str,message_type:str) -> None:
    for user in event.current_users.all():
        send_to_user(user=user,notification_text=notification_text,message_type=message_type)
    for fan in event.fans.all():
        send_to_user(user=fan,notification_text=notification_text,message_type=message_type)
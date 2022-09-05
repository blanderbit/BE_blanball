from django.db.models.signals import pre_delete,pre_save
from django.dispatch import receiver
from .models import Event
from notifications.tasks import send_notification_to_subscribe_event_user

@receiver(pre_delete,sender=Event)
def delete_event(sender,instance,*args,**kwargs):
    send_notification_to_subscribe_event_user(event =instance,notification_text='event_deleted')

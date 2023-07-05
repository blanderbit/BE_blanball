from django.db.models.signals import (
    post_save,
)
from django.dispatch import receiver
from events.models import (
    Event,
)
from notifications.models import Notification



@receiver(post_save, sender=Event)
def delete_all_event_relations_after_finished(
    sender: Event, instance: Event, **kwargs
) -> None:
    if instance.status == instance.Status.FINISHED:
        instance.invites.all().delete()
        for notification in Notification.get_all().filter(data__event__id=instance.id):
            notification.data["event"].update({"finished": True})
            notification.save()
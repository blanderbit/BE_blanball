from django.db import models
from authentication.models import User


class Notification(models.Model):
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"(Event{self.user} {self.event})"
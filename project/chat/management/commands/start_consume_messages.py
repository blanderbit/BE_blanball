from threading import Thread

from chat.helpers.default_consumer import (
    default_consumer,
)
from django.core.management.base import (
    BaseCommand,
)


class Command(BaseCommand):
    help = "Consume Kafka messages"

    def handle(self, *args, **options):
        thread = Thread(target=default_consumer)
        thread.start()

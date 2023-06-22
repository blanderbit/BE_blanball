import multiprocessing

from chat.tasks import ALL_CONSUMER_TASKS
from django.core.management.base import (
    BaseCommand,
)


class Command(BaseCommand):
    help = "Consume Kafka messages"

    def handle(self, *args, **options):
        processes = []

        for task in ALL_CONSUMER_TASKS:
            process = multiprocessing.Process(target=task)
            processes.append(process)

        # Start all the consumer processes
        for process in processes:
            process.start()

        # Wait for all the consumer processes to finish
        for process in processes:
            process.join()

        self.stdout.write(
            self.style.SUCCESS(
                "Message consumption via kafka broker started successfully for all tasks"
            )
        )

from time import sleep

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import (
    BaseCommand,
)
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable


class Command(BaseCommand):
    help = "Consume Kafka messages"

    def handle(self, *args, **options):
        self.connected = False

        while not self.connected:
            try:
                consumer = KafkaConsumer(**settings.KAFKA_CONSUMER_CONFIG)
                self.connected = True
                consumer.close()
                self.on_connection_success(
                    settings.KAFKA_CONSUMER_CONFIG["bootstrap_servers"]
                )
                break
            except NoBrokersAvailable:
                self.on_connection_error()

    def on_connection_error(self) -> None:
        self.stdout.write(
            self.style.ERROR(
                "No active Kafka brokers available. Trying to reconnect..."
            )
        )
        sleep(5)

    def on_connection_success(self, broker_address: str) -> None:
        self.stdout.write(
            self.style.SUCCESS(
                f"Connected to Kafka broker successfully. Broker address - {broker_address}"
            )
        )
        call_command("start_consume_messages")

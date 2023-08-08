import json
from typing import Any
from decouple import config
from django.utils.translation import (
    gettext_lazy as _,
)

USE_KAFKA: bool = config("USE_KAFKA", default=False)

if USE_KAFKA:
    KAFKA_PRODUCER_CONFIG: dict[str, Any] = {
        "bootstrap_servers": [config("KAFKA_PRODUCER_ADRESS", cast=str)],
        "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
    }

    KAFKA_ADMIN_CONFIG: dict[str, Any] = {
        "bootstrap_servers": [config("KAFKA_CONSUMER_ADRESS", cast=str)],
    }

    KAFKA_CONSUMER_CONFIG: dict[str, Any] = {
        "bootstrap_servers": [config("KAFKA_CONSUMER_ADRESS", cast=str)],
        "value_deserializer": lambda v: json.loads(v.decode("utf-8")),
        "enable_auto_commit": True,
    }

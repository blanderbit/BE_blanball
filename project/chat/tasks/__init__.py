from chat.tasks.create_chat import (
    create_chat_producer as create_chat_producer,
    create_chat_response_consumer as create_chat_response_consumer
)
from chat.tasks.create_message import (
    create_message_producer as create_message_producer,
    create_message_response_consumer as create_message_response_consumer
)


ALL_CONSUMER_TASKS = [
    create_chat_response_consumer,
    create_message_response_consumer,
]
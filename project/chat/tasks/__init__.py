from chat.tasks.create_chat import (
    create_chat_producer as create_chat_producer,
    create_chat_response_consumer as create_chat_response_consumer
)


ALL_CONSUMER_TASKS = [
    create_chat_response_consumer
]
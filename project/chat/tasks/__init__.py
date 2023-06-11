from chat.tasks.add_user_to_chat import (
    add_user_to_chat_producer as add_user_to_chat_producer,
)
from chat.tasks.add_user_to_chat import (
    add_user_to_chat_response_consumer as add_user_to_chat_response_consumer,
)
from chat.tasks.create_chat import (
    create_chat_producer as create_chat_producer,
)
from chat.tasks.create_chat import (
    create_chat_response_consumer as create_chat_response_consumer,
)
from chat.tasks.create_message import (
    create_message_producer as create_message_producer,
)
from chat.tasks.create_message import (
    create_message_response_consumer as create_message_response_consumer,
)
from chat.tasks.delete_chat import (
    delete_chat_producer as delete_chat_producer,
)
from chat.tasks.delete_chat import (
    delete_chat_response_consumer as delete_chat_response_consumer,
)
from chat.tasks.disable_chat import (
    disable_chat_producer as disable_chat_producer,
)
from chat.tasks.disable_chat import (
    disable_chat_response_consumer as disable_chat_response_consumer,
)
from chat.tasks.edit_chat import (
    edit_chat_producer as edit_chat_producer,
)
from chat.tasks.edit_chat import (
    edit_chat_response_consumer as edit_chat_response_consumer,
)
from chat.tasks.remove_user_from_chat import (
    remove_user_from_chat_producer as remove_user_from_chat_producer,
)
from chat.tasks.remove_user_from_chat import (
    remove_user_from_chat_response_consumer as remove_user_from_chat_response_consumer,
)
from chat.tasks.get_chats_list import (
    get_chats_list_producer as get_chats_list_producer
)
from chat.tasks.get_chats_list import (
    get_chats_list_response_consumer as get_chats_list_response_consumer
)

ALL_CONSUMER_TASKS = [
    create_chat_response_consumer,
    create_message_response_consumer,
    add_user_to_chat_response_consumer,
    remove_user_from_chat_response_consumer,
    delete_chat_response_consumer,
    disable_chat_response_consumer,
    edit_chat_response_consumer,
    get_chats_list_response_consumer,
]

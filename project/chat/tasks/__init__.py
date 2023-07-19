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
from chat.tasks.edit_message import (
    edit_message_producer as edit_message_producer
)
from chat.tasks.edit_message import (
    edit_message_response_consumer as edit_message_response_consumer
)
from chat.tasks.get_chat_messages_list import (
    get_chat_messages_list_producer as get_chat_messages_list_producer
)
from chat.tasks.get_chat_messages_list import (
    get_chat_messages_list_response_consumer as get_chat_messages_list_response_consumer
)
from chat.tasks.read_or_unread_messages import (
    read_or_unread_messages_producer as read_or_unread_messages_producer
)
from chat.tasks.read_or_unread_messages import (
    read_or_unread_messages_response_consumer as read_or_unread_messages_response_consumer
)
from chat.tasks.delete_messages import (
    delete_messages_producer as delete_messages_producer
)
from chat.tasks.delete_messages import (
    delete_messages_response_consumer as delete_messages_response_consumer
)
from chat.tasks.get_chat_users_list import (
    get_chat_users_list_producer as get_chat_users_list_producer
)
from chat.tasks.get_chat_users_list import (
    get_chat_users_list_response_consumer as get_chat_users_list_response_consumer
)
from chat.tasks.set_or_unset_chat_admin import (
    set_or_unset_chat_admin_producer as set_or_unset_chat_admin_producer
)
from chat.tasks.set_or_unset_chat_admin import (
    set_or_unset_chat_admin_response_consumer as set_or_unset_chat_admin_response_consumer
)
from chat.tasks.get_user_info_in_chat import (
    get_user_info_in_chat_producer as get_user_info_in_chat_producer
)
from chat.tasks.get_user_info_in_chat import (
    get_user_info_in_chat_response_consumer as get_user_info_in_chat_response_consumer
)
from chat.tasks.off_or_on_push_notifications import (
    off_or_on_push_notifications_response_consumer as off_or_on_push_notifications_response_consumer
)
from chat.tasks.off_or_on_push_notifications import (
    off_or_on_push_notifications_producer as off_or_on_push_notifications_producer
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
    edit_message_response_consumer,
    get_chat_messages_list_response_consumer,
    read_or_unread_messages_response_consumer,
    delete_messages_response_consumer,
    get_chat_users_list_response_consumer,
    set_or_unset_chat_admin_response_consumer,
    get_user_info_in_chat_response_consumer,
    off_or_on_push_notifications_response_consumer,
]

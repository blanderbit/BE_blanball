from chat.filters import CHATS_LIST_SEARCH_FIELDS
from config.openapi import (
    concat_search_fields,
    offset_query,
)
from drf_yasg import openapi

chats_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description=f"EN - This option allows you to filter \
        the list of chats by fields such as:\
        \n{concat_search_fields(CHATS_LIST_SEARCH_FIELDS)}\
    \n \
    \n RU - Эта опция позволяет фильтровать \
    список чатов по полям:\
    \n{concat_search_fields(CHATS_LIST_SEARCH_FIELDS)}",
    type=openapi.TYPE_STRING,
)

chats_list_query_params: list[openapi.Parameter] = [
    chats_searh_query,
    offset_query,
]

from config.openapi import (
    concat_search_fields,
    offset_query,
    skip_param_query,
)
from drf_yasg import openapi
from friends.filters import MY_FRIENDS_LIST_SEARCH_FIELDS

friend_is_online_query = openapi.Parameter(
    "user__is_online",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        friends by is_online by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список друзей \
        по выбору онлайна",
    type=openapi.TYPE_BOOLEAN,
)

friends_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description=f"EN - This option allows you to filter \
        the list of friends by fields such as:\
        \n{concat_search_fields(MY_FRIENDS_LIST_SEARCH_FIELDS)}\
    \n \
    \n RU - Эта опция позволяет фильтровать \
    список друзей по полям:\
    \n{concat_search_fields(MY_FRIENDS_LIST_SEARCH_FIELDS)}",
    type=openapi.TYPE_STRING,
)

my_friends_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    offset_query,
    friends_searh_query,
    friend_is_online_query,
]

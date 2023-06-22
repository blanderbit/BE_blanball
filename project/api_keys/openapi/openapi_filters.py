from api_keys.filters import (
    API_KEYS_LIST_ORDERING_FIELDS,
    API_KEYS_LIST_SEARCH_FIELDS,
)
from config.openapi import (
    concat_search_fields,
    skip_param_query,
)
from drf_yasg import openapi

api_keys_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description=f"EN - This option allows you to filter \
        the list of api keys by fields such as:\
        \n{concat_search_fields(API_KEYS_LIST_SEARCH_FIELDS)}\
    \n \
    \n RU - Эта опция позволяет фильтровать \
    список апи ключей по полям:\
    \n{concat_search_fields(API_KEYS_LIST_SEARCH_FIELDS)}",
    type=openapi.TYPE_STRING,
)
api_keys_ordering_query = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="EN - This option allows you to sort the list of \
        api keys\
        \n \
        \n RU - Эта опция позволяет вам сортировать список \
        апи ключей",
    enum=[k for k in API_KEYS_LIST_ORDERING_FIELDS],
    type=openapi.TYPE_STRING,
)

api_keys_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    api_keys_searh_query,
    api_keys_ordering_query,
]

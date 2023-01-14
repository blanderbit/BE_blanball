from bugs.filters import (
    BUGS_LIST_ORDERING_FIELDS,
    BUGS_LIST_SEARCH_FIELDS,
)
from bugs.models import Bug
from config.openapi import (
    concat_search_fields,
    skip_param_query,
)
from drf_yasg import openapi

bugs_type_query = openapi.Parameter(
    "type",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
        bugs by type by selection. \
    \n \
    \n RU - Эта опция позволяет фильтровать список \
        ошибки по выбору типа.",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Bug.Type.choices],
)
bugs_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description=f"EN - This option allows you to filter \
        the list of bugs by fields such as:\
    \n{concat_search_fields(BUGS_LIST_SEARCH_FIELDS)}\
    \n \
    \n RU - Эта опция позволяет фильтровать \
        список багов по таким полям как полям:\
    \n{concat_search_fields(BUGS_LIST_SEARCH_FIELDS)}",
    type=openapi.TYPE_STRING,
)
bugs_ordering_query = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="EN - This option allows you to sort the list of \
        bugs\
    \n \
    \n RU - Эта опция позволяет вам сортировать список \
        ошибок",
    enum=[k for k in BUGS_LIST_ORDERING_FIELDS],
    type=openapi.TYPE_STRING,
)
bugs_time_created_min_query = openapi.Parameter(
    "time_created_min",
    openapi.IN_QUERY,
    description="EN - This parameter allows the user to filter \
        the list of users by specifying a minimum time created value.\
    \n \
    \nRU - Этот параметр позволяет пользователю фильтровать \
        список пользователей, указав минимальное значение даты создания.",
    type=openapi.TYPE_STRING,
)
bugs_time_created_max_query = openapi.Parameter(
    "time_created_max",
    openapi.IN_QUERY,
    description="EN - This parameter allows the user to filter \
        the list of bugs by specifying a maximum time created value. \
    \n \
    \nRU - Этот параметр позволяет пользователю фильтровать \
        список багов, указав максимальное значение даты создания.",
    type=openapi.TYPE_STRING,
)

bugs_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    bugs_searh_query,
    bugs_type_query,
    bugs_ordering_query,
    bugs_time_created_min_query,
    bugs_time_created_max_query,
]

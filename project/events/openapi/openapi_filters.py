from authentication.models import Gender
from config.openapi import (
    concat_search_fields,
    distance_query,
    offset_query,
    point_query,
    skip_param_query,
)
from drf_yasg import openapi
from events.filters import (
    EVENTS_LIST_ORDERING_FIELDS,
    EVENTS_LIST_SEARCH_FIELDS,
    EVENTS_RELEVANT_LIST_SEARCH_FIELDS,
)
from events.models import Event

events_type_query = openapi.Parameter(
    "type",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
    events by type by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список \
    событий по выбору типа.",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Event.Type.choices],
)
events_gender_query = openapi.Parameter(
    "gender",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
    events by gender by selection.\
    events by type by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список \
    событий по выбору гендера.",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Gender.choices],
)
events_status_query = openapi.Parameter(
    "status",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
        events by status by selection. \
    \n \
    \n RU - Эта опция позволяет фильтровать список \
    событий по выбору статуса.",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Event.Status.choices],
)
events_duration_query = openapi.Parameter(
    "duration",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
        events by duration by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список \
    событий по выбору длительности.",
    type=openapi.TYPE_INTEGER,
    enum=[k for k, _ in Event.Duration.choices],
)
events_need_ball_query = openapi.Parameter(
    "need_ball",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
        events by need_ball by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список \
    событий по выбору нужен ли мяч.",
    type=openapi.TYPE_BOOLEAN,
)
events_relevant_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description=f"EN - This option allows you to filter the list of \
        events to get the most relevant entries for your query. \
        \nRecords are filtered by the fields: \
        {concat_search_fields(EVENTS_RELEVANT_LIST_SEARCH_FIELDS)} \
        \n \
        \n RU - Эта опция позволяет фильтровать список \
        события, чтобы получить наиболее релевантные записи для вашего запроса. \
        \nЗаписи фильтруются по полям: \
        {concat_search_fields(EVENTS_RELEVANT_LIST_SEARCH_FIELDS)}",
    type=openapi.TYPE_STRING,
)
events_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description=f"EN - This option allows you to filter \
        the list of events by fields such as:\
        \n{concat_search_fields(EVENTS_LIST_SEARCH_FIELDS)}\
    \n \
    \n RU - Эта опция позволяет фильтровать \
    список событий по полям:\
    \n{concat_search_fields(EVENTS_LIST_SEARCH_FIELDS)}",
    type=openapi.TYPE_STRING,
)
events_ordering_query = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="EN - This option allows you to sort the list of \
        events\
        \n \
        \n RU - Эта опция позволяет вам сортировать список \
        событий",
    enum=[k for k in EVENTS_LIST_ORDERING_FIELDS],
    type=openapi.TYPE_STRING,
)
event_date_and_time_before_query = openapi.Parameter(
    "date_and_time_before",
    openapi.IN_QUERY,
    description="EN - This option allows the user \
        to filter the list of events by limiting it to \
        the maximum date.\
        \ndate format = yyyy-mm-dd \
    \n \
    \nRU - Эта опция позволяет пользователю \
        отфильтровать список событий, ограничив его \
        максимальной дата.\
        \nформат даты = гггг-мм-дд",
    type=openapi.TYPE_STRING,
)
event_date_and_time_after_query = openapi.Parameter(
    "date_and_time_after",
    openapi.IN_QUERY,
    description="EN - This option allows the user \
        to filter the list of events by limiting it to \
        the minimum date.\
        \ndate format = yyyy-mm-dd\
    \n \
    \nRU - Эта опция позволяет пользователю \
        чтобы отфильтровать список событий, ограничив его до \
        минимальная датe.\
        \nформат даты = гггг-мм-дд",
    type=openapi.TYPE_STRING,
)

events_list_query_params: list[openapi.Parameter] = [
    event_date_and_time_before_query,
    event_date_and_time_after_query,
    skip_param_query,
    point_query,
    events_type_query,
    events_status_query,
    events_gender_query,
    events_duration_query,
    events_need_ball_query,
    events_searh_query,
    events_ordering_query,
    distance_query,
    offset_query,
]
events_relevant_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    events_relevant_searh_query,
]

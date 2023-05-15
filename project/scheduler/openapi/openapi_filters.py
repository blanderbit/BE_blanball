from config.openapi import (
    offset_query,
    skip_param_query,
)
from drf_yasg import openapi

scheduled_events_user_id_query = openapi.Parameter(
    "user_id",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
    events by type by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список \
    событий по выбору типа.",
    type=openapi.TYPE_STRING,
)

scheduled_events_date_query = openapi.Parameter(
    "date",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
    events by type by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список \
    событий по выбору типа.",
    type=openapi.TYPE_STRING,
)

scheduled_events_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    scheduled_events_user_id_query,
    scheduled_events_date_query,
    offset_query,
]
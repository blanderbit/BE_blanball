from config.openapi import (
    distance_query,
    point_query,
    skip_param_query,
)
from drf_yasg import openapi

event_type_query = openapi.Parameter(
    "type",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by type by selection.\
        \nPossible options: Football, Futsal",
    type=openapi.TYPE_STRING,
)
event_gender_query = openapi.Parameter(
    "gender",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by gender by selection.\
        \nPossible options: Man, Woman",
    type=openapi.TYPE_STRING,
)
event_status_query = openapi.Parameter(
    "status",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by status by selection.\
        \nPossible options: Planned, Active, Finished",
    type=openapi.TYPE_STRING,
)
event_duration_query = openapi.Parameter(
    "duration",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by duration by selection.\
        \nPossible options: 10, 20, 30, 40, 50, 60, 70, 80, 90 \
        100, 110, 120, 130, 140, 150, 160, 170, 180",
    type=openapi.TYPE_INTEGER,
)
event_need_ball_query = openapi.Parameter(
    "need_ball",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by need_ball by selection.",
    type=openapi.TYPE_BOOLEAN,
)
event_relevant_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events to get the most relevant entries for your query. \
        \nRecords are filtered by the field 'name'",
    type=openapi.TYPE_STRING,
)
event_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="This option allows you to filter \
        the list of events by fields such as:\
        \n'id,'name','price','amount_members'",
    type=openapi.TYPE_STRING,
)

events_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    point_query,
    event_type_query,
    event_status_query,
    event_gender_query,
    event_duration_query,
    event_need_ball_query,
    event_searh_query,
    distance_query,
]
events_relevant_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    event_relevant_searh_query,
]

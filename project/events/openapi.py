from authentication.models import Gender
from config.openapi import (
    distance_query,
    point_query,
    skip_param_query,
)
from drf_yasg import openapi
from events.models import Event

events_type_query = openapi.Parameter(
    "type",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by type by selection.",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Event.Type.choices],
)
events_gender_query = openapi.Parameter(
    "gender",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by gender by selection.",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Gender.choices],
)
events_status_query = openapi.Parameter(
    "status",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by status by selection.",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Event.Status.choices],
)
events_duration_query = openapi.Parameter(
    "duration",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by duration by selection.",
    type=openapi.TYPE_INTEGER,
    enum=[k for k, _ in Event.Duration.choices],
)
events_need_ball_query = openapi.Parameter(
    "need_ball",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events by need_ball by selection.",
    type=openapi.TYPE_BOOLEAN,
)
events_relevant_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events to get the most relevant entries for your query. \
        \nRecords are filtered by the field 'name'",
    type=openapi.TYPE_STRING,
)
events_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="This option allows you to filter \
        the list of events by fields such as:\
        \n'id,'name','price','amount_members'",
    type=openapi.TYPE_STRING,
)
events_ordering_query = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="This option allows you to sort the list of \
        events by fields such as: id, -id\
        \nIf you add a minus before the field name, then sorting \
        will be in reverse order.",
    type=openapi.TYPE_STRING,
)
event_date_and_time_before_query = openapi.Parameter(
    "date_and_time_before",
    openapi.IN_QUERY,
    description="This option allows the user \
        to filter the list of events by limiting it to \
        the maximum date.\
        \ndate format = yyyy-mm-dd",
    type=openapi.TYPE_STRING,
)
event_date_and_time_after_query = openapi.Parameter(
    "date_and_time_after",
    openapi.IN_QUERY,
    description="This option allows the user \
        to filter the list of events by limiting it to \
        the minimum date.\
        \ndate format = yyyy-mm-dd",
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
]
events_relevant_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    events_relevant_searh_query,
]

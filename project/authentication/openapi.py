from config.openapi import (
    distance_query,
    point_query,
    skip_param_query,
)
from drf_yasg import openapi

users_relevant_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        events to get the most relevant entries for your query. \
        \nRecords are filtered by the field 'profile__name', 'profile__last_name",
    type=openapi.TYPE_STRING,
)
users_profile__position_query = openapi.Parameter(
    "profile__position",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        users by position by selection.\
        \nPossible options: GK, LB, RB, CB, LWB, RWB, \
        CDM, CM, CAM, RM, LM, RF, CF, LF, ST",
    type=openapi.TYPE_STRING,
)
users_profile__gender_query = openapi.Parameter(
    "profile__gender",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        users by gender by selection.\
        \nPossible options: Man, Woman",
    type=openapi.TYPE_STRING,
)
users_is_online_query = openapi.Parameter(
    "is_online",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        users by is_online by selection.",
    type=openapi.TYPE_BOOLEAN,
)
users_ordering = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="This option allows you to sort the list of \
        users by fields such as: id, profile__age, raiting, \
        -id, -profile__age, -raiting. \
        \nIf you add a minus before the field name, then sorting \
        will be in reverse order.",
    type=openapi.TYPE_STRING,
)

users_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    distance_query,
    point_query,
    users_profile__position_query,
    users_profile__gender_query,
    users_is_online_query,
    users_ordering,
]
users_relevant_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    users_relevant_searh_query,
]

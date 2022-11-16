import json

from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def get_current_version_for_swagger():
    with open("./config/config.json", "r") as f:
        json_data = json.load(f)
        return json_data["version"]


schema_view = get_schema_view(
    openapi.Info(
        title="Blanball",
        default_version=get_current_version_for_swagger(),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "api/v1/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]


skip_param_query = openapi.Parameter(
    "skipids",
    openapi.IN_QUERY,
    description="This parameter makes it possible to delete \
        entries from the beginning of the list by id. \
        \nQuery example: '1, 2, 3, 4, 5' - 5 entries will be \
        removed from the top of the list",
    type=openapi.TYPE_STRING,
)
point_query = openapi.Parameter(
    "point",
    openapi.IN_QUERY,
    description="This option allows you to sort \
        the list in descending order, starting from \
        the entered coordinate value (longitude, latitude).",
    type=openapi.TYPE_STRING,
)
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

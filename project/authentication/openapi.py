from authentication.models import Gender, Profile
from config.openapi import (
    distance_query,
    point_query,
    skip_param_query,
)
from drf_yasg import openapi

users_relevant_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
        events to get the most relevant entries for your query. \
        \nRecords are filtered by the field 'profile__name', 'profile__last_name\
    \n \
    \n RU - Эта опция позволяет фильтровать список \
        события, чтобы получить наиболее релевантные записи для вашего запроса. \
        \nЗаписи фильтруются по полям 'profile__name', 'profile__last_name",
    type=openapi.TYPE_STRING,
)
users_profile__position_query = openapi.Parameter(
    "profile__position",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
        users by position by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список \
        пользователей по выбору иговой позиции",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Profile.Position.choices],
)
users_profile__gender_query = openapi.Parameter(
    "profile__gender",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
        users by gender by selection. \
    \n \
    \n RU - Эта опция позволяет фильтровать список пользователей \
        по выбору гендера",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Gender.choices],
)
users_is_online_query = openapi.Parameter(
    "is_online",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        users by is_online by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список пользователей \
        по выбору онлайна",
    type=openapi.TYPE_BOOLEAN,
)
users_ordering = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="EN - This option allows you to sort the list of \
        users by fields such as: id, profile__age, raiting, \
        -id, -profile__age, -raiting. \
        \nIf you add a minus before the field name, then sorting \
        will be in reverse order.\
    \n \
    \n RU - Эта опция позволяет вам сортировать список \
        пользователей по таким полям как: id, profile__age, raiting, \
        -id, -профиль__возраст, -рейтинг. \
        \nЕсли добавить минус перед именем поля, то сортировка \
        будет в обратном порядке.",
    type=openapi.TYPE_STRING,
)
users_profile_age_min_query = openapi.Parameter(
    "profile__age_min",
    openapi.IN_QUERY,
    description="EN - This parameter allows the user to filter \
        the list of users by specifying a minimum age value.\
    \n \
    \nRU - Этот параметр позволяет пользователю фильтровать \
        список пользователей, указав минимальное значение возраста.",
    type=openapi.TYPE_STRING,
)
users_profile_age_max_query = openapi.Parameter(
    "profile__age_max",
    openapi.IN_QUERY,
    description="EN - This parameter allows the user to filter \
        the list of users by specifying a maximum age value. \
    \n \
    \nRU - Этот параметр позволяет пользователю фильтровать \
        список пользователей, указав максимальное значение возраста.",
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
    users_profile_age_min_query,
    users_profile_age_max_query,
]
users_relevant_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    users_relevant_searh_query,
]

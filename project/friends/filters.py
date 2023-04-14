from typing import Union

from django_filters import (
    rest_framework as filters,
)
from friends.models import (
    Friend
)
MY_FRIENDS_LIST_ORDERING_FIELDS: list[str] = [
    "created_at",
    "-created_at",
]
MY_FRIENDS_LIST_SEARCH_FIELDS: list[str] = [
    "user__profile__name",
]

class MyFriendsListFilterSet(filters.FilterSet):
    user__is_online = filters.BooleanFilter(field_name='user__is_online')

    class Meta:
        model: Friend = Friend
        fields: Union[str, list[str]] = [
            "user__is_online",
        ]
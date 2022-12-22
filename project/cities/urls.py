from typing import Union

from cities.views import (
    GetCoordinatesByPlaceName,
    GetPlaceNameByCoordinates,
    UkraineAreasList,
)
from django.urls import path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path(
        "client/get/coordinates/by/place/name",
        GetCoordinatesByPlaceName.as_view(),
        name="get-coordinates-by-place-name",
    ),
    path(
        "client/get/place/name/by/coordinates",
        GetPlaceNameByCoordinates.as_view(),
        name="get-place-name-by-coordinates",
    ),
    path(
        "client/ukraine/areas/list",
        UkraineAreasList.as_view(),
        name="ukraine-areas-list",
    ),
]

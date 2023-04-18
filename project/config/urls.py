from typing import Union

from config.yasg import urlpatterns as doc_urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.urls.resolvers import (
    URLPattern,
    URLResolver,
)

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path("api/v1/events/", include("events.urls"), name="events"),
    path("api/v1/friends/", include("friends.urls"), name="friends"),
    path(
        "api/v1/authentication/", include("authentication.urls"), name="authentication"
    ),
    path("api/v1/notifications/", include("notifications.urls"), name="notifications"),
    path("api/v1/reviews/", include("reviews.urls"), name="reviews"),
    path("api/v1/cities/", include("cities.urls"), name="cities"),
    path("api/v1/bugs/", include("bugs.urls"), name="bugs"),
    path("api/v1/api_keys/", include("api_keys.urls"), name="api_keys"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += doc_urls

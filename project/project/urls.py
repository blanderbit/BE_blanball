from typing import Union

from project.yasg import urlpatterns as doc_urls

from django.urls import (
    path,
    include,
)
from django.urls.resolvers import (
    URLResolver, 
    URLPattern,
)

from django.conf.urls.static import static
from django.conf import settings

urlpatterns: list[Union[URLResolver, URLPattern]] = [
    path('api/v1/events/', include('events.urls'), 
        name = 'events'),
    path('api/v1/authentication/', include('authentication.urls'), 
        name = 'authentication'),
    path('api/v1/notifications/', include('notifications.urls'), 
        name = 'notifications'),
    path('api/v1/reviews/', include('reviews.urls'), 
        name = 'reviews'),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += doc_urls
from .yasg import urlpatterns as doc_urls

from django.urls import path,include

urlpatterns = [
    path('events/api/v1/', include('events.urls')),
    path('authentication/api/v1/', include('authentication.urls')),
    path('notifications/api/v1/',include('notifications.urls')),
    path('reviews/api/v1/',include('reviews.urls')),
]


urlpatterns += doc_urls
from django.urls import path,include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('events/api/v1/', include('events.urls')),
    path('authentication/api/v1/', include('authentication.urls')),
    path('notifications/api/v1/',include('notifications.urls')),
]


urlpatterns += doc_urls
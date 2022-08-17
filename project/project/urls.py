from django.urls import path,include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('events/api/v1/', include('event.urls')),
    path('authentication/api/v1/', include('authentication.urls')),
]


urlpatterns += doc_urls
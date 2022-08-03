from django.urls import path,include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('events/api/v1/', include('event.urls')),
]


urlpatterns += doc_urls
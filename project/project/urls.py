from django.urls import path,include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('ivents/api/v1/', include('ivents.urls')),
]


urlpatterns += doc_urls
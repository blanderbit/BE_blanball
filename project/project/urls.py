from django.urls import path,include
from .yasg import urlpatterns as doc_urls

urlpatterns = []


urlpatterns += doc_urls
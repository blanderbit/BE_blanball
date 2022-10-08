from project.yasg import urlpatterns as doc_urls
from django.conf.urls.static import serve

from django.urls import path,include
from django.conf.urls.static import static
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/v1/events/', include('events.urls'), 
        name='events'),
    path('api/v1/authentication/', include('authentication.urls'), 
        name='authentication'),
    path('api/v1/notifications/', include('notifications.urls'), 
        name='notifications'),
    path('api/v1/reviews/', include('reviews.urls'), 
        name='reviews'),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += doc_urls
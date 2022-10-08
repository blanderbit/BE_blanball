from project.yasg import urlpatterns as doc_urls

from django.urls import path,include
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
urlpatterns += doc_urls
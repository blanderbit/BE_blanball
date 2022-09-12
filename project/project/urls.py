from .yasg import urlpatterns as doc_urls

from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('events/api/v1/', include('events.urls')),
    path('authentication/api/v1/', include('authentication.urls')),
    path('notifications/api/v1/',include('notifications.urls')),
    path('reviews/api/v1/',include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
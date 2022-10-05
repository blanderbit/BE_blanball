from project.yasg import urlpatterns as doc_urls

from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('events/api/v1/', include('events.urls'), 
        name='events'),
    path('authentication/api/v1/', include('authentication.urls'), 
        name='authentication'),
    path('notifications/api/v1/', include('notifications.urls'), 
        name='notifications'),
    path('reviews/api/v1/', include('reviews.urls'), 
        name='reviews'),
]

if settings.DEBUG:
    # import debug_toolbar

    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ]
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
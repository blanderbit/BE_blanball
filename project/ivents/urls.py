from django.urls import path
from .views import *



urlpatterns = [
    #endpoint where a user with admin
    #role can create a new one ivent 
    path('admin/ivent/create',CreateIvent.as_view(),
        name = 'create-ivent'),
    #endpoint where a user with admin
    #role can get detail info,update and delete ivent 
    path('admin/ivent/<int:pk>',GetPutDeleteIvent.as_view(),
        name = 'ivent-detail'),
    #endpoint where a use can get list of ivents
    path('client/ivent/list',IventList.as_view(),
        name = 'ivent-list'),
    #endpoint where a user with admin
    #role can create a new one ivent type
    path('client/ivents/delete',DeleteIvents.as_view(),
        name = 'ivents-delete'),
]

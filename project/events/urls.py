from django.urls import path
from .views import *



urlpatterns = [
    #endpoint where a user with admin
    #role can create a new one event 
    path('client/event/create',CreateEvent.as_view(),
        name = 'create-event'),
    #endpoint where a user with admin
    #role can get detail info and delete event 
    path('client/event/<int:pk>',GetDeleteEvent.as_view(),
        name = 'event-detail'),
    #endpoint where a user with admin
    #role can get detail info and delete event 
    path('client/event/update/<int:pk>',UpdateEvent.as_view(),
        name = 'event-updatel'),
    #endpoint where a use can get list of events
    path('client/events/list',EventList.as_view(),
        name = 'events-list'),
    #endpoint where a user with admin
    #role can delete events
    path('admin/events/delete',DeleteEvents.as_view(),
        name = 'events-delete'),
    #endpoint where a user can join to event 
    path('client/event/join',JoinToEvent.as_view(),
        name = 'event-join'),
    #endpoint where a fan can join to event 
    path('client/fan/event/join',FanJoinToEvent.as_view(),
        name = 'event-join-fan'),
    #endpoint where a fan can leave from event 
    path('client/fan/event/leave',FanLeaveFromEvent.as_view(),
        name = 'event-leave-fan'),
    #endpoint where a user can leaver from event 
    path('client/event/leave',LeaveFromEvent.as_view(),
        name = 'event-leave'),
    #endpoint where a use can get list of user events
    path('client/my/events/list',UserEvents.as_view(),
        name = 'user-events-list'),
    #endpoint where a use can get list of user events
    path('client/user/planned/events/list<int:pk>',UserPlannedEvents.as_view(),
        name = 'events-planned-list'),
    #endpoint where a use can get list of user events
    path('client/user/planned/events/list<int:pk>',UserPlannedEvents.as_view(),
        name = 'events-planned-list'),
     #endpoint where a use can get list of events
    path('client/popular/events/list',PopularIvents.as_view(),
        name = 'popular-events-list'),
]

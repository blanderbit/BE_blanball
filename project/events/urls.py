from .views import *

from django.urls import path




urlpatterns = [
    #endpoint where a user with admin
    #role can create a new one event 
    path('client/event/create',CreateEvent.as_view()),
    #endpoint where a user with admin
    #role can get detail info and delete event 
    path('client/event/<int:pk>',GetDeleteEvent.as_view()),
    #endpoint where a user with admin
    #role can get detail info and delete event 
    path('client/event/update/<int:pk>',UpdateEvent.as_view()),
    #endpoint where a use can get list of events
    path('client/events/list',EventList.as_view()),
    #endpoint where a user with admin
    #role can delete events
    path('admin/events/delete',DeleteEvents.as_view()),
    #endpoint where a user can join to event 
    path('client/event/join',JoinToEvent.as_view()),
    #endpoint where a fan can join to event 
    path('client/fan/event/join',FanJoinToEvent.as_view()),
    #endpoint where a fan can leave from event 
    path('client/fan/event/leave',FanLeaveFromEvent.as_view()),
    #endpoint where a user can leaver from event 
    path('client/event/leave',LeaveFromEvent.as_view()),
    #endpoint where a user can get list of user events
    path('client/my/events/list',UserEvents.as_view()),
    #endpoint where a user can get list of user events
    path('client/user/planned/events/list<int:pk>',UserPlannedEvents.as_view()),
    #endpoint where a user can get list of user events
    path('client/user/planned/events/list<int:pk>',UserPlannedEvents.as_view()),
     #endpoint where a user can get list of events
    path('client/popular/events/list',PopularIvents.as_view()),
    #endpoint where a user can invite other user to ivent
    path('client/invite/user/to/event',InviteUserToEvent.as_view()),
]
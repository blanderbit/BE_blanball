from .set_up import SetUpEventsViews,LoginUserSetUp
from rest_framework import status
from events.models import *
from django.urls import reverse
from notifications.models import Notification


class TestEventsViews(SetUpEventsViews,LoginUserSetUp):

    def test_create_event_with_no_auth(self) -> None:
        response = self.client.post(reverse("event-create"),self.event_create_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_create(self) -> None:
        self.auth()
        response = self.client.post(reverse("event-create"),self.event_create_data)
        self.assertEqual(Event.objects.count(),1)
        self.assertEqual(Event.objects.first().status,'Planned')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_event_create_without_phone(self) -> None:
        self.auth()
        response = self.client.post(reverse("event-create"),self.event_create_withount_phone_data)
        self.assertEqual(Event.objects.count(),1)
        self.assertEqual(Event.objects.first().contact_number,User.objects.first().phone)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_event_create_author_invites_himself(self) -> None:
        self.auth()
        self.event_create_data['current_users'].append(self.user.id)
        response = self.client.post(reverse("event-create"),self.event_create_data)
        self.assertEqual(Notification.objects.count(),0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_author_event_join(self) -> None:
        self.auth()
        self.client.post(reverse("event-create"),self.event_create_data)
        self.assertEqual(Event.objects.count(),1)
        response = self.client.post(reverse("join-to-event"),self.event_join_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_events_list(self) -> None:
        self.auth()
        self.client.post(reverse("event-create"),self.event_create_data)
        self.assertEqual(Event.objects.count(),1)
        response=self.client.get(reverse("user-events"))
        self.assertEqual(response.data['total_count'],1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_events_list_with_no_auth(self) -> None:
        response=self.client.get(reverse("user-events"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
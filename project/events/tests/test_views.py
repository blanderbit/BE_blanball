from .set_up import SetUpEventsViews
from rest_framework import status
from events.models import *
from django.urls import reverse
from notifications.models import Notification
from freezegun import freeze_time
from events.tasks import check_event_start_time


class TestEventsViews(SetUpEventsViews):

    @freeze_time("2022-9-29")
    def test_event_create(self) -> None:
        self.auth()
        response = self.client.post(reverse("event-create"),self.event_create_data)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.first().status, 'Planned')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @freeze_time("2022-9-29")
    def test_event_create_without_phone(self) -> None:
        self.auth()
        response = self.client.post(reverse("event-create"),self.event_create_withount_phone_data)
        self.assertEqual(Event.objects.count(),1)
        self.assertEqual(Event.objects.first().contact_number,User.objects.first().phone)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @freeze_time("2022-9-29")
    def test_event_create_author_invites_himself(self) -> None:
        self.auth()
        self.event_create_data['current_users'].append(User.objects.first().id)
        response = self.client.post(reverse("event-create"), self.event_create_data)
        self.assertEqual(Notification.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @freeze_time("2022-10-01")
    def test_event_create_with_bad_start_time(self):
        self.auth()
        response = self.client.post(reverse("event-create"),self.event_create_data)
        self.assertEqual(Event.objects.count(),0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @freeze_time("2022-9-29")
    def test_author_event_join(self) -> None:
        self.auth()
        self.client.post(reverse("event-create"),self.event_create_data)
        response = self.client.post(reverse("join-to-event"),self.event_join_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @freeze_time("2022-9-29")
    def test_event_join(self):
        self.auth()
        self.client.post(reverse("event-create"),self.event_create_data)
        self.client.force_authenticate(None)
        self.client.post(reverse('register'), self.user_reg_data_2)
        self.client.force_authenticate(User.objects.get(email = self.user_reg_data_2['email']))
        response = self.client.post(reverse("join-to-event"), {"event_id":Event.objects.first().id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.first().count_current_users,1)

    @freeze_time("2022-9-29")
    def test_second_event_join(self):
        self.auth()
        self.client.post(reverse("event-create"),self.event_create_data)
        self.client.force_authenticate(None)
        self.client.post(reverse('register'), self.user_reg_data_2)
        self.client.force_authenticate(User.objects.get(email=self.user_reg_data_2['email']))
        event_join = self.client.post(reverse("join-to-event"), {"event_id": Event.objects.first().id})
        event_join_2 = self.client.post(reverse("join-to-event"), {"event_id": Event.objects.first().id})
        self.assertEqual(event_join.status_code, status.HTTP_200_OK)
        self.assertEqual(event_join_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Event.objects.first().count_current_users,1)

    @freeze_time("2022-9-29")
    def test_user_events_list(self) -> None:
        self.auth()
        self.client.post(reverse("event-create"), self.event_create_data)
        self.client.force_authenticate(None)
        self.client.post(reverse('register'), self.user_reg_data_2)
        self.client.force_authenticate(User.objects.get(email = self.user_reg_data_2['email']))
        self.client.post(reverse("event-create"),self.event_create_data)
        response = self.client.get(reverse("user-events-list"))
        self.assertEqual(Event.objects.count(),2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['total_count'], 1)
    
    def test_get_events_list(self):
        self.auth()
        get_all_users_list = self.client.get(reverse("events-list"))
        # self.assertEqual(get_all_users_list.data['total_count'], Event.objects.count())


    def auth(self):
        self.client.post(reverse('register'), self.user_reg_data)
        user = User.objects.get(email = self.user_reg_data['email'])
        return self.client.force_authenticate(user)
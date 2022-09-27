from typing import Any
from authentication.models import (
    User,
    Profile,
)

from collections import OrderedDict
from rest_framework.test import APITestCase


class SetUpAuthenticationModels(APITestCase):
    def setUp(self) -> OrderedDict:
        self.profile_data: dict[str,Any] = {
            'name':'John',
            'last_name':'Jesus',
            'gender':'Man',
            'birthday':'2000-09-09',
            'height':30,
            'weight':30,
            'position':'postion'
        }
        self.user_data = {
            "email": "user@example.com",
            "phone": "+380683861969",
            "password": "string11",
        }
        self.profile: Profile = Profile.objects.create(**self.profile_data)
        self.user: User = User.objects.create(**self.user_data,profile = self.profile)
        return super().setUp()

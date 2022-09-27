from collections import OrderedDict
from types import NoneType

from rest_framework.test import APITestCase
from authentication.models import *
from events.models import *
from django.urls import reverse


class LoginUserSetUp:
    def auth(self) -> NoneType:
        data = {
            "email": "user@example.com",
            "phone": "+380683861969",
            "password": "string11",
            "re_password": "string11",
            "profile": {
                "name": "string",
                "last_name": "string",
                "gender": "Man",
                "birthday": "2000-09-10",
                "height": 30,
                "weight": 30,
                "position": "Вратар",
                "about_me": "string"
            }
        } 

        self.client.post(reverse("register"),data)
        self.user = User.objects.get(email = data['email'])
        return self.client.force_authenticate(self.user)

class SetUpAauthenticationViews(APITestCase):
    def setUp(self) -> OrderedDict:
        self.user_register_data = {
            "email": "user@example.com",
            "phone": "+380683861969",
            "password": "string11",
            "re_password": "string11",
            "profile": {
                "name": "string",
                "last_name": "string",
                "gender": "Man",
                "birthday": "2000-09-10",
                "height": 30,
                "weight": 30,
                "position": "Вратар",
                "about_me": "string"
            }
        } 
        self.user_register_bad_data = {
            "email": "user@example.com",
            "phone": "gffgfgfg",
            "password": "string12121",
            "re_password": "string11",
            "profile": {
                "name": "string",
                "last_name": "string",
                "gender": "Man",
                "birthday": "2000-09-10",
                "height": 30,
                "weight": 30,
                "position": "Вратар",
                "about_me": "string"
            }
        } 
        self.user_login_data = {
            "email": "user@example.com",
            "password": "string11"
        }

        self.request_change_password_data = {
            "new_password": "19211921",
            "old_password": "string11",
        }

        self.request_change_password_bad_data = {
            "new_password": "19211921",
            "old_password": "string1",
        }

        self.code_bad_data = {
            "verify_code": "11111"
        }

        return super().setUp()

    
class SetUpAuthenticationModels(APITestCase):
    def setUp(self) -> OrderedDict:
        self.profile_data = {
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
        self.profile = Profile.objects.create(**self.profile_data)
        self.user = User.objects.create(**self.user_data,profile = self.profile)
        return super().setUp()



class SetUpEventsViews(APITestCase):
    def setUp(self) -> OrderedDict:
        self.event_create_data = {
            "name": "string",
            "small_disc": "string",
            "full_disc": "string",
            "place": "string",
            "gender": "Man",
            "date_and_time": "2230-10-17T10:26:26.178Z",
            "contact_number": "+380683861202",
            "need_ball": True,
            "amount_members": 50,
            "type": "Football",
            "price": 32767,
            "price_description": "string",
            "need_form": True,
            "privacy": True,
            "duration": 10,
            "forms": "Shirt-Front",
            "current_users": []
        }

        self.event_create_withount_phone_data = {
            "name": "string",
            "small_disc": "string",
            "full_disc": "string",
            "place": "string",
            "gender": "Man",
            "date_and_time": "2230-10-17T10:26:26.178Z",
            "need_ball": True,
            "amount_members": 50,
            "type": "Football",
            "price": 32767,
            "price_description": "string",
            "need_form": True,
            "privacy": True,
            "duration": 10,
            "forms": "Shirt-Front",
            "current_users": []
        }

        self.event_join_data = {
            "event_id": 1
        }
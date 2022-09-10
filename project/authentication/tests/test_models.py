from rest_framework.test import APITestCase
from authentication.models import *
import jwt

from django.conf import settings

class SetUpTest(APITestCase):
    def setUp(self):
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

class TestAuthenticationModels(SetUpTest):
    
    def test_create_user(self):
        self.assertEqual(Profile.objects.count(),1)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(self.user.profile_id,self.profile.id)

    def test_check_user_defalut_fields(self):
        self.assertEqual(self.user.get_planned_events,'1m')
        self.assertEqual(self.user.group_name,'user_1')
        self.assertEqual(self.user.__str__(),'user@example.com')
        self.assertEqual(self.user.configuration,{'email': True,'phone':True})
    
    def test_user_tokens_method(self):
        self.client.force_authenticate(self.user.tokens()['access'])
        payload = jwt.decode(self.user.tokens()['access'], settings.SECRET_KEY, algorithms="HS256")
        self.assertEqual(self.user.id,payload['user_id'])


    def test_max_birthday_age(self):
        Profile.objects.create(birthday = '1800-01-01')
        Profile.objects.create(birthday = '2000-01-01')
        # self.assertFalse(Profile.objects.create(birthday = '2000-01-01'))
        print(Profile.objects.count())
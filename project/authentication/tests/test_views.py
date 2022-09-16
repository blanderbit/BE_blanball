from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from project.constaints import EMAIL_CHANGE_CODE_TYPE
from authentication.models import *

class SetUpTest(APITestCase):
    def setUp(self):
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
                "position": "string",
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
                "position": "string",
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


class TestAuthenticationViews(SetUpTest):

    def test_user_register(self):
        response = self.client.post(reverse("register"),self.user_register_data)
        self.assertEqual(User.objects.count(),1)
        self.assertTrue(User.objects.get(email =self.user_register_data['email']).profile.age >= 22)
        self.assertEqual("User",User.objects.get(email =self.user_register_data['email']).role)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_register_without_data(self):
        response = self.client.post(reverse("register"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_users_with_same_data(self):
        self.client.post(reverse("register"),self.user_register_data)
        response = self.client.post(reverse("register"),self.user_register_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_users_with_bad_data(self):
        response = self.client.post(reverse("register"),self.user_register_bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        self.client.post(reverse("register"),self.user_register_data)
        response = self.client.post(reverse("login"),self.user_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_without_data(self):
        response = self.client.post(reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_my_profile_with_no_atuhorized(self):
        response = self.client.get(reverse("my-profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_my_profile_with_atuhorized(self):
        self.auth()
        response = self.client.get(reverse("my-profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_list_with_atuhorized(self):
        self.auth()
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_list_with_no_atuhorized(self):
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_with_authorized(self):
        self.auth()
        response = self.client.post(reverse("register"),self.user_register_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_with_authorized(self):
        self.auth()
        response = self.client.post(reverse("login"),self.user_login_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_change_password(self):
        self.auth()
        response = self.client.post(reverse("request-change-password"),self.request_change_password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_change_password_with_bad_data(self):
        self.auth()
        response = self.client.post(reverse("request-change-password"),self.request_change_password_bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_change_password_without_authorization(self):
        response = self.client.post(reverse("request-change-password"),self.request_change_password_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_code_with_bad_data(self):
        self.auth()
        response = self.client.post(reverse("check-code"),self.code_bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_code(self):
        self.auth()
        code = Code.objects.create(verify_code='FFFFF',
            user_email=self.user_register_data['email'],type=EMAIL_CHANGE_CODE_TYPE,dop_info='userexample@gmail.com111',life_time= 
            timezone.now() + timezone.timedelta(minutes=CODE_EXPIRE_MINUTES_TIME))
        response = self.client.post(reverse("check-code"),{"verify_code":code.verify_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_request_reset_password(self):
        register_user = self.client.post(reverse("register"),self.user_register_data)
        request_reset = self.client.post(reverse("request-reset-password"),{"email":register_user.data['email']})
        self.assertEqual(request_reset.status_code, status.HTTP_200_OK)
    
    def test_request_reset_password_with_authorized(self):
        register_user = self.client.post(reverse("register"),self.user_register_data)
        self.auth()
        request_reset = self.client.post(reverse("request-reset-password"),{"email":register_user.data['email']})
        self.assertEqual(request_reset.status_code, status.HTTP_403_FORBIDDEN)


    def auth(self):
        self.client.post(reverse("register"),self.user_register_data)
        user = User.objects.get(email = self.user_register_data['email'])
        return self.client.force_authenticate(user)

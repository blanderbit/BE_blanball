from types import NoneType
from django.urls import reverse
from rest_framework import status
from project.constaints import EMAIL_CHANGE_CODE_TYPE
from authentication.models import *
from .set_up import SetUpAauthenticationViews


class TestAuthenticationViews(SetUpAauthenticationViews):

    def test_user_register(self) -> None:
        response = self.client.post(reverse("register"),self.user_register_data)
        self.assertEqual(User.objects.count(),1)
        self.assertTrue(User.objects.get(email =self.user_register_data['email']).profile.age >= 22)
        self.assertEqual("User",User.objects.get(email =self.user_register_data['email']).role)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_register_without_data(self) -> None:
        response = self.client.post(reverse("register"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_users_with_same_data(self) -> None:
        self.client.post(reverse("register"),self.user_register_data)
        response = self.client.post(reverse("register"),self.user_register_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_users_with_bad_data(self) -> None:
        response = self.client.post(reverse("register"),self.user_register_bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self) -> None:
        self.client.post(reverse("register"),self.user_register_data)
        response = self.client.post(reverse("login"),self.user_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_without_data(self) -> None:
        response = self.client.post(reverse("login"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_my_profile_with_no_atuhorized(self) -> None:
        response = self.client.get(reverse("my-profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_my_profile_with_atuhorized(self) -> None:
        self.auth()
        response = self.client.get(reverse("my-profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_list_with_atuhorized(self) -> None:
        self.auth()
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_list_with_no_atuhorized(self) -> None:
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_with_authorized(self) -> None:
        self.auth()
        response = self.client.post(reverse("register"),self.user_register_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_with_authorized(self) -> None:
        self.auth()
        response = self.client.post(reverse("login"),self.user_login_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_change_password(self) -> None:
        self.auth()
        response = self.client.post(reverse("request-change-password"),self.request_change_password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_request_change_password_with_bad_data(self) -> None:
        self.auth()
        response = self.client.post(reverse("request-change-password"),self.request_change_password_bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_change_password_without_authorization(self) -> None:
        response = self.client.post(reverse("request-change-password"),self.request_change_password_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_code_with_bad_data(self) -> None:
        self.auth()
        response = self.client.post(reverse("check-code"),self.code_bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_code(self) -> None:
        self.auth()
        code:Code = Code.objects.create(verify_code='FFFFF',
            user_email=self.user_register_data['email'],type=EMAIL_CHANGE_CODE_TYPE,dop_info='userexample@gmail.com111',life_time= 
            timezone.now() + timezone.timedelta(minutes=CODE_EXPIRE_MINUTES_TIME))
        response = self.client.post(reverse("check-code"),{"verify_code":code.verify_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_request_reset_password(self) -> None:
        register_user = self.client.post(reverse("register"),self.user_register_data)
        request_reset = self.client.post(reverse("request-reset-password"),{"email":register_user.data['email']})
        self.assertEqual(request_reset.status_code, status.HTTP_200_OK)
    
    def test_request_reset_password_with_authorized(self):
        register_user = self.client.post(reverse("register"),self.user_register_data)
        self.auth()
        request_reset = self.client.post(reverse("request-reset-password"),{"email":register_user.data['email']})
        self.assertEqual(request_reset.status_code, status.HTTP_403_FORBIDDEN)


    def auth(self) -> NoneType:
        self.client.post(reverse("register"),self.user_register_data)
        user = User.objects.get(email = self.user_register_data['email'])
        return self.client.force_authenticate(user)

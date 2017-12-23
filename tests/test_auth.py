from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from core.utils import generate_hash
from tests import factories


class LoginAPIViews(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(email="john@snow.de")
        self.user.set_password('test1234TEST')
        self.user.save()
        self.user1 = factories.UserFactory(email="daineris@targarien.de")
        self.user1.set_password('test1234TEST')
        self.user.save()
        self.client = APIClient()

    def test_user_is_authenticated_with_credentials(self):
        url = reverse("accounts-user-login")
        response = self.client.post(url, data={"email": "john@snow.de", "password": "test1234TEST"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_404_with_wrong_credentials(self):
        url = reverse("accounts-user-login")
        response = self.client.post(url,
                                    data={"email": "john@snow.de",
                                          "password": "WRONG_PASSWORD"}
                                    )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RegisterApiView(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(email="john@snow.de")
        self.hashed_email = generate_hash(self.user.email)

    def test_register_user_return_user_information(self):
        url = reverse("accounts-user-register")
        test_data = {
            "email": "john_targarian@snow.de",
            "first_name": "John",
            "last_name": "Snow",
            "password": "test1234TEST"
        }
        response = self.client.post(
            url,
            data=test_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('email'), test_data.get('email'))
        self.assertEqual(response.data.get('first_name'), test_data.get('first_name'))
        self.assertEqual(response.data.get('last_name'), test_data.get('last_name'))
        self.assertNotIn('password', response.data.keys())

    def test_raise_400_execption_if_validation_didnt_pass(self):
        url = reverse("accounts-user-register")
        test_data = {
            "email": "WRONG_EMAIL",
            "first_name": "John",
            "last_name": "Snow",
            "password": "test1234TEST"
        }
        response = self.client.post(
            url,
            data=test_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data, {'email': ['Enter a valid email address.']})

    def test_verify_user_mail(self):
        url = reverse("accounts-user-verify", kwargs={"email": self.hashed_email})
        self.assertFalse(self.user.verified)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_user_password(self):
        url = reverse("accounts-user-reset", kwargs={"email": self.hashed_email})
        response = self.client.post(url, data={'password': 'new_pass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_user_password(self):
        url = reverse("accounts-user-password", kwargs={"email": self.hashed_email})
        response = self.client.post(url, data={'password': 'new_pass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

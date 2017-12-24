from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from core.utils import encode_email, decode_email


class HealthCheckTests(APITestCase):
    def test_ok(self):
        url = reverse('health_check-list')
        response = self.client.get(
            url
        )
        self.assertEqual(response.status_code, 200)


class UtilsTests(TestCase):
    def test_encode_email(self):
        res = encode_email('little@finger.com')
        self.assertEqual(b'bGl0dGxlQGZpbmdlci5jb20=', res)

    def test_decode_email(self):
        res = decode_email('dGlyaW9uQGxhbmlzdGVyLmNvbQ==')
        self.assertEqual('tirion@lanister.com', res)

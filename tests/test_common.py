from django.urls import reverse
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    def test_ok(self):
        url = reverse('health_check-list')
        response = self.client.get(
            url
        )
        self.assertEqual(response.status_code, 200)

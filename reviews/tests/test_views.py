from django.test import Client, TestCase
from django.urls import reverse


class HomeTestCase(TestCase):
    def test_test(self):
        self.client = Client()

        response = self.client.get(reverse('app_reviews:test'))
        self.assertEqual(response.status_code, 200)
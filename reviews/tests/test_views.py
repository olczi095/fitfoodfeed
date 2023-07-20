from django.test import TestCase


class HomePageTestCase(TestCase):
    def test_home_page_returns_correct_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
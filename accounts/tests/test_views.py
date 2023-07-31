from django.test import TestCase
from django.urls import reverse


class RegisterTestCase(TestCase):
    
    def test_register_url(self):
        response = self.client.get(reverse('app_accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
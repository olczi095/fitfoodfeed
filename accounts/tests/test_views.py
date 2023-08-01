from django.test import TestCase
from django.urls import reverse, reverse_lazy
from accounts.forms import CustomUserCreationForm


class RegisterTestCase(TestCase):
    
    def test_register_url(self):
        response = self.client.get(reverse('app_accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_redirect_home_form_valid(self):
        valid_data = {
            'username': 'user1',
            'password1': 'user1_password',
            'password2': 'user1_password',
            'email': 'user1@mail.com'
        }
        form = CustomUserCreationForm(valid_data)
        is_form_valid = form.is_valid()
        self.assertTrue(is_form_valid)

        response = self.client.post(reverse('app_accounts:register'), valid_data, follow=True)
        self.assertRedirects(response, reverse_lazy('app_reviews:home'))
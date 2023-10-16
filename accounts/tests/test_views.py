from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.messages import get_messages

from accounts.forms import CustomUserCreationForm
from accounts.models import User


class RegisterTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'user1',
            'password1': 'user1_password',
            'password2': 'user1_password',
            'email': 'user1@mail.com'
        }
        form = CustomUserCreationForm(self.valid_data)
        is_form_valid = form.is_valid()
        self.assertTrue(is_form_valid)
    
    def test_register_url(self):
        response = self.client.get(reverse('app_accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_display_success_message_after_valid_register(self):
        success_message = f"Registration Successful! Now you can log in."
        response = self.client.post(reverse('app_accounts:register'), self.valid_data, follow=True)
        self.assertContains(response, success_message)
        
    def test_redirect_login_page_after_successful_registration(self):
        response = self.client.post(reverse('app_accounts:register'), self.valid_data, follow=True)
        self.assertRedirects(response, reverse_lazy('app_accounts:login'))

class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_login = User.objects.create_user(username='admin', password='asdf1234', email='admin@test.pl')
        cls.user_login = user_login

    def test_login_url(self):
        response = self.client.get(reverse('app_accounts:login'))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_redirect_home(self):
        response = self.client.post(reverse('app_accounts:login'), {'username':'admin', 'password':'asdf1234'}, follow=True)
        self.assertRedirects(response, reverse_lazy('app_reviews:home'))

    def test_valid_login_display_success_message(self):
        response = self.client.post(reverse("app_accounts:login"), {'username':'admin', 'password':'asdf1234'}, follow=True)
        success_message = "Hello, <strong>admin</strong>!"
        self.assertContains(response, success_message)

    def test_invalid_login_stay_on_page(self):
        response = self.client.post(reverse('app_accounts:login'), {'username':'incorrect_username', 'password':'incorrect_password'}, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_invalid_username_display_error_message(self):
        response = self.client.post(reverse('app_accounts:login'), {'username':'incorrect_username', 'password':'asdf1234'}, follow=True)
        error_message = "Invalid username or password."
        self.assertContains(response, error_message)

    def test_invalid_password_display_error_message(self):
        response = self.client.post(reverse('app_accounts:login'), {'username':'admin', 'password':'incorrect_password'}, follow=True)
        error_message = "Invalid username or password."
        self.assertContains(response, error_message)
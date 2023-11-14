from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth import get_user_model

from accounts.forms import CustomUserCreationForm


User = get_user_model()


class RegisterTestCase(TestCase):
    def setUp(self):
        self.register_url = reverse('app_accounts:register')
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
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_display_success_message_after_valid_register(self):
        success_message = f"Registration Successful! Now you can log in."
        response = self.client.post(self.register_url, self.valid_data, follow=True)
        self.assertContains(response, success_message)
        
    def test_redirect_login_page_after_successful_registration(self):
        response = self.client.post(self.register_url, self.valid_data, follow=True)
        self.assertRedirects(response, reverse_lazy(settings.LOGIN_URL))

class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_login = User.objects.create_user(username='admin', password='asdf1234', email='admin@test.pl')
        cls.login_url = reverse(settings.LOGIN_URL) 
        cls.home_url = reverse(settings.LOGIN_REDIRECT_URL)

    def test_login_url(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_redirect_home(self):
        response = self.client.post(self.login_url, {'username':'admin', 'password':'asdf1234'}, follow=True)
        self.assertRedirects(response, self.home_url)

    def test_valid_login_display_success_message(self):
        response = self.client.post(self.login_url, {'username':'admin', 'password':'asdf1234'}, follow=True)
        success_message = "Hello, <strong>admin</strong>!"
        self.assertContains(response, success_message)

    def test_invalid_login_stay_on_page(self):
        response = self.client.post(self.login_url, {'username':'incorrect_username', 'password':'incorrect_password'}, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_invalid_username_display_error_message(self):
        response = self.client.post(self.login_url, {'username':'incorrect_username', 'password':'asdf1234'}, follow=True)
        error_message = "Invalid username or password."
        self.assertContains(response, error_message)

    def test_invalid_password_display_error_message(self):
        response = self.client.post(self.login_url, {'username':'admin', 'password':'incorrect_password'}, follow=True)
        error_message = "Invalid username or password."
        self.assertContains(response, error_message)
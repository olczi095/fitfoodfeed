from django.test import TestCase

from accounts.forms import CustomUserCreationForm


class CustomUserCreationFormTests(TestCase):
    def test_form_valid(self):
        valid_data = {
            'username': 'user1',
            'password1': 'user1_password',
            'password2': 'user1_password',
            'email': 'user1@mail.com'
        }
        form = CustomUserCreationForm(valid_data)
        is_form_valid = form.is_valid()
        self.assertTrue(is_form_valid)

    def test_form_invalid_without_username(self):
        invalid_data = {
            'username': '',
            'password1': 'user1_password',
            'password2': 'user1_password',
            'email': 'user1@mail.com'
        }
        form = CustomUserCreationForm(invalid_data)
        is_form_valid = form.is_valid()
        self.assertFalse(is_form_valid)

    def test_form_invalid_wrong_password(self):
        invalid_data = {
            'username': 'user2',
            'password1': 'user1_password',
            'password2': 'user2_password',
            'email': 'user2@mail.com'
        }
        form = CustomUserCreationForm(invalid_data)
        is_form_valid = form.is_valid()
        self.assertFalse(is_form_valid)

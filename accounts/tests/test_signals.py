from django.contrib.auth.models import Group
from django.test import TestCase
from accounts.models import User


class SignalsTestCase(TestCase):
    def test_adding_superuser_to_admin_group(self):
        admin_group, created = Group.objects.get_or_create(name='admin')
        user = User.objects.create(
            username='test_user', 
            password='test_password',
            bio='test_bio',
            is_superuser=True
        )
        user_has_admin_group = admin_group in user.groups.all()
        self.assertTrue(user_has_admin_group)
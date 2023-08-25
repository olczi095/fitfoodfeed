from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from accounts.admin import UserAdmin
from accounts.models import User


class UserAdminModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user', 
            password='test_password',
            bio='something about the user'
        )

    def test_display_user_on_admin_page(self):
        user_admin = UserAdmin(model=self.user, admin_site=AdminSite())
        displayed_user = user_admin.display_user(self.user)
        self.assertEqual(displayed_user, 'test_user')

    def test_display_groups_on_admin_page(self):
        user_admin = UserAdmin(model=self.user, admin_site=AdminSite())
        displayed_groups = user_admin.display_groups(self.user)
        self.assertEqual(displayed_groups, '')
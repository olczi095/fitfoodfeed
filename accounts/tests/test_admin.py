from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite

from accounts.admin import UserAdmin


User = get_user_model()


class UserAdminModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='test_user',
            password='test_password',
            bio='something about the user'
        )

        cls.user_admin = UserAdmin(model=cls.user, admin_site=AdminSite())

    def test_display_user_on_admin_page(self):
        displayed_user = self.user_admin.display_user(self.user)
        self.assertEqual(displayed_user, 'test_user')

    def test_display_groups_on_admin_page(self):
        displayed_groups = self.user_admin.display_groups(self.user)
        self.assertEqual(displayed_groups, '')

    def test_fieldsets_configuration(self):
        actual_fieldsets = self.user_admin.fieldsets
        expected_fieldsets = [
            (
                "Identification Data",
                {'fields': ['username', 'password', 'first_name', 'last_name', 'email']}
            ),
            (
                "Administration Properties",
                {'fields': ['is_active', 'is_superuser', 'is_staff', 'is_author']}
            ),
            (
                "Permission-related Fields",
                {'fields': ['groups', 'user_permissions']}
            ),
            (
                "Additional Information",
                {'fields': ['avatar', 'bio']}
            )
        ]
        for actual, expected in zip(actual_fieldsets, expected_fieldsets):
            self.assertTupleEqual(actual, expected)

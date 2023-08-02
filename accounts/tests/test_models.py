from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from accounts.admin import UserAdmin
from accounts.models import User


class UserModelExistenceTestCase(TestCase):
    def test_user_model_exists(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

        
class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user', 
            password='test_password',
            bio='test_bio'
        )

    def test_bio_with_expected_value(self):
        self.assertEqual(self.user.bio, 'test_bio')

    def test_string_representation_with_username(self):
        self.assertEqual(str(self.user), 'test_user')

    def test_image_field_with_default_image(self):
        self.assertIsNotNone(self.user.avatar)
        self.assertEqual(self.user.avatar.name, 'avatars/default-avatar.png')

    def test_is_author_field_exists(self):
        field_exists = 'is_author' in [field.name for field in self.user._meta.get_fields()]
        self.assertTrue(field_exists)
        self.assertEqual(self.user._meta.get_field('is_author').verbose_name, 'author status')


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
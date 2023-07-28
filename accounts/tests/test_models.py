from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from accounts.admin import UserAdmin
from accounts.models import User, Author


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

    def test_role_field_default_returns_user(self):
        self.assertEqual(self.user.role, 'user')


class RoleUserTestCase(TestCase):
    def test_role_labels(self):
        self.assertEqual(User.Role.ADMIN.label, 'admin')
        self.assertEqual(User.Role.AUTHOR.label, 'author')
        self.assertEqual(User.Role.USER.label, 'user')


class AuthorModelExistenceTestCase(TestCase):
    def test_author_model_exists(self):
        authors = Author.objects.all()
        self.assertEqual(authors.count(), 0)

        
class AuthorModelTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create(
            username='test_user', 
            password='test_password',
            bio='test_bio'
        )

    def test_bio_with_expected_value(self):
        self.assertEqual(self.author.bio, 'test_bio')

    def test_string_representation_with_username(self):
        self.assertEqual(str(self.author), 'test_user')

    def test_image_field_with_default_image(self):
        self.assertIsNotNone(self.author.avatar)
        self.assertEqual(self.author.avatar.name, 'avatars/default-avatar.png')


class AuthorAdminModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            username='test_user', 
            password='test_password',
            bio='something about the user'
        )

    def test_display_user_on_admin_page(self):
        author_admin = UserAdmin(model=self.author, admin_site=AdminSite())
        displayed_author = author_admin.display_user(self.author)
        self.assertEqual(displayed_author, 'test_user')
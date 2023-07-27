from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from reviews.admin import AuthorAdmin
from reviews.models import Author


class AuthorModelExistenceTestCase(TestCase):
    def test_author_model_exists(self):
        authors = Author.objects.all()
        self.assertEqual(authors.count(), 0)

        
class AuthorModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            username='test_user', 
            password='test_password',
            bio='test_bio'
        )

    def test_bio_with_expected_value(self):
        self.assertEqual(self.author.bio, 'test_bio')

    def test_string_representation_with_username(self):
        self.assertEqual(str(self.author), 'test_user')

    def test_string_representation_without_username(self):
        anonymous = Author()
        self.assertEqual(str(anonymous), 'Anonymous')

    def test_image_field_with_default_image(self):
        self.assertIsNotNone(self.author.avatar)
        self.assertEqual(self.author.avatar.name, 'avatars/default-avatar.png')


class AuthorAdminModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            username='test_user', 
            password='test_password',
            bio='test_bio'
        )

    def test_display_author_on_admin_page(self):
        author_admin = AuthorAdmin(model=self.author, admin_site=AdminSite())
        displayed_author = author_admin.display_author(self.author)
        self.assertEqual(displayed_author, 'test_user')

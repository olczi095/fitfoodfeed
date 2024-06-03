from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelExistenceTests(TestCase):
    def test_user_model_exists(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 0)


class UserModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='test_user',
            password='test_password',
            bio='test_bio'
        )

    def test_user_bio_matches_expected_value(self):
        self.assertEqual(self.user.bio, 'test_bio')

    def test_user_string_is_correct(self):
        self.assertEqual(str(self.user), 'test_user')

    def test_image_field_has_none_default_image(self):
        self.assertEqual(self.user.avatar.name, None)

    def test_is_author_field_exists(self):
        self.assertTrue(hasattr(self.user, 'is_author'))
        self.assertEqual(
            self.user._meta.get_field('is_author').verbose_name,
            'author status'
        )

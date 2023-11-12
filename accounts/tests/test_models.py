from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


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
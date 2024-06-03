from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class SignalsTests(TestCase):
    def test_author_add_permissions(self):
        test_author = User.objects.create_user(
            username='author',
            password='xyz',
            is_author=True
        )
        self.assertTrue(test_author.is_author)

        expected_permissions = ['add_post', 'view_post']
        test_author_permissions = [
            permission.codename
            for permission in test_author.user_permissions.all()
        ]
        for expected_permission in expected_permissions:
            self.assertIn(expected_permission, test_author_permissions)

    def test_non_author_no_permissions(self):
        test_author = User.objects.create_user(
            username='author',
            password='xyz',
            is_author=False
        )
        self.assertFalse(test_author.is_author)

        expected_permissions = ['add_post', 'view_post']
        test_author_permissions = [
            permission.codename
            for permission in test_author.user_permissions.all()
        ]
        for expected_permission in expected_permissions:
            self.assertNotIn(expected_permission, test_author_permissions)

    def test_superuser_is_staff_set_to_true(self):
        test_user = User.objects.create_user(
            username='superuser',
            password='xyz'
        )
        test_user.is_superuser = True
        test_user.save()
        self.assertTrue(test_user.is_superuser)
        self.assertTrue(test_user.is_staff)

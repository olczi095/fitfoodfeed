from django.contrib.auth import get_user_model
from django.test import TestCase

from carts.models import ShoppingUser

User = get_user_model()


class ShoppingUserExistenceTest(TestCase):
    def test_model_exists(self):
        shopping_users = ShoppingUser.objects.all()
        self.assertEqual(shopping_users.count(), 0)


class ShoppingUserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='test_password'
        )

    def test_create_shopping_user(self):
        shopping_user = ShoppingUser.objects.create(
            user=self.user
        )
        self.assertEqual(ShoppingUser.objects.all().count(), 1)
        self.assertEqual(shopping_user.user, self.user)
        self.assertEqual(shopping_user.cart, {})

    def test_delete_user(self):
        self.user.delete()
        self.assertEqual(ShoppingUser.objects.all().count(), 0)

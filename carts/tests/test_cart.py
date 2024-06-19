from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import TestCase

from carts.cart import AnonymousCart, AuthenticatedCart, BaseCart
from shop.models import Product

User = get_user_model()


class UnimplementedCart(BaseCart):
    """
    A subclass of BaseCart that does not implement the abstract methods. 
    Created just for tests.
    """


class AnonymousCartTests(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.session = self.client.session
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.second_product = Product.objects.create(name='Second Test Product', price=20.0)
        self.cart = AnonymousCart(self.request)

    def test_add_item(self):
        self.cart.add(self.product, 2)
        self.assertEqual(len(self.cart), 2)
        self.assertEqual(self.cart.get_total_price(), 20.0)

    def test_add_existing_product(self):
        self.cart.add(self.product)
        for item in self.cart:
            if item['name'] == self.product.name:
                self.assertEqual(item['quantity'], 1)
        self.cart.add(self.product)
        for item in self.cart:
            if item['name'] == self.product.name:
                self.assertEqual(item['quantity'], 2)

    def test_update_quantity_to_odd_raises_error(self):
        self.cart.add(self.product)
        with self.assertRaises(ValueError):
            self.cart.update(self.product, -1)

    def test_update_quantity_to_zero(self):
        self.cart.add(self.product)
        self.cart.update(self.product, 0)
        self.assertEqual(len(self.cart), 0)

    def test_update_quantity_to_normal_value(self):
        self.cart.add(self.product)
        self.cart.update(self.product, 100)
        for item in self.cart:
            if item['name'] == self.product.name:
                self.assertEqual(item['quantity'], 100)

    def test_update_quantity_for_product_not_in_cart(self):
        with self.assertRaises(KeyError):
            self.cart.update(self.product, 10)

    def test_iter_no_items(self):
        items = list(self.cart)
        self.assertEqual(len(items), 0)

    def test_cart_iter_two_items(self):
        self.cart.add(self.product, 2)
        self.cart.add(self.second_product)
        items = list(self.cart)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['name'], 'Test Product')
        self.assertEqual(items[1]['name'], 'Second Test Product')
        self.assertEqual(items[0]['price'], 10.0)
        self.assertEqual(items[1]['price'], 20.0)

    def test_reset_cart(self):
        self.cart.add(self.product, quantity=2)
        self.assertEqual(len(self.cart), 2)

        self.cart.reset()
        self.assertNotIn('cart', self.request.session)


class AuthenticatedCartTests(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.session = self.client.session
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.client.force_login(self.user)
        self.request.user = self.user
        self.cart = AuthenticatedCart(self.request)

    def test_reset_cart(self):
        self.cart.add(self.product, quantity=2)
        self.assertEqual(len(self.cart), 2)

        self.cart.reset()
        self.assertEqual(len(self.cart), 0)


class UnimplementedCartTests(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.session = self.client.session
        self.cart = UnimplementedCart

    def test_get_cart_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.cart._get_cart(self.request)

    def test_reset_cart_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.cart.reset(self.request)

    def test_save_cart_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.cart.save(self.request)

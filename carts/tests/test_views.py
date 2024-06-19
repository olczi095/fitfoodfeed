from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.urls import reverse

from carts.cart import AnonymousCart, AuthenticatedCart
from carts.views import get_cart
from shop.models import Product

User = get_user_model()


class GetCartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10.0)

    def test_get_cart_authenticated_user(self):
        self.client.user = self.user
        cart = get_cart(self.client)
        self.assertIsInstance(cart, AuthenticatedCart)

    def test_get_cart_anonymous_user(self):
        self.client.user = AnonymousUser()
        cart = get_cart(self.client)
        self.assertIsInstance(cart, AnonymousCart)


class CartViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10.0)

    def test_cart_detail_view_anonymous_user(self):
        response = self.client.get(reverse('carts:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['cart'], AnonymousCart)
        self.assertTemplateUsed(response, 'carts/cart_detail.html')

    def test_cart_detail_view_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('carts:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['cart'], AuthenticatedCart)
        self.assertTemplateUsed(response, 'carts/cart_detail.html')

    def test_cart_add_view_default_quantity(self):
        response = self.client.post(
            reverse('carts:cart_add'), {'product_id': self.product.id, 'quantity': 2}
        )
        self.assertRedirects(response, reverse('carts:cart_detail'))

    def test_cart_add_view_custom_quantity(self):
        response = self.client.post(
            reverse('carts:cart_add'), {'product_id': self.product.id}, follow=True
        )
        quantity_of_items_in_cart = len(response.context['cart'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quantity_of_items_in_cart, 1)

    def test_cart_update_view_for_existing_item(self):
        self.client.post(reverse('carts:cart_add'), {'product_id': self.product.id}, follow=True)
        response = self.client.post(
            reverse('carts:cart_update'), {'product_id': self.product.id, 'quantity': 5}
        )
        self.assertRedirects(
            response=response, expected_url='/shop/cart/', status_code=302, target_status_code=200
        )

    def test_cart_update_view_for_non_existing_item(self):
        response = self.client.post(
            reverse('carts:cart_update'), {'product_id': self.product.id, 'quantity': 5}
        )
        self.assertEqual(response.status_code, 404)
        response = self.client.post(
            reverse('carts:cart_update'), {'product_id': self.product.id, 'quantity': 5},
            follow=True
        )

    def test_items_amount_after_updating_cart(self):
        self.client.post(reverse('carts:cart_add'), {'product_id': self.product.id}, follow=True)
        response = self.client.post(
            reverse('carts:cart_update'), {'product_id': self.product.id, 'quantity': 5},
            follow=True
        )
        quantity_of_items_in_cart = len(response.context['cart'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quantity_of_items_in_cart, 5)

    def test_cart_delete_view_for_existing_item(self):
        self.client.post(reverse('carts:cart_add'), {'product_id': self.product.id}, follow=True)
        response = self.client.post(
            reverse('carts:cart_delete'), {'product_id': self.product.id}, follow=True
        )
        quantity_of_items_in_cart = len(response.context['cart'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quantity_of_items_in_cart, 0)

    def test_cart_delete_view_for_non_existing_item(self):
        response = self.client.post(reverse('carts:cart_delete'), {'product_id': self.product.id})
        self.assertEqual(response.status_code, 404)

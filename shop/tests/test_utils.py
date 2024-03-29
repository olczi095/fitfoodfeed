from django.test import TestCase

from shop.models import Category, Product
from shop.utils import get_related_products


class GetRelatedProductsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product1 = Product.objects.create(
            name='Test Product 1', price=9.99, category=self.category, brand_name='Test Brand X'
        )
        self.product2 = Product.objects.create(
            name='Test Product 2', price=9.99, category=self.category, brand_name='Test Brand Y'
        )
        self.product3 = Product.objects.create(
            name='Test Product 3', price=9.99, category=self.category, brand_name='Test Brand Z'
        )
        self.product4 = Product.objects.create(
            name='Test Product 4', price=9.99, brand_name='Other Test Brand'
        )

    def get_related_products_returns_correct_related_products(self):
        related_products = get_related_products(product=self.product1, num_products=4)
        self.assertEqual(len(related_products), 2)
        self.assertIn(self.product2, related_products)
        self.assertIn(self.product3, related_products)

    def test_related_products_returns_no_duplicates(self):
        related_products = get_related_products(product=self.product1, num_products=4)
        self.assertEqual(len(related_products), len(set(related_products)))

    def test_get_related_products_returns_correct_products_number(self):
        related_products = get_related_products(product=self.product1, num_products=1)
        self.assertEqual(len(related_products), 1)

    def test_get_related_products_returns_empty_list_for_no_related_products(self):
        related_products = get_related_products(product=self.product4, num_products=4)
        self.assertEqual(len(related_products), 0)

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from shop.models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_slug_field(self):
        self.assertEqual(self.category.slug, 'test-category')

    def test_polish_slug_field(self):
        polish_category = Category.objects.create(
            name='Masła Orzechowe'
        )
        self.assertEqual(polish_category.slug, 'masla-orzechowe')

    def test_number_of_products_method(self):
        expected_number_of_products = 0
        self.assertEqual(self.category.number_of_products, expected_number_of_products)


class ProductModelTest(TestCase):
    def setUp(self):
        with open('shop/tests/files/test_image.jpg', 'rb') as f:
            content = f.read(0
                             )
        self.category = Category.objects.create(name='Test Category')
        self.category_2 = Category.objects.create(name='Test Category 2')
        self.product = Product.objects.create(
            name='Test Product',
            price=9.99,
            category=self.category,
            brand='Test Brand',
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=content,
                content_type='image/jpeg'
            )
        )
        self.product2 = None
        self.product3 = None
        self.product4 = None

    def test_string_representation(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_slug_field(self):
        self.assertEqual(self.product.slug, 'test-product')

    def test_polish_slug_field(self):
        with open('shop/tests/files/test_image.jpg', 'rb') as f:
            content = f.read()

        polish_product = Product.objects.create(
            name='Masło Orzechowe',
            price=9.99,
            brand='Test Brand',
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=content,
                content_type='image/jpeg'
            )
        )
        self.assertEqual(polish_product.slug, 'maslo-orzechowe')

    def test_get_absolute_url(self):
        product_absolute_url = '/shop/products/' + self.product.slug + '/'
        self.assertEqual(self.product.get_absolute_url(), product_absolute_url)

    def test_related_products_by_category(self):
        self.product2 = Product.objects.create(
            name='Test Product 2', price=9.99, category=self.category, brand='Test Brand'
        )
        self.product3 = Product.objects.create(
            name='Test Product 3', price=9.99, category=self.category, brand='Test Brand'
        )
        self.product4 = Product.objects.create(
            name='Test Product 4', price=9.99, brand='Test Brand'
        )

        related_products = self.product.related_products_by_category()
        self.assertEqual(related_products.count(), 2)
        self.assertIn(self.product2, related_products)
        self.assertIn(self.product3, related_products)
        self.assertNotIn(self.product4, related_products)

    def test_no_related_products_by_category(self):
        related_products = self.product.related_products_by_category()
        self.assertEqual(related_products.count(), 0)

    def test_related_products_by_brand(self):
        self.product2 = Product.objects.create(
            name='Test Product 2', price=9.99, category=self.category, brand='Test Brand'
        )
        self.product3 = Product.objects.create(
            name='Test Product 3', price=9.99, category=self.category, brand='Test Brand X'
        )
        self.product4 = Product.objects.create(
            name='Test Product 4', price=9.99, brand='Test Brand Y'
        )

        related_products = self.product.related_products_by_brand()
        self.assertEqual(related_products.count(), 1)
        self.assertIn(self.product2, related_products)
        self.assertNotIn(self.product3, related_products)
        self.assertNotIn(self.product4, related_products)

    def test_no_related_products_by_brand(self):
        related_products = self.product.related_products_by_brand()
        self.assertEqual(related_products.count(), 0)

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
        self.product = Product.objects.create(
            name='Test Product',
            price=9.99,
            brand_name='Test Brand',
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=content,
                content_type='image/jpeg'
            )
        )

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
            brand_name='Test Brand',
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=content,
                content_type='image/jpeg'
            )
        )
        self.assertEqual(polish_product.slug, 'maslo-orzechowe')

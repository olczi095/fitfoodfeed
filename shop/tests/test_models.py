from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from shop.models import Brand, Category, Product


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

    def test_get_absolute_url(self):
        category_absolute_url = '/shop/categories/' + self.category.slug + '/'
        self.assertEqual(self.category.get_absolute_url(), category_absolute_url)

    def test_number_of_products_method(self):
        expected_number_of_products = 0
        self.assertEqual(self.category.number_of_products, expected_number_of_products)


class BrandModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(
            name='Test Brand'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.brand), 'Test Brand')

    def test_polish_slug_field(self):
        polish_brand = Brand.objects.create(
            name='Kiełbasy Polskie'
        )
        self.assertEqual(polish_brand.slug, 'kielbasy-polskie')

    def test_get_absolute_url(self):
        brand_absolute_url = '/shop/brands/' + self.brand.slug + '/'
        self.assertEqual(self.brand.get_absolute_url(), brand_absolute_url)

    def test_number_of_products_method(self):
        expected_number_of_products = 0
        self.assertEqual(self.brand.number_of_products, expected_number_of_products)


class ProductModelTest(TestCase):
    def setUp(self):
        with open('shop/tests/files/test_image.jpg', 'rb') as f:
            content = f.read(0
                             )
        self.category = Category.objects.create(name='Test Category')
        self.category_2 = Category.objects.create(name='Test Category 2')
        self.brand_x = Brand.objects.create(name='Brand X')
        self.brand_y = Brand.objects.create(name='Brand Y')
        self.brand_z = Brand.objects.create(name='Brand Z')
        self.product = Product.objects.create(
            name='Test Product',
            price=9.99,
            category=self.category,
            brand=self.brand_x,
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
            brand=self.brand_x,
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
        product2 = Product.objects.create(
            name='Test Product 2', price=9.99, category=self.category, brand=self.brand_x
        )
        product3 = Product.objects.create(
            name='Test Product 3', price=9.99, category=self.category, brand=self.brand_x
        )
        product4 = Product.objects.create(
            name='Test Product 4', price=9.99, brand=self.brand_x
        )

        related_products = self.product.related_products_by_category()
        self.assertEqual(related_products.count(), 2)
        self.assertIn(product2, related_products)
        self.assertIn(product3, related_products)
        self.assertNotIn(product4, related_products)

    def test_no_related_products_by_category(self):
        related_products = self.product.related_products_by_category()
        self.assertEqual(related_products.count(), 0)

    def test_related_products_by_brand(self):
        product2 = Product.objects.create(
            name='Test Product 2', price=9.99, category=self.category, brand=self.brand_x
        )
        product3 = Product.objects.create(
            name='Test Product 3', price=9.99, category=self.category, brand=self.brand_y
        )
        product4 = Product.objects.create(
            name='Test Product 4', price=9.99, brand=self.brand_z
        )

        related_products = self.product.related_products_by_brand()
        self.assertEqual(related_products.count(), 1)
        self.assertIn(product2, related_products)
        self.assertNotIn(product3, related_products)
        self.assertNotIn(product4, related_products)

    def test_no_related_products_by_brand(self):
        related_products = self.product.related_products_by_brand()
        self.assertEqual(related_products.count(), 0)

    def test_is_new_true(self):
        self.assertTrue(self.product.is_new())

    def test_is_new_false(self):
        self.product.created_at = timezone.now() - timedelta(days=40)
        self.product.save()
        self.assertFalse(self.product.is_new())

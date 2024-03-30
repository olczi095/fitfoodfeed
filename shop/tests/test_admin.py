from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.html import strip_tags

from shop.admin import CategoryAdmin, ProductAdmin
from shop.models import Category, Product

User = get_user_model()


class CategoryAdminTest(TestCase):
    def setUp(self):
        self.category_model_admin = CategoryAdmin(model=Category, admin_site=AdminSite())

    def test_display_short_description_with_short_description(self):
        short_description = (
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry."
        )
        test_category = Category.objects.create(
            name='Test Category', description=short_description
        )
        self.assertEqual(
            self.category_model_admin.short_description(test_category), short_description
        )

    def test_display_short_description_with_long_description(self):
        long_description = (
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry."
            "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,"
            "when an unknown printer took a galley of type and scrambled it to make a type"
            "specimen book."
        )
        test_category = Category.objects.create(
            name='Test Category', description=long_description
        )
        self.assertEqual(
            self.category_model_admin.short_description(test_category),
            f"{long_description[:150]}..."
        )

    def test_display_short_description_field_display_without_description(self):
        test_category = Category.objects.create(
            name='Test Category'
        )
        self.assertEqual(self.category_model_admin.short_description(test_category), '')


class ProductAdminTest(TestCase):
    def setUp(self):
        self.product_model_admin = ProductAdmin(model=Product, admin_site=AdminSite())
        self.category = Category.objects.create(name='Test Category')

    def test_display_category_for_product_with_category(self):
        product = Product.objects.create(
            name='Test Product', category=self.category, price=9.99, brand_name='Test Brand'
        )
        category_model_display = self.product_model_admin.category_model(product)
        self.assertEqual(strip_tags(category_model_display), product.category.name)

    def test_display_category_for_product_without_category(self):
        product = Product.objects.create(
            name='Test Product 4', price=9.99, brand_name='Test Brand'
        )
        category_model_display = self.product_model_admin.category_model(product)
        self.assertEqual(category_model_display, None)

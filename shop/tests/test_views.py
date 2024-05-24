from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from shop.models import Brand, Category, Product


class ShopRedirectTest(TestCase):
    def test_shop_redirect_to_product_list(self):
        response = self.client.get(reverse('shop:shop_redirect'))
        self.assertRedirects(
            response=response,
            expected_url=reverse('shop:product_list'),
            status_code=302,
            target_status_code=200
        )


class ProductListTest(TestCase):
    def test_product_list_returns_200_response(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)


class CategoryProductListTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category'
        )
        self.brand = Brand.objects.create(
            name='Brand'
        )
        with open('shop/tests/files/test_image.jpg', 'rb') as f:
            content = f.read(0)
        self.product = Product.objects.create(
            name='Product',
            price=90.00,
            brand=self.brand,
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=content,
                content_type='image/jpeg'
            ),
            available=True
        )

    def test_category_product_list_returns_200_response(self):
        response = self.client.get(reverse('shop:category_product_list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.category, response.context['category'])

    def test_no_products_in_category_list(self):
        response = self.client.get(reverse('shop:category_product_list', args=[self.category.slug]))
        product_number = len(response.context['products'])
        self.assertEqual(product_number, 0)

    def test_one_product_in_category_list(self):
        self.product.category = self.category
        self.product.save()
        response = self.client.get(reverse('shop:category_product_list', args=[self.category.slug]))
        product_number = len(response.context['products'])
        self.assertEqual(product_number, 1)

    def test_category_does_not_exist(self):
        not_existing_slug = 'not-existing-slug'
        response = self.client.get(reverse('shop:category_product_list', args=[not_existing_slug]))
        self.assertRedirects(
            response=response,
            expected_url=reverse('shop:product_list'),
            status_code=302,
            target_status_code=200
        )

    def test_display_message_for_no_existing_category(self):
        not_existing_slug = 'not-existing-slug'
        response = self.client.get(
            reverse('shop:category_product_list', args=[not_existing_slug]), follow=True
        )
        message = list(response.context.get('messages'))[0]
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', message.tags)
        self.assertIn("category you were looking for not found", message.message)


class BrandProductListTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(
            name='Test Brand'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            available=True
        )

    def test_brand_product_list_returns_200_response(self):
        self.product.brand = self.brand
        self.product.save()
        response = self.client.get(reverse('shop:brand_product_list', args=[self.brand.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.brand, response.context['brand'])

    def test_no_products_in_brand_list_redirect(self):
        response = self.client.get(
            reverse('shop:brand_product_list', args=[self.brand.slug])
        )
        self.assertRedirects(
            response,
            expected_url=reverse('shop:product_list'),
            status_code=302,
            target_status_code=200
        )

    def test_no_products_in_brand_list_display_message(self):
        response = self.client.get(
            reverse('shop:brand_product_list', args=[self.brand.slug]), follow=True
        )
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertIn('we do not have any products from this brand', messages[0].message)

    def test_no_available_products_in_brand_list_display_message(self):
        self.product.available = False
        self.product.brand = self.brand
        self.product.save()
        response = self.client.get(
            reverse('shop:brand_product_list', args=[self.brand.slug]), follow=True
        )
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertIn('we do not have any available products from this brand', messages[0].message)

    def test_one_product_in_brand_list(self):
        self.product.brand = self.brand
        self.product.save()
        response = self.client.get(reverse('shop:brand_product_list', args=[self.brand.slug]))
        products_number = len(response.context['products'])
        self.assertEqual(products_number, 1)

    def test_brand_does_not_exist(self):
        wrong_slug = 'wrong-slug'
        response = self.client.get(reverse('shop:brand_product_list', args=[wrong_slug]))
        self.assertRedirects(
            response=response,
            expected_url=reverse('shop:product_list'),
            status_code=302,
            target_status_code=200
        )

    def test_display_message_for_no_existing_brand(self):
        wrong_slug = 'wrong-slug'
        response = self.client.get(
            reverse('shop:brand_product_list', args=[wrong_slug]), follow=True
        )
        message = list(response.context.get('messages'))[0]
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', message.tags)
        self.assertIn("brand you were looking for not found", message.message)


class ProductDetailTest(TestCase):
    def setUp(self):
        with open('shop/tests/files/test_image.jpg', 'rb') as f:
            content = f.read(0)
        self.category = Category.objects.create(
            name='Test Category'
        )
        self.brand = Brand.objects.create(
            name='Fake Brand'
        )
        self.product = Product.objects.create(
            name='Another Fake Product',
            price=19.99,
            brand=self.brand,
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=content,
                content_type='image/jpeg'
            ),
            available=True,
            quantity=10
        )

    def test_product_detail_returns_200_response(self):
        response = self.client.get(reverse('shop:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product, response.context['product'])

    def test_unavailable_product_with_category_in_product_detail(self):
        self.product.available = False
        self.product.category = self.category
        self.product.save()
        response = self.client.get(reverse('shop:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product, response.context['product'])

    def test_unavailable_product_without_category_in_product_detail(self):
        self.product.available = False
        self.product.save()
        response = self.client.get(reverse('shop:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product, response.context['product'])

    def test_display_message_for_unavailable_product_without_category_in_product_detail(self):
        self.product.available = False
        self.product.save()
        response = self.client.get(
            reverse('shop:product_detail', args=[self.product.slug]), follow=True
        )
        message = list(response.context.get('messages'))[0]
        self.assertEqual('error', message.tags)
        self.assertIn(
            "currently unavailable", message.message
        )

    def test_not_existing_product_in_product_detail(self):
        not_existing_slug = 'not-existing-slug'
        response = self.client.get(reverse('shop:product_detail', args=[not_existing_slug]))
        self.assertRedirects(
            response=response,
            expected_url=reverse('shop:product_list'),
            status_code=302,
            target_status_code=200
        )

    def test_display_message_for_not_existing_product_in_product_detail(self):
        not_existing_slug = 'not-existing-slug'
        response = self.client.get(
            reverse('shop:product_detail', args=[not_existing_slug]), follow=True
        )
        message = list(response.context.get('messages'))[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual('error', message.tags)
        self.assertIn("product you were looking for was not found", message.message)


class CategoriesListTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(
            name='Test Category 1'
        )
        self.category2 = Category.objects.create(
            name='Test Category'
        )

    def test_categories_list_returns_200_response(self):
        response = self.client.get(reverse('shop:category_list'))
        displayed_category_names = [category.name for category in response.context['categories']]
        expected_category_names = [category.name for category in Category.objects.all()]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(displayed_category_names, expected_category_names)
        self.assertTemplateUsed(response, 'shop/category_list.html')


class BrandListTest(TestCase):
    def setUp(self):
        self.brand1 = Brand.objects.create(
            name='Test Brand 1'
        )
        self.brand2 = Brand.objects.create(
            name='Test Brand 2'
        )

    def test_brand_list_returns_200_response(self):
        response = self.client.get(reverse('shop:brand_list'))
        displayed_brand_names = [brand.name for brand in response.context['brands']]
        expected_brand_names = [brand.name for brand in Brand.objects.all()]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(displayed_brand_names, expected_brand_names)
        self.assertTemplateUsed(response, 'shop/brand_list.html')


class ProductOnSaleListTest(TestCase):
    def test_product_on_sale_list_no_products_on_sale(self):
        response = self.client.get(reverse('shop:product_on_sale_list'))
        self.assertRedirects(
            response=response,
            expected_url=reverse('shop:product_list'),
            status_code=302,
            target_status_code=200
        )

    def test_display_message_no_products_on_sale(self):
        response = self.client.get(reverse('shop:product_on_sale_list'), follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', message.tags)
        self.assertIn('no products on sale', message.message)

    def test_product_on_sale_list_with_product_on_sale(self):
        Product.objects.create(
            name='Product',
            price=99.99,
            is_on_sale=True,
            sale_price=0.99
        )
        response = self.client.get(reverse('shop:product_on_sale_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/filtered_product_list.html')


class ProductNewListTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='old_product',
            price=19.99,
        )

    def test_product_new_list_no_new_products(self):
        self.product.created_at = timezone.now() - timedelta(days=40)
        self.product.save()
        response = self.client.get(reverse('shop:product_new_list'))
        self.assertRedirects(
            response=response,
            expected_url=reverse('shop:product_list'),
            status_code=302,
            target_status_code=200
        )

    def test_display_message_no_new_products(self):
        self.product.created_at = timezone.now() - timedelta(days=40)
        self.product.save()
        response = self.client.get(reverse('shop:product_new_list'), follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', message.tags)
        self.assertIn('no new products', message.message)

    def test_product_new_list_with_new_product(self):
        response = self.client.get(reverse('shop:product_new_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/filtered_product_list.html')

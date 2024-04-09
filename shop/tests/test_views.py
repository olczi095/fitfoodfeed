from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

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

    def test_no_available_product_in_category_list(self):
        self.product.available = False
        self.product.save()
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
            available=True
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
        self.assertRedirects(
            response=response,
            expected_url=reverse('shop:category_product_list', args=[self.category.slug]),
            status_code=302,
            target_status_code=200
        )

    def test_unavailable_product_without_category_in_product_detail(self):
        self.product.available = False
        self.product.save()
        response = self.client.get(reverse('shop:product_detail', args=[self.product.slug]))
        self.assertRedirects(
            response=response,
            expected_url=reverse('shop:product_list'),
            status_code=302,
            target_status_code=200
        )

    def test_display_message_for_unavailable_product_without_category_in_product_detail(self):
        self.product.available = False
        self.product.save()
        response = self.client.get(
            reverse('shop:product_detail', args=[self.product.slug]), follow=True
        )
        message = list(response.context.get('messages'))[0]
        self.assertEqual('error', message.tags)
        self.assertIn(
            "product you were looking for is not available at this moment", message.message
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
        self.assertIn("product you were looking for not found", message.message)


class CategoriesListTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(
            name='Test Category 1'
        )
        self.category2 = Category.objects.create(
            name='Test Category'
        )

    def test_categories_list_returns_200_response(self):
        response = self.client.get(reverse('shop:categories_list'))
        displayed_category_names = [category.name for category in response.context['categories']]
        expected_category_names = [category.name for category in Category.objects.all()]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(displayed_category_names, expected_category_names)
        self.assertTemplateUsed(response, 'shop/categories_list.html')

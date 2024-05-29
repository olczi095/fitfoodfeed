from django.test import TestCase

from comments.models import Publication
from shop.models import Product


class SignalsTestCase(TestCase):
    def setUp(self):
        self.publication = Publication.objects.create()
        self.product = Product.objects.create(
            name='test product',
            price=10.10,
            publication=self.publication
        )

    def test_delete_publication_with_product(self):
        self.assertIsNotNone(self.product.publication)
        self.product.delete()
        self.assertFalse(Publication.objects.filter(id=self.publication.id).exists())

from django.test import TestCase
from taggit.models import Tag


class TagSignalsTestCase(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(
            name='masła orzechowe'
        )
        self.tag2 = Tag.objects.create(
            name='odżywki białkowe'
        )

    def test_slug_generation(self):
        expected_slug1 = 'masla-orzechowe'
        expected_slug2 = 'odzywki-bialkowe'

        self.assertEqual(self.tag1.slug, expected_slug1)
        self.assertEqual(self.tag2.slug, expected_slug2)

    def test_slug_generation_after_changing_name(self):
        self.tag1.name = 'masełka proteinowe'
        expected_slug1 = 'maselka-proteinowe'

        self.tag1.save()

        self.assertEqual(self.tag1.slug, expected_slug1)

    def test_slug_generation_after_changing_slug_manually(self):
        correct_slug2 = self.tag2.slug

        self.tag2.slug = 'odżywki białkowe'
        self.tag2.save()
        wrong_slug2 = 'odżywki białkowe'

        self.assertNotEqual(self.tag2.slug, wrong_slug2)
        self.assertEqual(self.tag2.slug, correct_slug2)

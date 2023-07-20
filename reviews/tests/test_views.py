from django.test import TestCase
from reviews.models import Author, Post


class HomePageTestCase(TestCase):
    def test_home_page_returns_correct_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class HomePageContentTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(
            username='random',
            password='testpassword',
            bio='This is the random author for testing.'
        )

        self.post1 = Post.objects.create(
            title='Sample Post Review',
            slug='sample-post-review',
            author=self.author1,
            meta_description='This is a sample Post Review for testing.',
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )
        self.post2 = Post.objects.create(
            title='Another Sample Post Review',
            slug='another-post-review',
            author=self.author1,
            meta_description='This is an another sample Post Review for testing.',
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )

    def test_home_page_displays_added_posts(self):
        response = self.client.get('/')
        self.assertIn(self.post1, response.context['posts'])
        self.assertIn(self.post2, response.context['posts'])
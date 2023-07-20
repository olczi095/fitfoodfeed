from django.test import TestCase
from reviews.models import Author, Post


class HomePageTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(
            username='random',
            password='testpassword',
            bio='This is the random author for testing.'
        )

        self.post1 = Post.objects.create(
            title='Sample Post Review',
            slug='sample-post-review',
            pub_date = '2020-01-01',
            author=self.author1,
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )
        self.post2 = Post.objects.create(
            title='Another Sample Post Review',
            slug='another-post-review',
            pub_date = '2021-01-01',
            author=self.author1,
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )
        self.post3 = Post.objects.create(
            title='Again Another Sample Post Review',
            slug='once-more-post-review',
            pub_date = '2021-08-01',
            author=self.author1,
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )
        self.post4 = Post.objects.create(
            title='The last one',
            slug='the-last-test-post',
            pub_date = '2023-01-01',
            author=self.author1,
            body='Normally in this place I should have much longer text with the complete review for particular food product.',
            status='PUB'
        )

    def test_home_page_returns_correct_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_displays_added_posts(self):
        response = self.client.get('/')
        self.assertContains(response, self.post2.title)
        self.assertContains(response, self.post2.body)


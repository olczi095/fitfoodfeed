from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from reviews.models import User, Post


class HomePageTestCase(TestCase):
    def setUp(self):
        self.author1 = User.objects.create(
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

    def test_pagination_displays(self):
        response = self.client.get('/')
        self.assertEqual(response.context['is_paginated'], True)
        self.assertIn('paginator', response.context)

    
class PostDetailTestCase(TestCase):
    def setUp(self):
        self.author1 = User.objects.create(
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

    def test_post_detail_returns_correct_response(self):
        response = self.client.get(reverse('app_reviews:review', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_template_contains_body_and_title(self):
        response = self.client.get(reverse('app_reviews:review', kwargs={'slug': self.post1.slug}))
        self.assertContains(response, self.post1.body)
        self.assertContains(response, self.post1.title)


class PostCreateTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='random',
            password='testpassword',
            bio='This is the random author for testing.'
        )

    def test_unlogged_user_redirect_to_login(self):
        response = self.client.get(reverse('app_reviews:add_review'))
        self.assertEqual(response.status_code, 302)  
        expected_url = reverse('app_accounts:login') + '?next=' + reverse('app_reviews:add_review')
        self.assertRedirects(response, expected_url)

    
    def test_logged_user_without_permission_returns_403_page(self):
        self.client.login(username='random', password='testpassword')
        response = self.client.get(reverse_lazy('app_reviews:add_review'))
        self.assertEqual(response.status_code, 403)
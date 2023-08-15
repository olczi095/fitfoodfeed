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


class PostCreateWithPermissionTestCase(TestCase):
    def setUp(self):
        self.adminuser = User.objects.create_superuser(
            username='admin',
            password='admin-password'
        )
        self.client.login(username='admin', password='admin-password')

    def test_display_add_review_success(self):
        self.assertTrue(self.adminuser.has_perm('reviews.add_post'))
        response = self.client.get(reverse_lazy('app_reviews:add_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/post_add.html')

    def test_successful_post_creation_redirect(self):
        new_review = {
            'title': 'New Review',
            'body': 'The body of the new review',
            'status': 'PUB'
        }
        response = self.client.post(reverse_lazy('app_reviews:add_review'), data=new_review)
        expected_url_after_post = '/new-review/'  #slug created automatically based on 'New Review'
        self.assertRedirects(response, expected_url_after_post)

    def test_successful_post_adding_to_database(self):
        first_review = {
            'title': 'New Review',
            'body': 'The body of the new review',
            'status': 'PUB'
        }
        second_review = {
            'title': 'Second Review',
            'body': 'The body of the new review',
            'status': 'PUB'

        }
        self.client.post(reverse_lazy('app_reviews:add_review'), data=first_review)
        self.client.post(reverse_lazy('app_reviews:add_review'), data=second_review)

        posts_amount = len(Post.objects.all())
        self.assertEqual(posts_amount, 2)

        # Check if the author is assigned to the posts
        first_post = Post.objects.get(title='New Review')
        author_of_first_post = first_post.author
        self.assertEqual(author_of_first_post, self.adminuser)


class PostStatusTestCase(TestCase):
    def setUp(self):
        self.adminuser = User.objects.create_superuser(
            username='author',
            password='author-password'
        )
        self.client.login(username='author', password='author-password')

    def test_post_published_should_appear_on_homepage(self):
        self.post = Post.objects.create(
            title='The new review',
            body='This is the body of the new review.',
            status='PUB'
        )
        homepage = self.client.get(reverse('app_reviews:home'))
        self.assertContains(homepage, self.post)

    def test_post_to_publish_should_not_appear_on_homepage(self):
        self.post = Post.objects.create(
            title='The first to-publish review',
            body='This is the body of a two-publish review.',
            status='TO_PUB'
        )
        homepage = self.client.get(reverse('app_reviews:home'))
        self.assertNotContains(homepage, self.post)

    def test_post_to_publish_should_not_be_published(self):
        data = {
            'title': 'The second to-publish review',
            'body': 'This is the body of a second two-publish review.',
            'status': 'TO_PUB',
            'slug': 'the-second-to-publish-review'
        }
        response = self.client.post(reverse('app_reviews:add_review'), data)
        self.assertRedirects(response, '/') # Redirect to the homepage, not to the post_detail
        response = self.client.get(reverse('app_reviews:review', kwargs={'slug': data['slug']}))
        self.assertEqual(response.status_code, 404)

    def test_post_to_publish_create_and_save(self):
        data = {
            'title': 'The third to-publish review',
            'body': 'This is the body of a second two-publish review.',
            'status': 'TO_PUB',
        }
        self.client.post(reverse('app_reviews:add_review'), data)

        post_amount = Post.objects.count()
        self.assertEqual(post_amount, 1)


    def test_post_draft_should_not_appear_on_homepage(self):
        self.post = Post.objects.create(
            title='The first draft review',
            body='This is the body of a draft review.',
            status='DRAFT'
        )
        homepage = self.client.get(reverse('app_reviews:home'))
        self.assertNotContains(homepage, self.post)

    def test_post_draft_should_not_be_published(self):
        data = {
            'title': 'The second draft review',
            'body': 'This is the body of a second draft review.',
            'status': 'DRAFT',
            'slug': 'the-second-draft-review'
        }
        response = self.client.post(reverse('app_reviews:add_review'), data)
        self.assertRedirects(response, '/') # Redirect to the homepage, not to the post_detail
        response = self.client.get(reverse('app_reviews:review', kwargs={'slug': data['slug']}))
        self.assertEqual(response.status_code, 404)

    def test_post_draft_create_and_save(self):
        data = {
            'title': 'The third draft review',
            'body': 'This is the body of a third draft review.',
            'status': 'DRAFT',
        }
        self.client.post(reverse('app_reviews:add_review'), data)

        post_amount = Post.objects.count()
        self.assertEqual(post_amount, 1)
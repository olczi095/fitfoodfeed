from datetime import datetime
from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from reviews.models import Post, Model


class PostModelExistenceTestCase(TestCase):
    def test_post_model_exists(self):
        posts = Post.objects.all()
        self.assertEqual(posts.count(), 0)


class PostModelTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create(
            username='test_user',
            password='test_password'
        )
        self.post = Post.objects.create(
            title='test_title',
            slug='test_slug',
            pub_date=timezone.now().date(),
            author=self.author,
            body='test_body'
        )
        self.second_post = Post.objects.create(
            title='second_test_title',
            slug='second_test_slug',
            pub_date=datetime(2022, 7, 14).date(),
            author=self.author,
            body='second_test_body'
        )
    
    def test_author_post_fields(self):
        self.assertEqual(self.post.title, 'test_title')
        self.assertEqual(self.post.slug, 'test_slug')
        self.assertEqual(self.post.pub_date, timezone.now().date())
        self.assertEqual(self.post.author, self.author)
        self.assertEqual(self.post.meta_description, '')
        self.assertEqual(self.post.body, 'test_body')
        self.assertEqual(self.post.status, 'DRAFT')

    def test_status_choices(self):
        expected_status_choices = [
            ('DRAFT', 'Draft'),
            ('TO_PUB', 'Prepared to publish'),
            ('PUB', 'Published')
        ]
        official_status_choices = Post._meta.get_field('status').choices
        self.assertEqual(expected_status_choices, official_status_choices)

    def test_valid_status_returns_PUB(self):
        self.post.status = 'PUB'
        self.assertEqual(self.post.status, 'PUB')
        
    def test_invalid_status_returns_error(self):
        with self.assertRaises(ValidationError):
            self.post.status = 'INVALID_STATUS'
            self.post.full_clean()

    def test_ordering(self):
        expected_ordering = ['-pub_date']
        real_ordering = Post._meta.ordering
        self.assertEqual(expected_ordering, real_ordering)

    def test_ordering_with_two_posts_with_different_dates(self):
        expected_order = [self.post, self.second_post]
        actual_order = list(Post.objects.all())
        self.assertEqual(expected_order, actual_order)

    def test_string_representation(self):
        self.assertEqual(str(self.post), 'test_title')

    def test_create_slug_automatically_if_not_passed(self):
        self.review = Post.objects.create(
                title='Tytuł z polskimi znakami',
                author=self.author,
                body='Sprawdzamy jak zadziała automatyczne ustawienie slug.',
                status='PUB'
            )
        self.assertNotEqual(self.review.slug, '')

    def test_create_slug_automatically_recommended_approach(self):
        self.review = Post.objects.create(
                title='Tytuł z polskimi znakami!!!%',
                author=self.author,
                body='Sprawdzamy czy poprawnie przekonwertuje tytuł na slug.',
                status='PUB'
            )
        self.assertEqual(self.review.slug, 'tytul-z-polskimi-znakami')

    def test_get_absolute_url(self):
        post_absolute_url = '/test_slug/'
        self.assertEqual(self.post.get_absolute_url(), post_absolute_url)

    def test_post_model_has_image_field(self):
        self.assertTrue(Post._meta.get_field('image'))


class CategoryModelExistenceTestCase(TestCase):
    def test_category_model_exists(self):
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 0)
from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone

from reviews.models import Author, Post


class AuthorModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(username='test_user', 
                                            password='test_password',
                                            bio='test_bio')

    def test_bio_with_expected_value(self):
        self.assertEqual(self.author.bio, 'test_bio')

    def test_string_representation_with_username(self):
        self.assertEqual(str(self.author), 'test_user')

    def test_string_representation_without_username(self):
        anonymous = Author()
        self.assertEqual(str(anonymous), 'Anonymous')

    def test_image_field_with_default_image(self):
        self.assertIsNotNone(self.author.avatar)
        self.assertEqual(self.author.avatar.name, 'avatars/default-avatar.png')


class PostModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(username='test_user', password='test_password')
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
            pub_date='2022-07-14',
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
from datetime import datetime
from django.contrib.admin.sites import AdminSite
from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone
from reviews.admin import AuthorAdmin
from reviews.models import Author, Post


class AuthorModelExistenceTestCase(TestCase):
    def test_author_model_exists(self):
        authors = Author.objects.all()
        self.assertEqual(authors.count(), 0)

        
class AuthorModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            username='test_user', 
            password='test_password',
            bio='test_bio'
        )

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


class AuthorAdminModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            username='test_user', 
            password='test_password',
            bio='test_bio'
        )

    def test_display_author_on_admin_page(self):
        author_admin = AuthorAdmin(model=self.author, admin_site=AdminSite())
        displayed_author = author_admin.display_author(self.author)
        self.assertEqual(displayed_author, 'test_user')


class PostModelExistenceTestCase(TestCase):
    def test_post_model_exists(self):
        posts = Post.objects.all()
        self.assertEqual(posts.count(), 0)


class PostModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
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
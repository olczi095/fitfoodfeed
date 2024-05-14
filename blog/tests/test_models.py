from datetime import datetime

from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone

from blog.models import Category, Post
from comments.models import Comment

User = get_user_model()


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
        self.category = Category.objects.create(
            name='test_category'
        )
        self.post = Post.objects.create(
            title='test_title',
            slug='test_slug',
            pub_date=timezone.now().date(),
            author=self.author,
            body='test_body',
            category=self.category
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
        self.assertEqual(self.post.category.name, self.category.name)
        self.assertEqual(self.post.likes.count(), 0)

    def test_category_field(self):
        post_fields = [field.name for field in self.post._meta.get_fields()]
        category_field = 'category'
        self.assertIn(category_field, post_fields)

    def test_category_field_connected_with_category_model(self):
        category_field = Post._meta.get_field('category')
        self.assertEqual(category_field.related_model, Category)

    def test_category_default(self):
        default_category = 'Other'
        self.assertEqual(self.second_post.category.name, default_category)

    def test_status_choices(self):
        expected_status_choices = [
            ('DRAFT', 'Draft'),
            ('TO_PUB', 'Prepared to publish'),
            ('PUB', 'Published')
        ]
        official_status_choices = Post._meta.get_field('status').choices
        self.assertEqual(expected_status_choices, official_status_choices)

    def test_valid_status_returns_pub(self):
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

    def test_get_absolute_url(self):
        post_absolute_url = '/blog/test_slug/'
        self.assertEqual(self.post.get_absolute_url(), post_absolute_url)

    def test_post_model_has_image_field(self):
        self.assertTrue(Post._meta.get_field('image'))


class PostFunctionalityTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create(
            username='test_user',
            password='test_password'
        )
        self.category = Category.objects.create(
            name='test_category'
        )
        self.post = Post.objects.create(
            title='test_title',
            pub_date=timezone.now().date(),
            author=self.author,
            body='test_body',
            category=self.category
        )

    def test_comment_counter(self):
        amount_of_no_comments = self.post.comment_stats
        self.assertEqual(amount_of_no_comments, 0)

        comment = Comment.objects.create(
            post=self.post,
            body='Test comment.',
            active=True
        )
        comment.save()
        self.post.save()
        amount_of_comments = self.post.comment_stats
        self.assertEqual(amount_of_comments, 1)

    def test_likes_counter_with_no_likes(self):
        calculated_post_likes = self.post.likes_stats
        expected_likes = 0
        self.assertEqual(calculated_post_likes, expected_likes)

    def test_likes_counter_with_one_like(self):
        self.post.likes.add(self.author)
        calculated_post_likes = self.post.likes_stats
        expected_likes = 1
        self.assertEqual(calculated_post_likes, expected_likes)


class CategoryModelExistenceTestCase(TestCase):
    def test_category_model_exists(self):
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 0)


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='peanut butter'
        )
        self.assertTrue(self.category)

    def test_category_fields(self):
        expected_fields = {
            'name': 'Peanut Butter',
            'slug': 'peanut-butter'
        }
        self.assertEqual(self.category.name, expected_fields['name'])
        self.assertEqual(self.category.slug, expected_fields['slug'])

    def test_string_representation(self):
        expected_representation = self.category.name.title()
        self.assertEqual(str(self.category), expected_representation)

    def test_get_absolute_url(self):
        expected_category_absolute_url = '/blog/category/' + self.category.slug + '/'
        self.assertEqual(
            self.category.get_absolute_url(),
            expected_category_absolute_url
        )

from unittest.mock import Mock

from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.html import strip_tags
from taggit.models import Tag

from blog.admin import CategoryAdmin, PostAdmin
from blog.models import Category, Post

User = get_user_model()


class PostAdminTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Peanut Butter'
        )
        self.author = User.objects.create(
            username='test_user',
            password='test_password',
            is_staff=True,
        )
        self.review = Post.objects.create(
            title='My Review',
            author=self.author,
            body='This is the body of my test review.',
            category=self.category
        )
        self.another_review = Post(
            title='Another Review',
            author=self.author,
            body='This is the body of my another review.',
        )

        tag_chocolate = Tag.objects.create(name='chocolate')
        tag_bars = Tag.objects.create(name='bars')
        self.review.tags.add(tag_chocolate, tag_bars)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post_model_admin = PostAdmin(model=Post, admin_site=AdminSite())

    def test_likes_model_with_no_likes(self):
        calculated_review_likes = self.post_model_admin.likes_counter_model(self.review)
        expected_likes = 0
        self.assertEqual(calculated_review_likes, expected_likes)

    def test_likes_model_with_one_like(self):
        self.review.likes.add(self.author)
        calculated_review_likes = self.post_model_admin.likes_counter_model(self.review)
        expected_likes = 1
        self.assertEqual(calculated_review_likes, expected_likes)

    def test_get_queryset(self):
        queryset = self.post_model_admin.get_queryset(self.review)
        self.assertTrue(queryset.filter(tags__name='chocolate').exists())
        self.assertTrue(queryset.filter(tags__name='bars').exists())

    def test_tag_list(self):
        expected_tag_list = 'chocolate, bars'
        tag_list_html = self.post_model_admin.tag_list(self.review)
        tag_list_text = strip_tags(tag_list_html)
        self.assertEqual(expected_tag_list, tag_list_text)

    def test_assign_author_automatically_to_creating_post(self):
        request = Mock(user=self.author)
        self.post_model_admin.save_model(
            request, self.another_review,
            PostAdmin.form,
            change=False
        )
        new_review = Post.objects.get(pk=self.another_review.pk)
        self.assertEqual(new_review.author, self.author)

    def test_displaying_author(self):
        expected_author = self.review.author.username
        displayed_author = self.post_model_admin.author_model(self.review)
        displayed_author_without_url = strip_tags(displayed_author)
        self.assertEqual(expected_author, displayed_author_without_url)

    def test_displaying_category(self):
        expected_category = self.review.category.name
        displayed_category = self.post_model_admin.category_model(self.review)
        displayed_category_without_url = strip_tags(displayed_category)
        self.assertEqual(expected_category, displayed_category_without_url)


class CategoryAdminTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Peanut Butter'
        )
        self.post1 = Post.objects.create(
            title='Post 1',
            body='The body of Post 1',
            category=self.category,
            status='PUB'
        )
        self.post2 = Post.objects.create(
            title='Post 2',
            body='The body of Post 2',
            category=self.category,
            status='PUB'
        )
        self.post3 = Post.objects.create(
            title='Post 3',
            body='The body of Post 3',
            category=self.category,
            status='PUB'
        )

    def test_post_amount_for_category(self):
        category_model_admin = CategoryAdmin(model=Category, admin_site=AdminSite())
        post_amount = category_model_admin.post_amount(self.category)
        expected_post_amount = 3
        self.assertEqual(post_amount, expected_post_amount)

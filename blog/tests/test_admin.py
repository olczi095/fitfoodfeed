from unittest.mock import Mock

from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.utils.html import strip_tags
from taggit.models import Tag

from blog.admin import CategoryAdmin, CommentAdmin, PostAdmin
from blog.models import Category, Comment, Post

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
        self.assertTrue('tags' in queryset._prefetch_related_lookups)

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


class CommentAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='xyz',
            email='user@mail.com'
        )
        self.review = Post.objects.create(title='New review', body='The body.')
        self.user_comment = Comment.objects.create(
            logged_user=self.user,
            post=self.review,
            pub_datetime=timezone.now(),
            body='Comment written by logged user.'
        )
        self.random_comment = Comment.objects.create(
            post=self.review,
            pub_datetime=timezone.now(),
            body='Comment written by unlogged user.'
        )
        self.random_comment_with_email = Comment.objects.create(
            post=self.review,
            pub_datetime=timezone.now(),
            body='Comment written by unlogged user with email',
            email='random@mail.com'
        )
        self.comment_model_admin = CommentAdmin(model=Comment, admin_site=AdminSite())

    def test_displaying_author_with_logged_user(self):
        expected_author = self.user.username
        displayed_author = self.comment_model_admin.author(self.user_comment)
        displayed_author_without_url = strip_tags(displayed_author)
        self.assertEqual(expected_author, displayed_author_without_url)

    def test_displaying_email_with_logged_user(self):
        expected_email = self.user.email
        displayed_email = self.comment_model_admin.email(self.user_comment)
        self.assertEqual(expected_email, displayed_email)

    def test_displaying_author_with_unlogged_user(self):
        expected_author = 'guest'
        displayed_author = self.comment_model_admin.author(self.random_comment)
        self.assertEqual(expected_author, displayed_author)

    def test_displaying_author_email_with_unlogged_user_without_email(self):
        expected_no_email = None
        displayed_email_from_comment_without_email = (
            self.comment_model_admin.email(self.random_comment)
        )
        self.assertEqual(expected_no_email, displayed_email_from_comment_without_email)

    def test_displaying_author_email_with_unlogged_user_with_email(self):
        expected_email = self.random_comment_with_email.email
        displayed_email_from_comment_with_email = (
            self.comment_model_admin.email(self.random_comment_with_email)
        )
        self.assertEqual(expected_email, displayed_email_from_comment_with_email)

    def test_displaying_post_title(self):
        expected_title = self.random_comment.post.title
        displayed_title = self.comment_model_admin.post_title(self.random_comment)
        displayed_title_without_url = strip_tags(displayed_title)
        self.assertEqual(expected_title, displayed_title_without_url)

    def test_displaying_excerpt_of_comment(self):
        long_comment = Comment.objects.create(
            post=self.review,
            pub_datetime=timezone.now(),
            body='This is a very long comment, the longest from all comments. \
                This comment contains more than 75 signs.'
        )
        expected_comment = long_comment.body[:75]
        displayed_comment = self.comment_model_admin.comment(long_comment)
        self.assertEqual(expected_comment, displayed_comment)

    def test_formatting_datetime(self):
        expected_datetime = self.user_comment.pub_datetime.strftime("%Y-%m-%d %H:%M:%S")
        displayed_comment = self.comment_model_admin.datetime(self.user_comment)
        self.assertEqual(expected_datetime, displayed_comment)

    def test_title_of_datetime_column(self):
        expected_title = 'DATE / TIME'
        displayed_title = self.comment_model_admin.datetime.short_description
        self.assertEqual(expected_title, displayed_title)

    def test_save_comment_with_authenticated_user(self):
        self.comment_model_admin.save_model(
            request=None, obj=self.user_comment, form=None, change=False
        )
        self.assertIsNone(self.user_comment.unlogged_user)
        self.assertEqual(self.user_comment.logged_user, self.user)

    def test_get_fields_new_empty_form(self):
        base_fields = [
            'unlogged_user', 'logged_user', 'response_to',
            'email', 'post', 'body', 'active', 'level'
        ]
        self.assertEqual(
            list(self.comment_model_admin.get_fields(request=None)),
            base_fields
        )
        editable_fields = [
            'unlogged_user', 'logged_user', 'response_to',
            'email', 'post', 'body', 'active'
        ]
        self.assertEqual(
            list(self.comment_model_admin.get_form(request=None).base_fields),
            editable_fields
        )

    def test_get_fields_for_logged_user_comment(self):
        expected_fields = [
            'logged_user', 'response_to', 'email', 'post', 'body', 'active', 'level'
        ]
        actual_fields = self.comment_model_admin.get_fields(
            request=None,
            obj=self.user_comment
        )
        self.assertEqual(actual_fields, expected_fields)

    def test_get_fields_for_unlogged_user_comment(self):
        expected_fields = [
            'unlogged_user', 'response_to', 'email', 'post', 'body', 'active', 'level'
        ]
        actual_fields = self.comment_model_admin.get_fields(
            request=None,
            obj=self.random_comment
        )
        self.assertEqual(actual_fields, expected_fields)

    def test_get_readonly_fields_for_logged_user_comment(self):
        expected_readonly_fields = [
            'logged_user', 'unlogged_user', 'response_to', 'level'
        ]
        actual_readonly_fields = self.comment_model_admin.get_readonly_fields(
            request=None,
            obj=self.user_comment
        )
        self.assertEqual(actual_readonly_fields, expected_readonly_fields)

    def test_get_readonly_fields_for_unlogged_user_comment(self):
        expected_readonly_fields = [
            'logged_user', 'unlogged_user', 'response_to', 'level'
        ]
        actual_readonly_fields = self.comment_model_admin.get_readonly_fields(
            request=None,
            obj=self.random_comment
        )
        self.assertEqual(actual_readonly_fields, expected_readonly_fields)

    def test_get_changeform_initial_data(self):
        initial_data = self.comment_model_admin.get_changeform_initial_data(
            request=None
        )
        self.assertEqual(initial_data, {'unlogged_user': ''})

    def test_get_readonly_fields_for_responsed_comment(self):
        responsed_comment = Comment.objects.create(
            response_to=self.user_comment,
            post=self.review,
            body='The body of the responsed comment.'
        )
        expected_fields = [
            'logged_user', 'unlogged_user', 'response_to', 'post', 'level'
        ]
        actual_readonly_fields = self.comment_model_admin.get_readonly_fields(
            request=None,
            obj=responsed_comment
        )
        self.assertEqual(expected_fields, actual_readonly_fields)

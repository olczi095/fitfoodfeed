from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from model_bakery import baker

from blog.models import Post
from comments.admin import CommentAdmin, PublicationAdmin
from comments.models import Comment, Publication
from shop.models import Product

User = get_user_model()


class PublicationAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = PublicationAdmin(Publication, self.site)
        self.author = User.objects.create_superuser(
            username='admin',
            password='password'
        )
        self.publication = Publication.objects.create()
        self.post = Post.objects.create(
            title='test_title',
            author=self.author,
            body='test_body',
            status='PUB'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=999.99,
        )

    def test_publication_type_expected_none(self):
        pub_type = self.admin.publication_type(self.publication)
        self.assertEqual(pub_type, None)

    def test_publication_type_for_post(self):
        pub_type = self.admin.publication_type(self.post.publication)
        self.assertEqual(pub_type, 'post')

    def test_publication_type_for_product(self):
        pub_type = self.admin.publication_type(self.product.publication)
        self.assertEqual(pub_type, 'product')

    def test_publication_object_expected_none(self):
        pub_obj = self.admin.publication_object(self.publication)
        self.assertEqual(pub_obj, None)

    def test_publication_object_for_post(self):
        pub_obj = self.admin.publication_object(self.post.publication)
        expected_link = reverse('admin:blog_post_change', args=[self.post.pk])
        self.assertIn(expected_link, pub_obj)
        self.assertIn(str(self.post), pub_obj)

    def test_publication_object_for_product(self):
        pub_obj = self.admin.publication_object(self.product.publication)
        expected_link = reverse('admin:shop_product_change', args=[self.product.pk])
        self.assertIn(expected_link, pub_obj)
        self.assertIn(str(self.product), pub_obj)


class CommentAdminAuthorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='xyz',
            email='user@mail.com'
        )
        self.review = baker.make(Post)
        self.user_comment = Comment.objects.create(
            logged_user=self.user,
            publication=self.review.publication,
            pub_datetime=timezone.now(),
            body='Comment written by logged user.'
        )
        self.random_comment = Comment.objects.create(
            publication=self.review.publication,
            pub_datetime=timezone.now(),
            body='Comment written by unlogged user.'
        )
        self.random_comment_with_email = Comment.objects.create(
            publication=self.review.publication,
            pub_datetime=timezone.now(),
            body='Comment written by unlogged user with email',
            email='random@mail.com'
        )
        self.admin = CommentAdmin(model=Comment, admin_site=AdminSite())

    def test_displaying_author_with_logged_user(self):
        expected_author = self.user.username
        displayed_author = self.admin.author(self.user_comment)
        displayed_author_without_url = strip_tags(displayed_author)
        self.assertEqual(expected_author, displayed_author_without_url)

    def test_displaying_email_with_logged_user(self):
        expected_email = self.user.email
        displayed_email = self.admin.email(self.user_comment)
        self.assertEqual(expected_email, displayed_email)

    def test_displaying_author_with_unlogged_user(self):
        expected_author = 'guest'
        displayed_author = self.admin.author(self.random_comment)
        self.assertEqual(expected_author, displayed_author)

    def test_displaying_author_email_with_unlogged_user_without_email(self):
        expected_no_email = None
        displayed_email_from_comment_without_email = (
            self.admin.email(self.random_comment)
        )
        self.assertEqual(expected_no_email, displayed_email_from_comment_without_email)

    def test_displaying_author_email_with_unlogged_user_with_email(self):
        expected_email = self.random_comment_with_email.email
        displayed_email_from_comment_with_email = (
            self.admin.email(self.random_comment_with_email)
        )
        self.assertEqual(expected_email, displayed_email_from_comment_with_email)


class CommentAdminFieldsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='xyz',
            email='user@mail.com'
        )
        self.review = baker.make(Post)
        self.user_comment = Comment.objects.create(
            logged_user=self.user,
            publication=self.review.publication,
            pub_datetime=timezone.now(),
            body='Comment written by logged user.'
        )
        self.random_comment = Comment.objects.create(
            publication=self.review.publication,
            pub_datetime=timezone.now(),
            body='Comment written by unlogged user.'
        )
        self.admin = CommentAdmin(model=Comment, admin_site=AdminSite())

    def test_get_fields_new_empty_form(self):
        base_fields = [
            'unlogged_user', 'logged_user', 'response_to',
            'email', 'publication', 'body', 'active', 'level'
        ]
        self.assertEqual(
            list(self.admin.get_fields(request=None)),
            base_fields
        )
        editable_fields = [
            'unlogged_user', 'logged_user', 'response_to',
            'email', 'publication', 'body', 'active'
        ]
        self.assertEqual(
            list(self.admin.get_form(request=None).base_fields),
            editable_fields
        )

    def test_get_fields_for_logged_user_comment(self):
        expected_fields = [
            'logged_user', 'response_to', 'email', 'publication', 'body', 'active', 'level'
        ]
        actual_fields = self.admin.get_fields(
            request=None,
            obj=self.user_comment
        )
        self.assertEqual(actual_fields, expected_fields)

    def test_get_fields_for_unlogged_user_comment(self):
        expected_fields = [
            'unlogged_user', 'response_to', 'email', 'publication', 'body', 'active', 'level'
        ]
        actual_fields = self.admin.get_fields(
            request=None,
            obj=self.random_comment
        )
        self.assertEqual(actual_fields, expected_fields)

    def test_get_readonly_fields_for_logged_user_comment(self):
        expected_readonly_fields = [
            'logged_user', 'unlogged_user', 'response_to', 'level'
        ]
        actual_readonly_fields = self.admin.get_readonly_fields(
            request=None,
            obj=self.user_comment
        )
        self.assertEqual(actual_readonly_fields, expected_readonly_fields)

    def test_get_readonly_fields_for_unlogged_user_comment(self):
        expected_readonly_fields = [
            'logged_user', 'unlogged_user', 'response_to', 'level'
        ]
        actual_readonly_fields = self.admin.get_readonly_fields(
            request=None,
            obj=self.random_comment
        )
        self.assertEqual(actual_readonly_fields, expected_readonly_fields)

    def test_get_changeform_initial_data(self):
        initial_data = self.admin.get_changeform_initial_data(
            request=None
        )
        self.assertEqual(initial_data, {'unlogged_user': ''})

    def test_get_readonly_fields_for_responsed_comment(self):
        responsed_comment = Comment.objects.create(
            publication=self.review.publication,
            response_to=self.user_comment,
            body='The body of the responsed comment.'
        )
        expected_fields = [
            'logged_user', 'unlogged_user', 'response_to', 'publication', 'level'
        ]
        actual_readonly_fields = self.admin.get_readonly_fields(
            request=None,
            obj=responsed_comment
        )
        self.assertEqual(expected_fields, actual_readonly_fields)


class CommentAdminPublicationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='xyz',
            email='user@mail.com'
        )
        self.review = baker.make(Post)
        self.product = baker.make(Product)
        self.review_comment = Comment.objects.create(
            publication=self.review.publication,
            pub_datetime=timezone.now(),
            body='Comment written by unlogged user.'
        )
        self.product_comment = Comment.objects.create(
            publication=self.product.publication,
            pub_datetime=timezone.now(),
            body='Comment written by unlogged user.'
        )
        self.admin = CommentAdmin(model=Comment, admin_site=AdminSite())

    def test_publication_type_for_post_comment(self):
        pub_type = self.admin.publication_type(self.review_comment)
        self.assertEqual(pub_type, 'post')

    def test_publication_object_for_post_comment(self):
        pub_obj = self.admin.publication_object(self.review_comment)
        expected_link = reverse('admin:blog_post_change', args=[self.review.pk])
        self.assertIn(expected_link, pub_obj)
        self.assertIn(str(self.review), pub_obj)

    def test_publication_type_for_product_comment(self):
        pub_type = self.admin.publication_type(self.product_comment)
        self.assertEqual(pub_type, 'product')

    def test_publication_object_for_product_comment(self):
        pub_obj = self.admin.publication_object(self.product_comment)
        expected_link = reverse('admin:shop_product_change', args=[self.product.pk])
        self.assertIn(expected_link, pub_obj)
        self.assertIn(str(self.product), pub_obj)

    def test_publication_type_for_comment_expects_none(self):
        publication = Publication.objects.create()
        comment = Comment.objects.create(
            logged_user=self.user,
            publication=publication,
            body='Comment without post'
        )
        pub_type = self.admin.publication_type(comment)
        self.assertIsNone(pub_type)

    def test_publication_object_for_comment_expects_none(self):
        publication = Publication.objects.create()
        comment = Comment.objects.create(
            logged_user=self.user,
            publication=publication,
            body='Comment without post'
        )
        pub_obj = self.admin.publication_object(comment)
        self.assertIsNone(pub_obj)


class CommentAdminOtherTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='xyz',
            email='user@mail.com'
        )
        self.review = baker.make(Post)
        self.publication = Publication.objects.create()
        self.user_comment = Comment.objects.create(
            logged_user=self.user,
            publication=self.review.publication,
            pub_datetime=timezone.now(),
            body='Comment written by logged user.'
        )
        self.admin = CommentAdmin(model=Comment, admin_site=AdminSite())

    def test_formatting_datetime(self):
        expected_datetime = self.user_comment.pub_datetime.strftime("%Y-%m-%d %H:%M:%S")
        displayed_comment = self.admin.datetime(self.user_comment)
        self.assertEqual(expected_datetime, displayed_comment)

    def test_save_comment_with_authenticated_user(self):
        self.admin.save_model(
            request=None, obj=self.user_comment, form=None, change=False
        )
        self.assertIsNone(self.user_comment.unlogged_user)
        self.assertEqual(self.user_comment.logged_user, self.user)

    def test_comment_short_body(self):
        short_body = "x" * 10
        comment = Comment.objects.create(
            logged_user=self.user,
            publication=self.publication,
            body=short_body
        )
        self.assertEqual(self.admin.comment(comment), short_body)

    def test_comment_exactly_75_char_body(self):
        exact_body = "x" * 75
        comment = Comment.objects.create(
            logged_user=self.user,
            publication=self.publication,
            body=exact_body
        )
        self.assertEqual(self.admin.comment(comment), exact_body)

    def test_commment_long_body(self):
        long_body = "x" * 100
        comment = Comment.objects.create(
            logged_user=self.user,
            publication=self.publication,
            body=long_body
        )
        self.assertEqual(self.admin.comment(comment), long_body[:75])

from django.test import TestCase
from django.contrib.admin import AdminSite
from django.utils import timezone
from taggit.models import Tag
from accounts.models import User
from reviews.models import Post, Category, Comment
from reviews.admin import PostAdmin, CategoryAdmin, CommentAdmin
from unittest.mock import Mock


class PostAdminTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create(
            username='test_user',
            password='test_password',
            is_staff=True,
        )
        self.review = Post.objects.create(
            title='My Review',
            author=self.author,
            body='This is the body of my test review.',
        )
        
        tag_chocolate = Tag.objects.create(name='chocolate')
        tag_bars = Tag.objects.create(name='bars')
        self.review.tags.add(tag_chocolate, tag_bars)
        
    def test_get_queryset(self):
        postModelAdmin = PostAdmin(model=Post, admin_site=AdminSite())
        queryset = postModelAdmin.get_queryset(self.review)
        self.assertTrue('tags' in queryset._prefetch_related_lookups)

    def test_tag_list(self):
        postModelAdmin = PostAdmin(model=Post, admin_site=AdminSite())
        expected_tag_list = 'chocolate, bars'
        self.assertEqual(postModelAdmin.tag_list(self.review), expected_tag_list)

    def test_assign_author_automatically_to_creating_post(self):
        self.another_review = Post(
            title='Another Review',
            author=self.author,
            body='This is the body of my another review.',
        )
        postModelAdmin = PostAdmin(model=Post, admin_site=AdminSite())
        request = Mock(user=self.author)
        postModelAdmin.save_model(request, self.another_review, PostAdmin.form, change=False)
        new_review = Post.objects.get(pk=self.another_review.pk)
        self.assertEqual(new_review.author, self.author)


class CategoryAdminTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Peanut Butter'
        )
        self.post1 = Post.objects.create(
            title='Post 1',
            body='The body of Post 1',
            category=self.category
        )
        self.post2 = Post.objects.create(
            title='Post 2',
            body='The body of Post 2',
            category=self.category
        )
        self.post3 = Post.objects.create(
            title='Post 3',
            body='The body of Post 3',
            category=self.category
        )

    def test_post_count_for_category(self):
        categoryModelAdmin = CategoryAdmin(model=Category, admin_site=AdminSite())
        post_count = categoryModelAdmin.post_count(self.category)
        expected_post_count = 3 
        self.assertEqual(post_count, expected_post_count)


class CommentAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='xyz')
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

    def test_displaying_author_with_logged_user(self):
        comment_model_admin = CommentAdmin(model=Comment, admin_site=AdminSite())
        expected_author = self.user.username
        displayed_author = comment_model_admin.author(self.user_comment)
        self.assertEqual(expected_author, displayed_author)


    def test_displaying_author_with_unlogged_user(self):
        comment_model_admin = CommentAdmin(model=Comment, admin_site=AdminSite())
        expected_author = 'guest'
        displayed_author = comment_model_admin.author(self.random_comment)
        self.assertEqual(expected_author, displayed_author)

from django.test import TestCase
from django.contrib.admin import AdminSite
from taggit.models import Tag
from accounts.models import User
from reviews.models import Post
from reviews.admin import PostAdmin
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
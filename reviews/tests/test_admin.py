from django.test import TestCase
from django.contrib.admin import AdminSite
from taggit.models import Tag
from accounts.models import User
from reviews.models import Post
from reviews.admin import PostAdmin


class PostAdminTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create(
            username='test_user',
            password='test_password'
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
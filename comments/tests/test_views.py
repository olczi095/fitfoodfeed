from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Post
from comments.models import Comment

User = get_user_model()


class CommentDeleteViewTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', password='admin_password',
        )
        self.post = Post.objects.create(
            title='Sample Post Review',
            author=self.admin,
            body='The body of the Sample Post Review.',
            status='PUB',
        )
        self.comment_to_delete = Comment.objects.create(
            post=self.post,
            body='Body comment',
            active=True
        )

    def test_comment_delete_view(self):
        self.client.force_login(self.admin)
        delete_url = reverse(
            'comments:delete_comment', kwargs={'pk': self.comment_to_delete.id}
        )
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, 303)
        self.assertRaises(
            Comment.DoesNotExist,
            Comment.objects.get,
            pk=self.comment_to_delete.id
        )

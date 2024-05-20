from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from blog.models import Post
from comments.models import Comment

User = get_user_model()


class CommentDeleteViewTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', password='admin_password',
        )
        self.post = baker.make(Post)
        self.comment_to_delete = Comment.objects.create(
            body='Body comment',
            publication=self.post.publication,
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

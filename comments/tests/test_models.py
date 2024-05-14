from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.test import TestCase

from blog.models import Post
from comments.models import Comment

User = get_user_model()


class CommentModelExistenceTestCase(TestCase):
    def test_comment_model_exists(self):
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 0)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='xyz')
        self.review = Post.objects.create(title='New review', body='The body.')
        self.comment = Comment.objects.create(
            logged_user=self.user,
            post=self.review,
            body='First comment'
        )

    def test_comment_creation_by_logged_user(self):
        self.assertEqual(self.comment.logged_user, self.user)
        self.assertEqual(self.comment.post, self.review)
        self.assertTrue(self.comment.pub_datetime)
        self.assertEqual(self.comment.body, 'First comment')
        self.assertFalse(self.comment.active)

    def test_comment_creation_by_unlogged_user(self):
        self.comment.logged_user = None
        self.comment.active = True
        self.comment.save()
        self.assertEqual(self.comment.logged_user, None)
        self.assertEqual(self.comment.unlogged_user, 'guest')
        self.assertTrue(self.comment.active)

    def test_string_representation_logged_user(self):
        expected_representation = (
            f"Comment by {self.comment.logged_user} on {self.comment.post.title}."
        )
        self.assertEqual(str(self.comment), expected_representation)

    def test_string_representation_unlogged_user(self):
        comment = Comment.objects.create(post=self.review, body='Body of comment.')
        expected_representation = f"Comment by {comment.unlogged_user}" \
            f" on {comment.post.title}."
        self.assertEqual(str(comment), expected_representation)

    def test_superuser_comment_set_active_automatically(self):
        superuser = User.objects.create_superuser(
            username='superuser',
            password='superuser_password',
            email='superuser@mail.com'
        )
        comment = Comment.objects.create(
            logged_user=superuser,
            post=self.review,
            body='Body of comment'
        )
        self.assertTrue(comment.active)

    def test_comment_with_different_post_response_to_and_post_not_added(self):
        second_review = Post.objects.create(title='Second review', body='The body.')

        with self.assertRaises(ValidationError) as context:
            Comment.objects.create(
                response_to=self.comment,
                post=second_review,
                body='Response for the main comment.'
            )
        self.assertIn(
            'response_to and post must be associated with the same post',
            str(context.exception)
        )

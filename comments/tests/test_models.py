from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.test import TestCase
from model_bakery import baker

from blog.models import Post
from comments.models import Comment, Publication

User = get_user_model()


class PublicationModelTestCase(TestCase):
    def setUp(self):
        self.publication = Publication.objects.create()
        self.superuser = User.objects.create_superuser(username='superuser', password='xyz')
        self.post = Post.objects.create(
            title='Test Post',
            body='This is a test post.',
            author=self.superuser,
            status='PUB'
        )
        self.review = baker.make(Post)

    def test_string_representation_for_no_object(self):
        expected_representation = "None"
        self.assertEqual(str(self.publication), expected_representation)

    def test_string_representation_for_post(self):
        self.post.publication = self.publication
        expected_representation = f'Post: "{self.post}"'
        self.assertEqual(str(self.publication), expected_representation)

    def test_comment_stats_with_no_comments(self):
        comment_stats = self.publication.comment_stats
        self.assertEqual(comment_stats, 0)

    def test_get_recent_comments_for_other_publication_type_returns_none(self):
        recent_comments = self.publication.get_recent_comments(5, 'review')
        self.assertEqual(recent_comments, None)


class CommentModelExistenceTestCase(TestCase):
    def test_comment_model_exists(self):
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 0)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='xyz')
        self.review = baker.make(Post)
        self.comment = Comment.objects.create(
            logged_user=self.user,
            publication=self.review.publication,
            body='First comment'
        )

    def test_comment_creation_by_logged_user(self):
        self.assertEqual(self.comment.logged_user, self.user)
        self.assertEqual(self.comment.publication, self.review.publication)
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
            f"Comment by {self.comment.logged_user} on {self.comment.publication}."
        )
        self.assertEqual(str(self.comment), expected_representation)

    def test_string_representation_unlogged_user(self):
        comment = Comment.objects.create(
            publication=self.review.publication,
            body='Body of comment.'
        )
        expected_representation = f"Comment by {comment.unlogged_user}" \
            f" on {comment.publication}."
        self.assertEqual(str(comment), expected_representation)

    def test_superuser_comment_set_active_automatically(self):
        superuser = User.objects.create_superuser(
            username='superuser',
            password='superuser_password',
            email='superuser@mail.com'
        )
        comment = Comment.objects.create(
            logged_user=superuser,
            publication=self.review.publication,
            body='Body of comment'
        )
        self.assertTrue(comment.active)

    def test_comment_with_different_post_response_to_and_post_not_added(self):
        second_review = baker.make(Post)

        with self.assertRaises(ValidationError) as context:
            Comment.objects.create(
                response_to=self.comment,
                publication=second_review.publication,
                body='Response for the main comment.'
            )
        self.assertIn(
            'response_to and publication must be associated with the same publication',
            str(context.exception)
        )

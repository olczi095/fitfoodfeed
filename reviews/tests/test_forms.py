from django.test import TestCase
from reviews.forms import PostForm


class PostFormTestCase(TestCase):
    def test_post_form_exists(self):
        self.assertTrue(hasattr(PostForm, '__init__'))
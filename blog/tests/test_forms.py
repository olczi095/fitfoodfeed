from django.test import TestCase

from blog.forms import PostForm, ProductSubmissionForm


class PostFormTests(TestCase):
    def test_post_form_valid(self):
        valid_data = {
            'title': 'Lorem Ipsum',
            'body':
                'Lorem Ipsum is simply dummy text of the printing '
                'and typesetting industry. '
                'Lorem Ipsum has been the industry\'s standard dummy text '
                'ever since the 1500s, when an unknown printer took a galley of type '
                'and scrambled it to make a type specimen book.',
            'status': 'DRAFT'
        }
        post_form = PostForm(valid_data)
        is_valid_post_form = post_form.is_valid()
        self.assertTrue(is_valid_post_form)

    def test_post_form_invalid(self):
        invalid_data_without_title = {
            'body':
                'Lorem Ipsum is simply dummy text of the printing '
                'and typesetting industry. '
                'Lorem Ipsum has been the industry\'s standard dummy text '
                'ever since the 1500s, when an unknown printer took a galley '
                'of type and scrambled it to make a type specimen book.',
        }
        invalid_data_without_body = {
                'title': 'Lorem Ipsum'
            }
        is_valid_without_title = PostForm(invalid_data_without_title).is_valid()
        is_valid_without_body = PostForm(invalid_data_without_body).is_valid()
        self.assertFalse(is_valid_without_title)
        self.assertFalse(is_valid_without_body)


class ProductSubmissionFormTests(TestCase):
    def test_form_valid(self):
        valid_data = {
            'name': 'Test Product for review',
            'brand': 'Test Brand',
            'user_email': 'test_user@mail.com',
        }
        product_submission_form = ProductSubmissionForm(valid_data)
        self.assertTrue(product_submission_form.is_valid())

    def test_form_invalid_without_name(self):
        invalid_data = {
            'brand': 'Test Brand',
            'user_email': 'test_user@mail.com',
        }
        product_submission_form = ProductSubmissionForm(invalid_data)
        self.assertFalse(product_submission_form.is_valid())

    def test_form_invalid_without_brand(self):
        invalid_data = {
            'name': 'Test Product for review',
            'user_email': 'test_user@mail.com',
        }
        product_submission_form = ProductSubmissionForm(invalid_data)
        self.assertFalse(product_submission_form.is_valid())

    def test_form_invalid_without_email(self):
        invalid_data = {
            'name': 'Test Product for review',
            'brand': 'Test Brand',
        }
        product_submission_form = ProductSubmissionForm(invalid_data)
        self.assertFalse(product_submission_form.is_valid())

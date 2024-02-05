from django.test import TestCase

from reviews.forms import PostForm


class PostFormTestCase(TestCase):
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

    def test_labels(self):
        post_form = PostForm()
        expected_labels = {
            'title': 'Title',
            'meta_description': 'Meta Description',
            'tags': 'Tags',
            'body': 'Body',
            'image': 'Image',
            'slug': 'Slug',
            'status': 'Status',
        }
        for field_name, expected_label in expected_labels.items():
            self.assertEqual(post_form.fields.get(field_name).label, expected_label)

from unittest.mock import patch

from django.test import TestCase

from blog.templatetags.file_exists import file_exists


class TemplatetagsTestCase(TestCase):
    @patch('blog.templatetags.file_exists.os.path.isfile')
    def test_file_exists_filter_success(self, mock_isfile):
        mock_isfile.return_value = True
        result = file_exists('fake/file/path')
        self.assertTrue(result)

    def test_file_does_not_exist_filter(self):
        nonexistent_file_path = ''
        result = file_exists(nonexistent_file_path)
        self.assertFalse(result)

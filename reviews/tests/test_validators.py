from django.forms import ValidationError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from reviews.validators import (validate_avatar_type)
from PIL import Image
import io


class AvatarTypeValidatorTestCase(TestCase):
    def setUp(self):
        self.image = Image.new("RGB", (350, 350), (255, 255, 255))
        self.image_buffer = io.BytesIO()

    def test_image_with_invalid_data_returns_error(self):
        image_with_invalid_data = SimpleUploadedFile("test_image.jpg", b"invalid_image_data", content_type="image/jpeg")
        with self.assertRaises(ValidationError):
            validate_avatar_type(image_with_invalid_data)

    def test_image_with_valid_type_should_pass(self):
        self.image.save(self.image_buffer, "JPEG")
        image_data = self.image_buffer.getvalue()
        image_with_valid_type = SimpleUploadedFile("test_image.jpg", image_data, content_type="image/jpeg")
        self.assertEqual(validate_avatar_type(image_with_valid_type), None)

    def test_image_with_pdf_type_returns_error(self):
        self.image.save(self.image_buffer, "PDF")
        image_data = self.image_buffer.getvalue()
        image_with_invalid_type = SimpleUploadedFile("test_image.pdf", image_data, content_type="document/pdf")
        with self.assertRaises(ValidationError):
            validate_avatar_type(image_with_invalid_type)

    def test_image_with_gif_type_returns_error(self):
        self.image.save(self.image_buffer, "GIF")
        image_data = self.image_buffer.getvalue()
        image_with_invalid_type = SimpleUploadedFile("test_image.gif", image_data, content_type="image/gif")
        with self.assertRaises(ValidationError):
            validate_avatar_type(image_with_invalid_type)
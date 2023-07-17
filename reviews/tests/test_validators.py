import io
from PIL import Image

from django.forms import ValidationError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from reviews.validators import (validate_avatar_type, validate_avatar_dimensions)


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


class AvatarDimensionsValidatorTestCase(TestCase):
    def test_image_with_min_valid_dimensions(self):
        image = Image.new("RGB", (100, 100), (255, 255, 255))
        image_buffer = io.BytesIO()
        image.save(image_buffer, "JPEG")
        self.assertEqual(validate_avatar_dimensions(image), None)

    def test_image_with_max_valid_dimensions(self):
        image = Image.new("RGB", (500, 500), (255, 255, 255))
        image_buffer = io.BytesIO()
        image.save(image_buffer, "JPEG")
        self.assertEqual(validate_avatar_dimensions(image), None)

    def test_image_too_small_width_returns_error(self):
        image = Image.new("RGB", (50, 350), (255, 255, 255))
        image_buffer = io.BytesIO()
        image.save(image_buffer, "JPEG")
        self.assertRaises(ValidationError, validate_avatar_dimensions, image)

    def test_image_with_too_large_width_returns_error(self):
        image = Image.new("RGB", (600, 350), (255, 255, 255))
        image_buffer = io.BytesIO()
        image.save(image_buffer, "JPEG")
        self.assertRaises(ValidationError, validate_avatar_dimensions, image)

    def test_image_with_too_small_height_returns_error(self):
        image = Image.new("RGB", (350, 50), (255, 255, 255))
        image_buffer = io.BytesIO()
        image.save(image_buffer, "JPEG")
        self.assertRaises(ValidationError, validate_avatar_dimensions, image)

    def test_image_with_too_large_height_returns_error(self):
        image = Image.new("RGB", (350, 600), (255, 255, 255))
        image_buffer = io.BytesIO()
        image.save(image_buffer, "JPEG")
        self.assertRaises(ValidationError, validate_avatar_dimensions, image)
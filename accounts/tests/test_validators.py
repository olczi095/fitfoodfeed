import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import ValidationError
from django.test import TestCase
from PIL import Image

from accounts.validators import validate_avatar_dimensions, validate_avatar_type


class AvatarTypeValidatorTests(TestCase):
    def setUp(self):
        self.image = Image.new("RGB", (350, 350), (255, 255, 255))
        self.image_buffer = io.BytesIO()

    def test_image_with_invalid_data_returns_error(self):
        image_with_invalid_data = SimpleUploadedFile(
            "test_image.jpg",
            b"invalid_image_data",
            content_type="image/jpeg"
        )
        with self.assertRaises(ValidationError):
            validate_avatar_type(image_with_invalid_data)

    def test_image_with_valid_type_should_pass(self):
        self.image.save(self.image_buffer, "JPEG")
        image_data = self.image_buffer.getvalue()
        image_with_valid_type = SimpleUploadedFile(
            "test_image.jpg",
            image_data,
            content_type="image/jpeg"
        )
        self.assertEqual(validate_avatar_type(image_with_valid_type), None)

    def test_image_with_pdf_type_returns_error(self):
        self.image.save(self.image_buffer, "PDF")
        image_data = self.image_buffer.getvalue()
        image_with_invalid_type = SimpleUploadedFile(
            "test_image.pdf",
            image_data,
            content_type="document/pdf"
        )
        with self.assertRaises(ValidationError):
            validate_avatar_type(image_with_invalid_type)

    def test_image_with_gif_type_returns_error(self):
        self.image.save(self.image_buffer, "GIF")
        image_data = self.image_buffer.getvalue()
        image_with_invalid_type = SimpleUploadedFile(
            "test_image.gif",
            image_data,
            content_type="image/gif"
        )
        with self.assertRaises(ValidationError):
            validate_avatar_type(image_with_invalid_type)


class AvatarDimensionsValidatorTests(TestCase):
    def setUp(self):
        self.image = Image.new("RGB", (350, 350), (255, 255, 255))
        self.image_buffer = io.BytesIO()
        self.image.save(self.image_buffer, "JPEG")

    def test_image_with_valid_dimensions(self):
        self.assertEqual(validate_avatar_dimensions(self.image), None)

    def test_image_with_min_valid_dimensions(self):
        self.image = self.image.resize((100, 100))
        self.assertEqual(validate_avatar_dimensions(self.image), None)

    def test_image_with_max_valid_dimensions(self):
        self.image = self.image.resize((500, 500))
        self.assertEqual(validate_avatar_dimensions(self.image), None)

    def test_image_with_too_small_width_and_height_returns_error(self):
        self.image = self.image.resize((50, 50))
        with self.assertRaisesMessage(
            ValidationError,
            "Image height and width are too small."
        ):
            validate_avatar_dimensions(self.image)

    def test_image_with_too_small_width_and_too_large_height(self):
        self.image = self.image.resize((50, 600))
        with self.assertRaisesMessage(
            ValidationError,
            "Image width is too small and image height is too large."
        ):
            validate_avatar_dimensions(self.image)

    def test_image_with_too_small_width_returns_error(self):
        self.image = self.image.resize((50, 350))
        with self.assertRaisesMessage(
            ValidationError,
            "Image width is too small."
        ):
            validate_avatar_dimensions(self.image)

    def test_image_with_too_large_width_and_height_returns_error(self):
        self.image = self.image.resize((600, 600))
        with self.assertRaisesMessage(
            ValidationError,
            "Image height and width are too large."
        ):
            validate_avatar_dimensions(self.image)

    def test_image_with_too_large_width_and_too_small_height(self):
        self.image = self.image.resize((600, 50))
        with self.assertRaisesMessage(
            ValidationError,
            "Image width is too large and image height is too small."
        ):
            validate_avatar_dimensions(self.image)

    def test_image_with_too_large_width_returns_error(self):
        self.image = self.image.resize((600, 350))
        with self.assertRaisesMessage(
            ValidationError,
            "Image width is too large."
        ):
            validate_avatar_dimensions(self.image)

    def test_image_with_too_small_height_returns_error(self):
        self.image = self.image.resize((350, 50))
        with self.assertRaisesMessage(
            ValidationError,
            "Image height is too small."
        ):
            validate_avatar_dimensions(self.image)

    def test_image_with_too_large_height_returns_error(self):
        self.image = self.image.resize((350, 600))
        with self.assertRaisesMessage(
            ValidationError,
            "Image height is too large."
        ):
            validate_avatar_dimensions(self.image)

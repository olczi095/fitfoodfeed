from typing import Any

import magic
from django.core.exceptions import ValidationError


def validate_avatar_type(image: Any) -> None:
    """Validates if the avatar's image type is supported."""
    allowed_image_types: list[str] = ['image/png', 'image/jpeg']
    file_mime_type = magic.from_buffer(image.read(2048), mime=True)
    if file_mime_type not in allowed_image_types:
        raise ValidationError("Invalid image type.")


def validate_avatar_dimensions(image: Any) -> None:
    """Validates if the avatar's image dimensions are in the allowed range."""
    min_width, max_width = 100, 500
    min_height, max_height = 100, 500

    width, height = image.width, image.height

    if width < min_width and height < min_height:
        raise ValidationError(
            "Image height and width are too small."
        )
    if width < min_width and height > max_height:
        raise ValidationError(
            "Image width is too small and image height is too large."
        )
    if width < min_width:
        raise ValidationError(
            "Image width is too small."
        )
    if width > max_width and height > max_height:
        raise ValidationError(
            "Image height and width are too large."
        )
    if width > max_width and height < min_height:
        raise ValidationError(
            "Image width is too large and image height is too small."
        )
    if width > max_width:
        raise ValidationError(
            "Image width is too large."
        )
    if height < min_height:
        raise ValidationError(
            "Image height is too small."
        )
    if height > max_height:
        raise ValidationError(
            "Image height is too large."
        )

from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_avatar(image):
    min_width, max_width = 100, 500
    min_height, max_height = 100, 500
    max_size = 2 * 1024 * 1024

    width, height = image.width, image.height

    if width < min_width:
        if height < min_height:
            raise ValidationError(f"Image height and width are too small.")
        elif height > max_height:
            raise ValidationError(f"Image width is too small and image height is too large.")
        else:
            raise ValidationError(f"Image width is too small.")
    elif width > max_width:
        if height > min_height:
            raise ValidationError(f"Image height and width are too large.")
        elif height < max_height:
            raise ValidationError(f"Image width is too large and image height is too small.")
        else:
            raise ValidationError(f"Image width is too large.")
    elif height < min_height:
        raise ValidationError(f"Image height is too small.")
    elif height > max_height:
        raise ValidationError(f"Image height is too large.")
    
    if image.size > max_size:
        raise ValidationError(f"Image size is too big.")
        

avatar_extension_validator = FileExtensionValidator(['jpg', 'jpeg', 'png'])
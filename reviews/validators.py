from django.core.exceptions import ValidationError
import magic

def validate_avatar_type(image):
    allowed_image_types = ['image/png', 'image/jpeg']
    file_mime_type = magic.from_buffer(image.read(2048), mime=True)
    if file_mime_type not in allowed_image_types:
        raise ValidationError(f"Invalid image type.")
    
def validate_avatar_dimensions(image):
    min_width, max_width = 100, 500
    min_height, max_height = 100, 500

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
    
                                    
def validate_avatar_size(image):
    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError(f"Image size is too big.")
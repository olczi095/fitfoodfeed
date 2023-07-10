from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_file_type, validate_image_dimensions, validate_image_size


class Author(AbstractUser):
    bio = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='images/', 
                               blank=True,
                               validators=[validate_file_type, 
                                           validate_image_dimensions, 
                                           validate_image_size
                                           ])

    def __str__(self):
        return self.username
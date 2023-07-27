from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_avatar_type, validate_avatar_dimensions


class Author(AbstractUser):
    bio = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='avatars/', 
                               blank=True,
                               validators=[validate_avatar_type, 
                                           validate_avatar_dimensions
                                           ],
                               default='avatars/default-avatar.png'
                               )

    def __str__(self):
        if self.username:
            return self.username
        else:
            return 'Anonymous'
    
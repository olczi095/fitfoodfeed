from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_avatar, avatar_extension_validator


class Author(AbstractUser):
    bio = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='images/', 
                               null=True,
                               blank=True,
                               validators=[validate_avatar,
                                           avatar_extension_validator]
                               )

    def __str__(self):
        return self.username
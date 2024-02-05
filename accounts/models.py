from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_avatar_dimensions, validate_avatar_type


class User(AbstractUser):
    bio = models.CharField(
        max_length=150,
        blank=True
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[validate_avatar_type, validate_avatar_dimensions],
    )
    is_author = models.BooleanField(
        default=False,
        verbose_name='author status'
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    )

    def __str__(self) -> str:
        return str(self.username)

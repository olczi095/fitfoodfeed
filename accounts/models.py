from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_avatar_type, validate_avatar_dimensions


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'admin'
        AUTHOR = 'AUTHOR', 'author'
        USER = 'USER', 'user'

    bio = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=25, choices=Role.choices, default='user')
    avatar = models.ImageField(upload_to='avatars/', 
                               blank=True,
                               validators=[validate_avatar_type, 
                                           validate_avatar_dimensions
                                           ],
                               default='avatars/default-avatar.png'
                               )
    def __str__(self):
        return self.username
    

class Author(User):
    class Meta:
        proxy = True
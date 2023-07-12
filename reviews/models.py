from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .validators import validate_avatar_type, validate_avatar_dimensions, validate_avatar_size


class Author(AbstractUser):
    bio = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='avatars/', 
                               blank=True,
                               validators=[validate_avatar_type, 
                                           validate_avatar_dimensions, 
                                           validate_avatar_size],
                               default='avatars/default-avatar.png'
                               )

    def __str__(self):
        return self.username
    

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PREPARED_TO_PUBLISH = 'TO_PUB', 'Prepared to publish'
        PUBLISHED = 'PUB', 'Published'


    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    pub_date = models.DateField(default=timezone.now)
    author = models.ForeignKey(
        Author, 
        on_delete=models.SET_DEFAULT, 
        default='Anonymous',
        related_name='review_posts'
    )
    meta_description = models.CharField(max_length=150, blank=True)
    body = models.TextField()
    status = models.CharField(choices=Status.choices, max_length=50, default='DRAFT')


    class Meta:
        ordering = ['-pub_date']


    def __str__(self):
        return self.title

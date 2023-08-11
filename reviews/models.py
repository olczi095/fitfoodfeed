from django_resized import ResizedImageField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User
from accounts.validators import validate_avatar_type


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PREPARED_TO_PUBLISH = 'TO_PUB', 'Prepared to publish'
        PUBLISHED = 'PUB', 'Published'


    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    pub_date = models.DateField(default=timezone.now)
    image = ResizedImageField(
        size=[800, None],
        upload_to='review_images',
        validators=[validate_avatar_type],
        blank=True,
        null=True
        )
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_DEFAULT, 
        default=None,
        related_name='review_posts',
        null=True,
        blank=True
    )
    meta_description = models.CharField(max_length=150, blank=True)
    body = models.TextField()
    status = models.CharField(choices=Status.choices, max_length=50, default='DRAFT')


    class Meta:
        ordering = ['-pub_date']


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("app_reviews:review", args=[str(self.slug)])

    def save(self, *args, **kwargs):
        polish_signs_conversion = {
            'ą': 'a',
            'ć': 'c',
            'ę': 'e',
            'ł': 'l',
            'ń': 'n',
            'ó': 'o',
            'ś': 's',
            'ź': 'z',
            'ż': 'z'
        }
        if not self.slug:
            title_without_polish_signs = ''
            for sign in self.title:
                if sign in polish_signs_conversion.keys():
                    title_without_polish_signs += polish_signs_conversion[sign]
                else:
                    title_without_polish_signs += sign
            self.slug = slugify(title_without_polish_signs)
        super(Post, self).save(*args, **kwargs)
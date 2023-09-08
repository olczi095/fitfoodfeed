from django_resized import ResizedImageField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

from accounts.models import User
from accounts.validators import validate_avatar_type

def convert_to_slug(text):
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
        text_without_polish_signs = ''
        for sign in text:
            if sign in polish_signs_conversion.keys():
                text_without_polish_signs += polish_signs_conversion[sign]
            else:
                text_without_polish_signs += sign
        return slugify(text_without_polish_signs)


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=25, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = convert_to_slug(self.name)
        if self.name:
            self.name = self.name.title()
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("app_reviews:category", kwargs={"category_name": self.slug})
        

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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,          
        default=None,          
        null=True,          
        blank=True     
    )
    meta_description = models.CharField(max_length=150, blank=True)
    body = models.TextField()
    status = models.CharField(choices=Status.choices, max_length=50, default='DRAFT')
    tags = TaggableManager(
        blank=True, 
        help_text="A comma-separated list of tags (case-insensitive)."
    )


    class Meta:
        ordering = ['-pub_date']


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("app_reviews:detail_review", args=[str(self.slug)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = convert_to_slug(self.title)
        if not self.category:
            default_category, created = Category.objects.get_or_create(name='Other')
            self.category = default_category
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    logged_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    unlogged_user = models.CharField(max_length=50, blank=True, null=True, default='guest') 
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    pub_datetime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    active = models.BooleanField(default=False)


    class Meta:
        ordering = ['-pub_datetime']
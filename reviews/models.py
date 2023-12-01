from typing import Any

from django_resized import ResizedImageField
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

from accounts.validators import validate_avatar_type


User = get_user_model()

def convert_to_slug(text: str) -> str:
    """
    Converts polish signs into their ASCII substitutes,
    creates a valid slug from the input text.
    """
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
        if sign in polish_signs_conversion:
            text_without_polish_signs += polish_signs_conversion[sign]
        else:
            text_without_polish_signs += sign
    return slugify(text_without_polish_signs)


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=25, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name.title()

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = convert_to_slug(self.name)
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
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
    status = models.CharField(
        choices=Status.choices,
        max_length=50,
        default='DRAFT'
    )
    tags = TaggableManager(
        blank=True,
        help_text="A comma-separated list of tags (case-insensitive)."
    )
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("app_reviews:detail_review", args=[str(self.slug)])

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = convert_to_slug(self.title)
        if not self.category:
            default_category, _ = Category.objects.get_or_create(name='Other')
            self.category = default_category
        super().save(*args, **kwargs)

    def comment_counter(self) -> int:
        return self.comments.filter(active=True).count()

    def likes_counter(self) -> int:
        return self.likes.count()


class Comment(models.Model):
    logged_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    unlogged_user = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default='guest'
    )
    response_to = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    email = models.EmailField(null=True, blank=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='comments'
    )
    pub_datetime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    active = models.BooleanField(default=False)
    level = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(8)])

    @property
    def active_replies(self) -> QuerySet['Comment']:
        return self.replies.filter(active=True)

    class Meta:
        ordering = ['-pub_datetime']

    def __str__(self) -> str:
        if self.logged_user:
            return f"Comment by {self.logged_user} on {self.post.title}."
        return f"Comment by {self.unlogged_user} on {self.post.title}."

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Assigns email for logged-in users.
        Switch for active if comment is written by superuser.
        """
        if self.logged_user:
            self.email = self.logged_user.email

            if self.logged_user.is_superuser:
                self.active = True

        if self.response_to:
            self.level = self.response_to.level + 1

        return super().save(*args, **kwargs)
    
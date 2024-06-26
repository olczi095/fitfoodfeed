from typing import Any

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, QuerySet
from django.urls import reverse
from django.utils import timezone
from django_resized import ResizedImageField
from taggit.managers import TaggableManager

from accounts.models import \
    User as AccountsUser  # Importing User directly for type hints
from accounts.validators import validate_avatar_type
from comments.models import Publication
from utils.polish_slug_utils import convert_to_slug

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=25, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name.title()

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = convert_to_slug(self.name)
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("blog:category", kwargs={"category_slug": self.slug})

    def get_posts(self) -> QuerySet['Post']:
        return self.posts.filter(status='PUB')

    def get_posts_amount(self) -> int:
        return self.get_posts().count()


class TaggedPostsManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status='PUB')


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PREPARED_TO_PUBLISH = 'TO_PUB', 'Prepared to publish'
        PUBLISHED = 'PUB', 'Published'

    publication = models.OneToOneField(
        Publication,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
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
        blank=True,
        limit_choices_to=Q(is_author=True) | Q(is_superuser=True)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        blank=True,
        related_name='posts'
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
    likes: models.ManyToManyField = models.ManyToManyField(
        User, related_name='post_likes', blank=True
    )
    objects = models.Manager()
    tagged_posts = TaggedPostsManager()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.title

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.publication:
            publication = Publication.objects.create()
            self.publication = publication
        if not self.slug:
            self.slug = convert_to_slug(self.title)
        if not self.category:
            default_category, _ = Category.objects.get_or_create(name='Other')
            self.category = default_category
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("blog:detail_review", kwargs={"post_slug": self.slug})

    @property
    def likes_stats(self) -> int:
        return self.likes.count()

    def display_likes_stats(self) -> str:
        likes_stats = self.likes_stats
        likes_stats_display = '1 Like' if likes_stats == 1 else f'{likes_stats} Likes'
        return likes_stats_display

    @classmethod
    def get_tagged_posts(cls, tag_slug: str) -> QuerySet['Post']:
        return cls.tagged_posts.all().filter(tags__slug=tag_slug)

    @classmethod
    def get_popular_posts(cls, amount: int) -> list['Post']:
        posts_with_comment_counters = {}

        for post in cls.objects.filter(status='PUB'):
            if post.publication:
                posts_with_comment_counters[post] = post.publication.active_comments

        popular_posts_with_comment_counters = sorted(
            posts_with_comment_counters.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Get just posts without comment counters
        popular_posts = [
            popular_post[0] for popular_post
            in popular_posts_with_comment_counters
        ][:amount]

        return popular_posts

    def get_related_posts(self, amount: int) -> list['Post']:
        """
        Gets random posts that have the same tag
        as post in order to propose them to the user.
        """
        post_tags = self.tags.all()
        all_related_posts = list(
            Post.objects.filter(tags__in=post_tags).exclude(pk=self.pk).distinct()
        )
        return all_related_posts[:amount]

    def toggle_like(self, user: AccountsUser) -> bool:
        """
        Toggle like for the given user.
        """
        if self.likes.filter(pk=user.pk).exists():
            self.likes.remove(user)
            return False
        self.likes.add(user)
        return True

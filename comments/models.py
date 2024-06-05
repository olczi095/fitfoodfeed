from typing import Any

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Model, QuerySet

User = get_user_model()


class Publication(models.Model):
    def __str__(self):
        return f"{self.publication_type}"

    @property
    def publication_type(self):
        if getattr(self, 'post', None):
            return f"Post: \"{self.post}\""
        if getattr(self, 'product', None):
            return f"Product: \"{self.product}\""
        return None

    @property
    def active_comments(self) -> int:
        return self.comments.filter(active=True).count()

    @classmethod
    def get_recent_comments(cls, amount: int, publication_type: str) -> QuerySet['Comment'] | None:
        if publication_type == 'post':
            post_active_comments = Comment.objects.filter(
                active=True,
                publication__post__isnull=False
            ).order_by('-pub_datetime')[:amount]
            return post_active_comments
        if publication_type == 'product':
            product_active_comments = Comment.objects.filter(
                active=True,
                publication__product__isnull=False
            ).order_by('-pub_datetime')[:amount]
            return product_active_comments
        return None

    def get_top_level_comments(self) -> QuerySet['Model']:
        """
        Gets top level comments for the current publication.
        """
        return self.comments.filter(active=True).filter(response_to=None)


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
    publication = models.ForeignKey(
        Publication,
        blank=True,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_datetime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    active = models.BooleanField(default=False)
    level = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(8)])

    class Meta:
        ordering = ['-pub_datetime']

    def __str__(self) -> str:
        if self.logged_user:
            return f"Comment by {self.logged_user} on {self.publication}."
        return f"Comment by {self.unlogged_user} on {self.publication}."

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Assigns email for logged-in users.
        Switch for active if comment is written by superuser.
        """
        if self.logged_user:
            self.email = self.logged_user.email

            if self.logged_user.is_staff:
                self.active = True

        if self.response_to:
            self.level = self.response_to.level + 1

        if self.response_to and self.response_to.publication != self.publication:
            raise ValidationError(
                'Fields response_to and publication must be associated with the same publication.'
            )

        return super().save(*args, **kwargs)

    @property
    def active_replies(self) -> QuerySet['Comment']:
        return self.replies.filter(active=True)

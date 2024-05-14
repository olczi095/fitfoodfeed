from typing import Any

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import QuerySet

from blog.models import Post

User = get_user_model()


class CommentManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(active=True) \
            .order_by('-pub_datetime')


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
    objects = models.Manager()
    recent_comments = CommentManager()

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

            if self.logged_user.is_staff:
                self.active = True

        if self.response_to:
            self.level = self.response_to.level + 1

        if self.response_to and self.response_to.post != self.post:
            raise ValidationError(
                'Fields response_to and post must be associated with the same post.'
            )

        return super().save(*args, **kwargs)

    @property
    def active_replies(self) -> QuerySet['Comment']:
        return self.replies.filter(active=True)

    @classmethod
    def get_recent_comments(cls, amount: int) -> list['Comment']:
        return list(cls.recent_comments.all())[:amount]

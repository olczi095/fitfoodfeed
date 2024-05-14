from django.contrib import admin
from django.db.models import Model
from django.forms import ModelForm
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'comment',
        'active',
        'post_title',
        'email',
        'datetime',
        'pk'
    ]
    list_editable = ['active']
    list_display_links = ['comment']
    ordering = ['-pub_datetime', 'active']

    def get_fields(self, request: HttpRequest, obj: Model | None = None) -> list:
        if obj and isinstance(obj, Comment) and obj.logged_user:
            return [
                'logged_user', 'response_to', 'email', 'post', 'body', 'active', 'level'
                ]
        if obj and isinstance(obj, Comment) and \
                obj.unlogged_user:
            return [
                'unlogged_user', 'response_to', 'email',
                'post', 'body', 'active', 'level'
            ]

        return [
            'unlogged_user', 'logged_user', 'response_to',
            'email', 'post', 'body', 'active', 'level'
        ]

    def get_readonly_fields(
        self, request: HttpRequest, obj: Model | None = None
    ) -> list:
        if obj and isinstance(obj, Comment):
            fields = ['logged_user', 'unlogged_user', 'response_to', 'post', 'level']
            if obj.response_to is None:
                fields.remove('post')
            return fields
        return ['level']

    def author(self, obj: Comment) -> str | None:
        """
        Allows to redirect to the "user change" admin panel
        if the author is a registered user.
        """
        if obj.logged_user:
            logged_user_change_url = reverse(
                'admin:accounts_user_change',
                args=[obj.logged_user.pk]
            )
            return format_html(
                f'<a href="{logged_user_change_url}">{obj.logged_user}</a>'
            )
        return obj.unlogged_user

    def comment(self, obj: Comment) -> str:
        return obj.body[:75]

    @admin.display(description="POSTED IN")
    def post_title(self, obj: Comment) -> str:
        """Allows to redirect to the "post change" admin panel."""
        post_change_url = reverse('admin:blog_post_change', args=[obj.post.pk])
        return format_html(f'<a href="{post_change_url}">{obj.post.title}</a>')

    def email(self, obj: Comment) -> str | None:
        if obj.logged_user:
            return obj.logged_user.email
        return obj.email

    @admin.display(description="DATE / TIME")
    def datetime(self, obj: Comment) -> str:
        return obj.pub_datetime.strftime("%Y-%m-%d %H:%M:%S")

    def save_model(
        self, request: HttpRequest, obj: Model, form: ModelForm, change: bool
    ) -> None:
        if isinstance(obj, Comment) and obj.logged_user:
            obj.unlogged_user = None
        return super().save_model(request, obj, form, change)

    def get_changeform_initial_data(
        self, request: HttpRequest
    ) -> dict[str, str | list[str]]:
        return {'unlogged_user': ''}

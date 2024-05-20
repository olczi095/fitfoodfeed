from typing import Any

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Model, QuerySet
from django.forms import ModelForm
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Post

User = get_user_model()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'title',
        'author_model',
        'likes_counter_model',
        'category_model',
        'tag_list',
        'pub_date',
        'status'
    ]
    readonly_fields = ['publication']
    list_display_links = ['title']
    list_filter = ['author', 'category', 'status']
    search_fields = ['title', 'meta_description', 'body']
    prepopulated_fields = {'slug': ('title',)}

    @admin.display(description="author")
    def author_model(self, obj: Post) -> str:
        """Allows to redirect to the "user change" admin panel."""
        if obj.author:
            author_change_url = reverse(
                'admin:accounts_user_change',
                args=[obj.author.pk]
            )
        return format_html(f'<a href="{author_change_url}">{obj.author}</a>')

    @admin.display(description="likes")
    def likes_counter_model(self, obj: Post) -> Any:
        return obj.likes_stats

    @admin.display(description="category")
    def category_model(self, obj: Post) -> str | None:
        """Allows to redirect to the "category change" admin panel. """
        if obj.category:
            category_change_url = reverse(
                'admin:blog_category_change',
                args=[obj.category.pk]
            )
        return format_html(f'<a href="{category_change_url}">{obj.category}</a>')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Model]:
        """Optimizes query performance by prefetching related 'tags' data."""
        return super().get_queryset(request).prefetch_related('tags')

    @admin.display(description="tags")
    def tag_list(self, obj: Post) -> str:
        """Allows to redirect to the "taggit tag change" admin panel."""
        tags = obj.tags.all()
        tag_links = []

        for tag in tags:
            tag_change_url = reverse('admin:taggit_tag_change', args=[tag.pk])
            tag_links.append(format_html(f'<a href="{tag_change_url}">{tag.name}</a>'))

        return format_html(', '.join(tag_links))

    def save_model(
            self,
            request: HttpRequest,
            obj: Model,
            form: ModelForm,
            change: bool) -> None:

        if (
            isinstance(obj, Post)
            and obj.author is None
            and isinstance(request.user, User)
        ):
            obj.author = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_amount']
    list_filter = ['name']
    search_fields = ['name']

    def post_amount(self, obj: Category) -> int:
        return obj.get_posts_amount()

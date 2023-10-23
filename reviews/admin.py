from typing import Any, Protocol

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpRequest
from django.db.models import Model, QuerySet
from django.forms import ModelForm

from accounts.models import User
from .models import Post, Category, Comment


class AdminAttributes(Protocol):
    short_description: str

def admin_attr_decorator(func: Any) -> Any:
    """
    A decorator for admin attributes (type hints).
    """
    return func


@admin.register(Post)
class PostAdmin(admin.ModelAdmin[Model]):
    list_display = ['pk', 'title', 'author_model', 'likes_counter_model', 'category_model', 'tag_list', 'pub_date', 'status']
    list_display_links = ['title']
    list_filter = ['author', 'category', 'status']
    search_fields = ['title', 'meta_description', 'body']
    prepopulated_fields = {'slug': ('title',)}

    @admin_attr_decorator
    def author_model(self, obj: Post) -> str:
        """
        Allows to redirect to the "user change" admin panel from Post admin panel (using author name).
        """
        if obj.author:
            author_change_url = reverse('admin:accounts_user_change', args=[obj.author.pk])
        return format_html(f'<a href="{author_change_url}">{obj.author}</a>')
    
    @admin_attr_decorator 
    def likes_counter_model(self, obj: Post) -> Any:
        """
        Returns the amount of likes for the post.
        """
        return obj.likes_counter()
    
    @admin_attr_decorator
    def category_model(self, obj: Post) -> str:
        """
        Allows to redirect to the "category change" admin panel from Post admin panel (using category name).
        """
        if obj.category:
            category_change_url = reverse('admin:reviews_category_change', args=[obj.category.pk])
        return format_html(f'<a href="{category_change_url}">{obj.category}</a>')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Model]:
        """
        Uses prefetch_related('tags') to prefetch related 'tags' data and improve the optimization.
        """
        return super().get_queryset(request).prefetch_related('tags')
    
    @admin_attr_decorator
    def tag_list(self, obj: Post) -> str:
        """
        Allows to redirect to the "taggit tag change" admin panel from Post admin panel (using tag name).
        """
        tags = obj.tags.all()
        tag_links = []

        for tag in tags:
            tag_change_url = reverse('admin:taggit_tag_change', args=[tag.pk])
            tag_links.append(format_html(f'<a href="{tag_change_url}">{tag.name}</a>'))

        return format_html(', '.join(tag_links))
    
    def save_model(self, request: HttpRequest, obj: Model, form: ModelForm[Model], change: bool) -> None: 
        """
        During the saving process, the function sets the "request.user" as the post's author when the post's author field is currently None.
        """
        if isinstance(obj, Post) and obj.author is None and isinstance(request.user, User):
            obj.author = request.user
        return super().save_model(request, obj, form, change)

    author_model.short_description = 'author'
    likes_counter_model.short_description = 'likes'
    category_model.short_description = 'category'
    tag_list.short_description = 'tags'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin[Model]):
    list_display = ['name', 'slug', 'post_count']
    list_filter = ['name']
    search_fields = ['name']

    def post_count(self, obj: Category) -> int:
        """
        Returns the amount of posts belonging to the specified category.
        """
        return obj.post_set.count()
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin[Model]):
    list_display = ['author', 'comment', 'active', 'post_title', 'email', 'datetime']
    list_display_links = ['comment']
    ordering = ['active', 'pub_datetime']

    def author(self, obj: Comment) -> str | None:
        """
        Allows to redirect to the "user change" admin panel if the comment's author is a registered user.
        Otherwise, if the author is not a registered user, displays only the author's name without redirection.
        """
        if obj.logged_user:
            logged_user_change_url = reverse('admin:accounts_user_change', args=[obj.logged_user.pk])
            return format_html(f'<a href="{logged_user_change_url}">{obj.logged_user}</a>')
        else:
            return obj.unlogged_user
        
    def comment(self, obj: Comment) -> str:
        """
        Returns only first 75 signs from the comment body.
        """
        return obj.body[:75]
    
    @admin_attr_decorator
    def post_title(self, obj: Comment) -> str:
        """
        Allows to redirect to the "post change" admin panel from Post admin panel (using post title).
        """
        post_change_url = reverse('admin:reviews_post_change', args=[obj.post.pk])
        return format_html(f'<a href="{post_change_url}">{obj.post.title}</a>')
        
    def email(self, obj: Comment) -> str | None:
        """
        Returns the email associated with the registered user in database if the comment's author is a registered user.
        Otherwise, if the comment's author is not a registered user, returns the email associated with the specific comment.
        """
        if obj.logged_user:
            return obj.logged_user.email
        return obj.email
        
    @admin_attr_decorator
    def datetime(self, obj: Comment) -> str:
        """
        Converts the publication datetime of the comment to a formatted string.
        """
        return obj.pub_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    def save_model(self, request: HttpRequest, obj: Model, form: ModelForm[Comment], change: bool) -> None:  
        """
        During the saving process, sets the 'unlogged_user' field of the comment as None if the comment is written by a logged-in user.
        """
        if isinstance(obj, Comment) and obj.logged_user:
            obj.unlogged_user = None
        return super().save_model(request, obj, form, change)

    def get_form(self, request: HttpRequest, obj: Model | None = None, change: bool = False, **kwargs: Any) -> type[ModelForm[Model]]: 
        """
        Retrieves the form used for Comment administration.
        If comment is written by a logged-in user, the 'unlogged_user' field is not displaying in Comment admin form,
        if the comment's author is not a logged-in user, the 'unlogged_user' field is visible and editable.
        """ 
        if isinstance(obj, Comment):
            if obj.logged_user is not None:
                self.readonly_fields = ('unlogged_user',)
            else:
                self.readonly_fields = ()
        return super().get_form(request, obj, **kwargs)

    def get_changeform_initial_data(self, request: HttpRequest) -> dict[str, str | list[str]]:
        """
        Retrieves the initial data from the change form, setting the 'unlogged_user' field as an empty string by default.
        """
        return {'unlogged_user': ''}
    
    datetime.short_description = "DATE / TIME" 
    post_title.short_description = "POSTED IN"
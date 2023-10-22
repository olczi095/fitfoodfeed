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
        if obj.author:
            author_change_url = reverse('admin:accounts_user_change', args=[obj.author.pk])
        return format_html(f'<a href="{author_change_url}">{obj.author}</a>')
    
    @admin_attr_decorator 
    def likes_counter_model(self, obj: Post) -> Any:
        return obj.likes_counter()
    
    @admin_attr_decorator
    def category_model(self, obj: Post) -> str:
        if obj.category:
            category_change_url = reverse('admin:reviews_category_change', args=[obj.category.pk])
        return format_html(f'<a href="{category_change_url}">{obj.category}</a>')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Model]:
        return super().get_queryset(request).prefetch_related('tags')
    
    @admin_attr_decorator
    def tag_list(self, obj: Post) -> str:
        tags = obj.tags.all()
        tag_links = []

        for tag in tags:
            tag_change_url = reverse('admin:taggit_tag_change', args=[tag.pk])
            tag_links.append(format_html(f'<a href="{tag_change_url}">{tag.name}</a>'))

        return format_html(', '.join(tag_links))
    
    def save_model(self, request: HttpRequest, obj: Model, form: ModelForm[Model], change: bool) -> None: 
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
        return obj.post_set.count()
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin[Model]):
    list_display = ['author', 'comment', 'active', 'post_title', 'email', 'datetime']
    list_display_links = ['comment']
    ordering = ['active', 'pub_datetime']

    def author(self, obj: Comment) -> str | None:
        if obj.logged_user:
            logged_user_change_url = reverse('admin:accounts_user_change', args=[obj.logged_user.pk])
            return format_html(f'<a href="{logged_user_change_url}">{obj.logged_user}</a>')
        else:
            return obj.unlogged_user
        
    def comment(self, obj: Comment) -> str:
        return obj.body[:75]
    
    @admin_attr_decorator
    def post_title(self, obj: Comment) -> str:
        post_change_url = reverse('admin:reviews_post_change', args=[obj.post.pk])
        return format_html(f'<a href="{post_change_url}">{obj.post.title}</a>')
        
    def email(self, obj: Comment) -> str | None:
        if obj.logged_user:
            print(obj.logged_user)
            return obj.email
        return obj.email
        
    @admin_attr_decorator
    def datetime(self, obj: Comment) -> str:
        return obj.pub_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    def save_model(self, request: HttpRequest, obj: Model, form: ModelForm[Comment], change: bool) -> None:   
        if isinstance(obj, Comment) and obj.logged_user:
            obj.unlogged_user = None
        return super().save_model(request, obj, form, change)

    def get_form(self, request: HttpRequest, obj: Model | None = None, change: bool = False, **kwargs: Any) -> type[ModelForm[Model]]:  
        if isinstance(obj, Comment):
            if obj.logged_user is not None:
                self.readonly_fields = ('unlogged_user',)
            else:
                self.readonly_fields = ()
        return super().get_form(request, obj, **kwargs)

    
    def get_changeform_initial_data(self, request: HttpRequest) -> dict[str, str | list[str]]:
        return {'unlogged_user': ''}
    
    datetime.short_description = "DATE / TIME"
    post_title.short_description = "POSTED IN"
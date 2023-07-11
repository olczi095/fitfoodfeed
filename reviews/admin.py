from django.contrib import admin
from .models import Author, Post


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['display_author', 'email', 'bio']

    def display_author(self, obj):
        return obj.username

    display_author.short_description = 'Author'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'pub_date', 'status']
    list_filter = ['status', 'author']
    search_fields = ['title', 'meta_description', 'body']
    prepopulated_fields = {'slug': ('title',)}

    def display_author(self, obj):
        return obj.username

    display_author.short_description = 'Author'


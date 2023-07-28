from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'pub_date', 'status']
    list_filter = ['status', 'author']
    search_fields = ['title', 'meta_description', 'body']
    prepopulated_fields = {'slug': ('title',)}
from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['display_author', 'email', 'bio']

    def display_author(self, obj):
        return obj.username

    display_author.short_description = 'Author'

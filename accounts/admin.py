from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['display_user', 'email', 'bio']

    def display_user(self, obj):
        return obj.username

    display_user.short_description = 'User'
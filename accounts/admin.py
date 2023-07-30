from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['display_user', 'display_groups', 'email', 'bio']

    def display_user(self, obj):
        return obj.username
    
    def display_groups(self, obj):
        user_groups = [group.name for group in obj.groups.all()]
        return ', '.join(user_groups)

    display_groups.short_description = 'Role'
    display_user.short_description = 'User'
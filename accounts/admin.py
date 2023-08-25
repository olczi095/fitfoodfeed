from django.contrib import admin
from .models import User
from .forms import CustomUserCreationForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = CustomUserCreationForm
    list_display = ['display_user', 'display_groups', 'email', 'is_author', 'is_staff',]
    fieldsets = [
        (
            'Identification Data',
            {
                'fields': ['username', 'password1', 'password2', 'first_name', 'last_name', 'email'] 
            }
        ),
        (
            'Administration Properties',
            {
                'fields': ['is_active', 'is_superuser', 'is_staff', 'is_author']
            }
        ),
        (
            'Permission-related Fields',
            {
                'fields': ['groups', 'user_permissions']
            }
        ),
        (
            'Additional Information',
            {
                'fields': ['avatar', 'bio']
            }
        )
    ]

    def display_user(self, obj):
        return obj.username
    
    def display_groups(self, obj):
        user_groups = [group.name for group in obj.groups.all()]
        user_groups.sort()
        return ', '.join(user_groups)

    display_groups.short_description = 'Role'
    display_user.short_description = 'User'
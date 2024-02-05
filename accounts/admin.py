from typing import Any, Protocol

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User as AccountsUser  # Importing User directly for type hints

User = get_user_model()


def admin_attr_decorator(func: Any) -> Any:
    return func


class AdminAttributes(Protocol):
    short_description: str


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display: list[Any] = [
        'display_user',
        'display_groups',
        'email',
        'is_author',
        'is_staff',
    ]
    fieldsets: list[Any] = [
        (
            'Identification Data',
            {
                'fields': ['username', 'password', 'first_name', 'last_name', 'email']
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
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email"),
            },
        ),
    )

    @admin_attr_decorator
    def display_user(self, obj: AccountsUser) -> str:
        return obj.username

    @admin_attr_decorator
    def display_groups(self, obj: AccountsUser) -> str:
        user_groups = [group.name for group in obj.groups.all()]
        user_groups.sort()
        return ', '.join(user_groups)

    display_user.short_description = 'User'
    display_groups.short_description = 'Role'

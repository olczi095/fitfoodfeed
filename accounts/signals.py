from typing import Any

from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from reviews.models import Post


User = get_user_model()


@receiver(post_save, sender=User)
def add_to_admin_group(instance: User, **kwargs: Any) -> None:
    """
    Assigns the user to the 'admin' group if it is a superuser
    and not already in the group.
    """
    if instance.is_superuser \
        and not instance.groups.filter(name='admin').exists():
        admin_group, _ = Group.objects.get_or_create(name='admin')
        transaction.on_commit(lambda: instance.groups.add(admin_group))

@receiver(pre_save, sender=User)
def set_is_staff_for_superuser(instance: User, **kwargs: Any) -> None:
    if instance.is_superuser:
        instance.is_staff = True

@receiver(post_save, sender=User)
def add_add_and_view_post_permissions_to_author(
    instance: User, 
    **kwargs: Any
) -> None:
    """Adds 'add_post' and 'view_post' permissions to authors."""
    content_type = ContentType.objects.get_for_model(Post)
    add_post_permission = Permission.objects.get(
        codename='add_post',
        content_type=content_type
    )
    view_post_permission = Permission.objects.get(
        codename='view_post',
        content_type=content_type
    )
    if instance.is_author:
        instance.user_permissions.add(add_post_permission)
        instance.user_permissions.add(view_post_permission)
from django.db.models.signals import post_save, pre_save
from django.db import transaction
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from reviews.models import Post
from .models import User

@receiver(post_save, sender=User)
def add_to_admin_group(sender, instance, **kwargs):
    if instance.is_superuser and not instance.groups.filter(name='admin').exists():
        admin_group, created = Group.objects.get_or_create(name='admin')
        transaction.on_commit(lambda: instance.groups.add(admin_group))

@receiver(pre_save, sender=User)
def set_is_staff_for_superuser(sender, instance, **kwargs):
    if instance.is_superuser:
        instance.is_staff = True

@receiver(post_save, sender=User)
def add_add_and_view_post_permissions_to_author(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(Post)
    add_post_permission = Permission.objects.get(codename='add_post',
                                                content_type=content_type)
    view_post_permission = Permission.objects.get(codename='view_post',
                                                content_type=content_type)
    if instance.is_author:
        instance.user_permissions.add(add_post_permission)
        instance.user_permissions.add(view_post_permission)
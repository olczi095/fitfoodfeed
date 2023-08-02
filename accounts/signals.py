from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User

@receiver(post_save, sender=User)
def add_to_admin_group(sender, instance, **kwargs):
    admin_group, created = Group.objects.get_or_create(name='admin')
    if instance.is_superuser:
        instance.groups.add(admin_group)
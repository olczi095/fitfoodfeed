from django.db.models.signals import pre_save
from django.dispatch import receiver
from taggit.models import Tag

from .models import convert_to_slug


@receiver(pre_save, sender=Tag)
def convert_tag_to_slug(sender, instance, i=None, **kwargs):
    instance.slug = convert_to_slug(instance.name)

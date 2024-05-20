from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from taggit.models import Tag

from .models import Post, convert_to_slug


@receiver(pre_save, sender=Tag)
def convert_tag_to_slug(sender, instance, i=None, **kwargs):
    instance.slug = convert_to_slug(instance.name)

@receiver(post_delete, sender=Post)
def delete_publication_with_post(sender, instance, **kwargs):
    if instance.publication:
        instance.publication.delete()

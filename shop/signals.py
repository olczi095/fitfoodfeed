from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Product


@receiver(post_delete, sender=Product)
def delete_publication_with_product(sender, instance, **kwargs):
    if instance.publication:
        instance.publication.delete()

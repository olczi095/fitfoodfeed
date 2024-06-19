from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ShoppingUser(models.Model):
    user = models.OneToOneField(
        User, blank=False, null=False, on_delete=models.CASCADE, related_name='shoppinguser'
    )
    cart = models.JSONField(default=dict)

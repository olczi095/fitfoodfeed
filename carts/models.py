from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ShoppingUser(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    cart = models.JSONField(default=dict)

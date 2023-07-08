from django.db import models
from django.contrib.auth.models import AbstractUser


class Author(AbstractUser):
    bio = models.CharField(max_length=150)
    # avatar = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.username
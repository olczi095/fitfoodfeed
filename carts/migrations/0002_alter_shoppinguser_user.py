# Generated by Django 4.2.3 on 2024-06-17 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("carts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shoppinguser",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shoppinguser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

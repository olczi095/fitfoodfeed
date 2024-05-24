# Generated by Django 4.2.3 on 2024-05-17 15:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Publication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "unlogged_user",
                    models.CharField(
                        blank=True, default="guest", max_length=50, null=True
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("pub_datetime", models.DateTimeField(auto_now_add=True)),
                ("body", models.TextField()),
                ("active", models.BooleanField(default=False)),
                (
                    "level",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MaxValueValidator(8)],
                    ),
                ),
                (
                    "logged_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "publication",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="comments.publication",
                    ),
                ),
                (
                    "response_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="comments.comment",
                    ),
                ),
            ],
            options={
                "ordering": ["-pub_datetime"],
            },
        ),
    ]
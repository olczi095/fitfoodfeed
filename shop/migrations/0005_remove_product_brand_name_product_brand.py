# Generated by Django 4.2.3 on 2024-04-09 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_alter_product_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="brand_name",
        ),
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

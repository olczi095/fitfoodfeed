# Generated by Django 4.2.3 on 2024-03-21 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(upload_to="product_images/"),
        ),
    ]

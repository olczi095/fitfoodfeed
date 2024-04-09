# Generated by Django 4.2.3 on 2024-04-09 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_remove_product_brand_name_product_brand"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                ("description", models.TextField(blank=True)),
                (
                    "logo",
                    models.ImageField(blank=True, null=True, upload_to="brand_images/"),
                ),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="products",
                to="shop.brand",
            ),
        ),
    ]

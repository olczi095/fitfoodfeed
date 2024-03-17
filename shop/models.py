from typing import Any

from django.db import models

from utils.polish_slug_utils import convert_to_slug

# Catalog with products

class Category(models.Model):
    """Model representing the base category for various products."""

    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=25, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = convert_to_slug(self.name)
        return super().save(*args, **kwargs)

    @property
    def number_of_products(self) -> int:
        return self.products.count()


class Product(models.Model):
    """Model representing products in the product catalog."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    brief_description = models.CharField(max_length=255, null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    # Additional information
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    brand_name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to='product_images/',
        default='static/images/default_product_image.png'
    )
    available = models.BooleanField(default=True)
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = convert_to_slug(self.name)
        return super().save(*args, **kwargs)

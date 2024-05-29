from typing import Any

from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone

from comments.models import Publication
from utils.polish_slug_utils import convert_to_slug


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

    def get_absolute_url(self) -> str:
        return reverse("shop:category_product_list", kwargs={"category_slug": self.slug})

    @property
    def number_of_products(self) -> int:
        return self.products.count()


class Brand(models.Model):
    """Model representing a brand or manufacturer of products."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brand_images/', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = convert_to_slug(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("shop:brand_product_list", kwargs={"brand_slug": self.slug})

    @property
    def number_of_products(self):
        return self.products.count()


class Product(models.Model):
    """Model representing products in the product catalog."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    publication = models.OneToOneField(
        Publication,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
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
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    image = models.ImageField(
        upload_to='product_images/',
        null=True,
        blank=True
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
        if not self.publication:
            publication = Publication.objects.create()
            self.publication = publication
        if not self.slug:
            self.slug = convert_to_slug(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("shop:product_detail", kwargs={"product_slug": self.slug})

    def related_products_by_category(self) -> QuerySet:
        if self.category:
            return Product.objects.filter(category=self.category).exclude(id=self.id)
        return Product.objects.none()

    def related_products_by_brand(self) -> QuerySet:
        return Product.objects.filter(brand=self.brand).exclude(id=self.id)

    def is_new(self, number_of_days: int = 30) -> bool:
        """
        Check if product is new according to the passing number_of_days value.
        """
        current_date = timezone.now()
        created_date = self.created_at
        time_difference = current_date - created_date
        return time_difference.days <= number_of_days

from typing import Any

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Brand, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'name', 
        'short_description', 
        'number_of_products'
    ]
    list_display_links = ['name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description="category description")
    def short_description(self, obj:Category) -> str:
        return f"{obj.description[:150]}..." if len(obj.description) > 150 else f"{obj.description}"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'short_description',
        'number_of_products'
    ]
    list_display_links = ['name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    @admin.display(description='brand description')
    def short_description(self, obj: Brand) -> str:
        return f"{obj.description[:150]}..." if len(obj.description) > 150 else f"{obj.description}"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display: list[Any] = [
        'id',
        'name',
        'price',
        'quantity',
        'category_model',
        'available',
    ]
    list_display_links = ['name']
    list_filter = ['category', 'available']
    search_fields = ['name', 'brief_description', 'full_description', 'price']
    prepopulated_fields = {'slug': ('name', )}
    fieldsets: list[Any] = [
        (
            'Basic Information',
            {
                'fields': ['id', 'name', 'slug', 'brief_description', 'full_description']
            }
        ),
        (
            'Additional Information',
            {
                'fields': ['category', 'brand', 'image']
            }
        ),
        (
            'Price',
            {
                'fields': ['price', 'quantity', 'available', 'is_on_sale', 'sale_price']
            }
        ),
        (
            'Date Information',
            {
                'fields': ['created_at', 'updated_at']
            }
        )
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']

    @admin.display(description='category')
    def category_model(self, obj: Product) -> str | None:
        """Allows to redirect to the "product change" admin panel."""
        if obj.category:
            category_change_url = reverse(
                'admin:shop_category_change',
                args=[obj.category.pk]
            )
            return format_html(f'<a href="{category_change_url}">{obj.category.name}</a>')
        return None

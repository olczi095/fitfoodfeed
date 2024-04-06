from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Category


def product_categories(request: HttpRequest) -> dict[str, QuerySet[Category]]:
    """
    Returns a list of product categories that can be added to the template context.
    
    These categories are used in the online shop.
    """
    categories = Category.objects.all()
    return {'product_categories': categories}

def main_categories(request: HttpRequest) -> dict[str, QuerySet[Category]]:
    """
    Returns a list contains six main categories that can be added to the template context.
    """
    all_categories = Category.objects.all()
    sorted_categories = sorted(
        all_categories,
        key=lambda category: category.number_of_products,
        reverse=True
    )
    return {
        'main_categories': 
            all_categories.filter(pk__in=[category.pk for category in sorted_categories[:6]])
    }

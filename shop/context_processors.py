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

from django.http import HttpRequest
from django.db.models.query import QuerySet

from .models import Category


def categories(request: HttpRequest) -> dict[str, QuerySet[Category]]:
    """
    Returns a category list that can be added to the template context.
    """
    return {'categories': Category.objects.all()}
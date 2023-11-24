from django.http import HttpRequest
from django.db.models.query import QuerySet
from taggit.models import Tag

from .models import Category


def categories(request: HttpRequest) -> dict[str, QuerySet[Category]]:
    """
    Returns a category list that can be added to the template context.
    """
    return {'categories': Category.objects.all()}

def filter_existing_tags_for_navbar() -> list[str]:
    expected_tags = ['sweets', 'snacks', 'drinks', 'ready-to-eat']
    tags_qs = Tag.objects.filter(name__in=expected_tags)
    navbar_tags = list(tags_qs.values_list('name', flat=True))
    return navbar_tags

def navbar_tags(request: HttpRequest) -> dict[str, list[str]]:
    """
    Returns a tag list to include it in the lower_navbar template.
    """
    navbar_tags = filter_existing_tags_for_navbar()
    return {'navbar_tags': navbar_tags}
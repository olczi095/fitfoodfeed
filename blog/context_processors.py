from django.db.models.query import QuerySet
from django.http import HttpRequest
from taggit.models import Tag

from .models import Category


def categories(request: HttpRequest) -> dict[str, QuerySet[Category]]:
    """
    Returns a category list that can be added to the template context.
    """
    return {'categories': Category.objects.all()}

def main_categories_blog(request: HttpRequest) -> dict[str, QuerySet[Category]]:
    """
    Returns a list contains six main categories that can be added to the template context.
    """
    all_categories = Category.objects.all()
    sorted_categories = sorted(
        all_categories,
        key=lambda category: category.get_posts_amount(),
        reverse=True
    )
    return {
        'main_categories_blog': 
            all_categories.filter(pk__in=[category.pk for category in sorted_categories[:6]])
    }

def filter_existing_tags_for_navbar() -> list[str]:
    expected_tags = ['sweets', 'snacks', 'drinks', 'ready-to-eat']
    tags_qs = Tag.objects.filter(name__in=expected_tags)
    context_navbar_tags = list(tags_qs.values_list('name', flat=True))
    return context_navbar_tags


def navbar_tags(request: HttpRequest) -> dict[str, list[str]]:
    """
    Returns a tag list to include it in the lower_navbar template.
    """
    context_navbar_tags = filter_existing_tags_for_navbar()
    return {'navbar_tags': context_navbar_tags}

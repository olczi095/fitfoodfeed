from random import sample

from django.db.models import Q, QuerySet

from .models import Product


def get_related_products(product: Product, num_products: int) -> list[Product] | QuerySet[Product]:
    related_products_by_category = product.related_products_by_category()
    related_products_by_brand = product.related_products_by_brand()
    unique_related_products = (related_products_by_category | related_products_by_brand).distinct()
    if len(unique_related_products) > num_products:
        return sample(list(unique_related_products), k=num_products)
    return unique_related_products

def sort_products_to_display(products: QuerySet[Product]) -> list[Product]:
    products_available = products.filter(Q(available=True) & ~Q(quantity=0))
    products_not_available = products.filter(Q(available=False) | Q(quantity=0))
    sorted_products = list(products_available) + list(products_not_available)
    return sorted_products

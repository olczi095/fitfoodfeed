from random import sample

from django.db.models import QuerySet

from .models import Product


def get_related_products(product: Product, num_products: int) -> list[Product] | QuerySet[Product]:
    related_products_by_category = product.related_products_by_category()
    related_products_by_brand = product.related_products_by_brand()
    unique_related_products = (related_products_by_category | related_products_by_brand).distinct()
    if len(unique_related_products) > num_products:
        return sample(list(unique_related_products), k=num_products)
    return unique_related_products

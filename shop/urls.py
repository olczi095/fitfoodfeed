from django.urls import path

from .views import (categories_list, category_product_list, product_detail,
                    product_list, shop_redirect)

app_name = 'shop'

urlpatterns = [
    path('', shop_redirect, name='shop_redirect'),
    path('products/', product_list, name='product_list'),
    path('products/<str:product_slug>/', product_detail, name='product_detail'),
    path('categories/', categories_list, name='categories_list'),
    path('<str:category_slug>/', category_product_list, name='category_product_list'),
]

from django.urls import path

from .views import (ProductDetailView, brand_list, brand_product_list, category_list,
                    category_product_list, product_list, product_new_list,
                    product_on_sale_list, shop_redirect)

app_name = 'shop'

urlpatterns = [
    path('', shop_redirect, name='shop_redirect'),
    path('products/', product_list, name='product_list'),
    path('products/on_sale/', product_on_sale_list, name='product_on_sale_list'),
    path('products/new/', product_new_list, name='product_new_list'),
    path('products/<slug:product_slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('brands/', brand_list, name='brand_list'),
    path('brands/<slug:brand_slug>/', brand_product_list, name='brand_product_list'),
    path('categories/', category_list, name='category_list'),
    path('categories/<slug:category_slug>/', category_product_list, name='category_product_list'),
]

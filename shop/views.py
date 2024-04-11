from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import Brand, Category, Product
from .utils import get_related_products


def shop_redirect(request: HttpRequest) -> HttpResponseRedirect:
    return redirect('shop:product_list')

# Views related to products
def product_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.order_by('-available')
    return render(request, 'shop/product_list.html', {'products': products})

def product_on_sale_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.filter(is_on_sale=True).order_by('sale_price')
    if products:
        return render(
            request,
            'shop/filtered_product_list.html',
            {'sale': True, 'products': products}
        )
    messages.error(
        request, "Unfortunatelly, there are no products on sale."
    )
    return redirect('shop:product_list')

def product_detail(request: HttpRequest, product_slug: str) -> HttpResponse:
    try:
        product = Product.objects.get(slug=product_slug)

        if product.available is True:
            related_products = get_related_products(product=product, num_products=4)
            return render(
                request,
                'shop/product_detail.html', 
                {'product': product, 'related_products': related_products}
            )

        if product.category:
            messages.error(
                request,
                "Unfortunatelly, the product you were looking for is not available at this moment."
            )
            return redirect('shop:category_product_list', category_slug=product.category.slug)

        messages.error(
            request,
            "Unfortunatelly, the product you were looking for is not available at this moment."
        )
        return redirect('shop:product_list')

    except Product.DoesNotExist:
        messages.error(
            request, "Unfortunatelly, the product you were looking for not found."
        )
        return redirect('shop:product_list')

# Views related to categories
def category_list(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

def category_product_list(request: HttpRequest, category_slug: str) -> HttpResponse:
    try:
        category = Category.objects.get(slug=category_slug)
        products = category.products.order_by('-available')
        return render(
            request, 'shop/filtered_product_list.html', {'category': category, 'products': products}
        )

    except Category.DoesNotExist:
        messages.error(
            request, "Unfortunatelly, the category you were looking for not found."
        )
        return redirect('shop:product_list')

# Views related to brands
def brand_list(request: HttpRequest) -> HttpResponse:
    brands = Brand.objects.all()
    return render(request, 'shop/brand_list.html', {'brands': brands})

def brand_product_list(request: HttpRequest, brand_slug: str) -> HttpResponse:
    try:
        brand = Brand.objects.get(slug=brand_slug)
        products = brand.products.order_by('-available')
        return render(
            request, 'shop/filtered_product_list.html', {'brand': brand, 'products': products}
        )

    except Brand.DoesNotExist:
        messages.error(
            request, "Unfortunatelly, the brand you were looking for not found."
        )
        return redirect('shop:product_list')

from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import Category, Product


def shop_redirect(request: HttpRequest) -> HttpResponseRedirect:
    return redirect('shop:product_list')


def product_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.order_by('-available')
    return render(request, 'shop/product_list.html', {'products': products})


def category_product_list(request: HttpRequest, category_slug: str) -> HttpResponse:
    try:
        category = Category.objects.get(slug=category_slug)
        products = category.products.order_by('-available')
        return render(
            request, 'shop/category_product_list.html', {'category': category, 'products': products}
        )

    except Category.DoesNotExist:
        messages.error(
            request, "Unfortunatelly, the category you were looking for not found."
        )
        return redirect('shop:product_list')


def product_detail(request: HttpRequest, product_slug: str) -> HttpResponse:
    try:
        product = Product.objects.get(slug=product_slug)

        if product.available is True:
            return render(request, 'shop/product_detail.html', {'product': product})

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

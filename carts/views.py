from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product

from .cart import AnonymousCart, AuthenticatedCart


def get_cart(request):
    if request.user.is_authenticated:
        return AuthenticatedCart(request)
    return AnonymousCart(request)

def get_product_info(request):
    """Helper function to extract product_id and quantity from request."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    return {'product_id': product_id, 'quantity': quantity}

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'carts/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request):
    cart = get_cart(request)
    product_info = get_product_info(request)
    product = get_object_or_404(Product, id=product_info['product_id'])
    cart.add(product=product, quantity=product_info['quantity'])
    return redirect('carts:cart_detail')

@require_POST
def cart_update(request):
    cart = get_cart(request)
    product_info = get_product_info(request)
    product = get_object_or_404(Product, id=product_info['product_id'])

    try:
        cart.update(product=product, new_quantity=product_info['quantity'])
    except KeyError:
        return HttpResponseNotFound('Product not found in the cart.')

    return redirect('carts:cart_detail')

@require_POST
def cart_delete(request):
    cart = get_cart(request)
    product_info = get_product_info(request)
    product = get_object_or_404(Product, id=product_info['product_id'])

    try:
        cart.delete(product)
    except KeyError:
        return HttpResponseNotFound('Product not found in the cart.')

    return redirect('carts:cart_detail')

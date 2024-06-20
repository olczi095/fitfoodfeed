from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Product

from .cart import AnonymousCart, AuthenticatedCart


def get_cart(request):
    if request.user.is_authenticated:
        return AuthenticatedCart(request)
    return AnonymousCart(request)

def get_item_info(request):
    """Helper function to extract item id, type and quantity from request."""
    item_type = request.POST.get('item_type')
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    return {'type': item_type, 'id': item_id, 'quantity': quantity}

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'carts/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request):
    cart = get_cart(request)
    item_info = get_item_info(request)

    if item_info['type'] == 'product':
        product = get_object_or_404(Product, id=item_info['id'])
        cart.add(item=product, quantity=item_info['quantity'])

    return redirect('carts:cart_detail')


@require_POST
def cart_update(request):
    cart = get_cart(request)
    item_info = get_item_info(request)

    if item_info['type'] == 'product':
        product = get_object_or_404(Product, id=item_info['id'])
        try:
            cart.update(item=product, new_quantity=item_info['quantity'])
        except KeyError:
            return HttpResponseNotFound('Product not found in the cart.')

    return redirect('carts:cart_detail')

@require_POST
def cart_delete(request):
    cart = get_cart(request)
    item_info = get_item_info(request)

    if item_info['type'] == 'product':
        product = get_object_or_404(Product, id=item_info['id'])
        try:
            cart.delete(product)
        except KeyError:
            return HttpResponseNotFound('Product not found in the cart.')

    return redirect('carts:cart_detail')

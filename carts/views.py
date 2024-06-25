from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

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

    if not item_type:
        raise ValueError("Item type is required.")
    if not item_id:
        raise ValueError("Item ID is required.")

    return {'type': item_type, 'id': str(item_id), 'quantity': quantity}

def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'carts/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request):
    """This method can be extended with other models for other items."""
    cart = get_cart(request)
    item_info = get_item_info(request)

    if item_info['type'] == 'product':
        cart.add(item_id=item_info['id'], model_name='Product', quantity=item_info['quantity'])
    else:
        return HttpResponseNotFound('Invalid item type.')
    return redirect('carts:cart_detail')

@require_POST
def cart_update(request):
    cart = get_cart(request)
    item_info = get_item_info(request)

    if item_info['type'] == 'product':
        try:
            cart.update(
                item_id=item_info['id'], model_name='Product', new_quantity=item_info['quantity']
            )
        except KeyError:
            return HttpResponseNotFound('Product not found in the cart.')
    else:
        return HttpResponseNotFound('Invalid item type.')

    return redirect('carts:cart_detail')

@require_POST
def cart_delete(request):
    cart = get_cart(request)
    item_info = get_item_info(request)

    if item_info['type'] == 'product':
        try:
            cart.delete(item_id=item_info['id'], model_name='Product')
        except KeyError:
            return HttpResponseNotFound('Product not found in the cart.')
    else:
        return HttpResponseNotFound('Invalid item type.')

    return redirect('carts:cart_detail')

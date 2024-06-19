from django.urls import path

from .views import cart_add, cart_delete, cart_detail, cart_update

app_name = 'carts'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/', cart_add, name='cart_add'),
    path('update/', cart_update, name='cart_update'),
    path('delete/', cart_delete, name='cart_delete'),
]

from abc import ABC, abstractmethod
from typing import Any

from django.http import HttpRequest

from shop.models import Product

from .models import ShoppingUser


class BaseCart(ABC):
    """A fundamental basic Cart class for manipulating client cart."""

    def __init__(self, request: HttpRequest) -> None:
        """Initializes the cart with the given request."""
        self.session = request.session
        self.cart = self._get_cart()

    def __iter__(self):
        """Iterates over the items in the cart."""
        for item in self.cart.values():
            yield item

    def __len__(self) -> int:
        """Returns the total amount of all cart items."""
        return sum(item['quantity'] for item in self.cart.values())


    @abstractmethod
    def _get_cart(self) -> dict[str, Any]:
        """
        Retrieves the cart fot the current user.
        
        Returns:
            dict[str, Any]:
                A dictionary containing cart items and their quantities
        """
        raise NotImplementedError("Subclassess must implement this method.")

    @abstractmethod
    def reset(self) -> None:
        """Resets the cart."""
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def save(self) -> None:
        """Saves the current state of the cart."""
        raise NotImplementedError("Subclasses must implement this method.")

    def add(self, product: Product, quantity: int = 1) -> None:
        """Adds a new product to the cart."""
        product_id = str(product.id)
        cart_item = self.cart.get(product_id)

        if cart_item:
            cart_item['quantity'] += quantity
        else:
            self.cart[product_id] = {
                "name": product.name,
                "quantity": quantity,
                "price": float(product.price)
            }
        self.save()

    def update(self, product: Product, new_quantity: int) -> None:
        """
        Updates the quantity of a product in the cart.
        It happens when client for example select other quantity in a form.
        """

        if new_quantity < 0:
            raise ValueError("Quantity must be grater than zero.")

        product_id = str(product.id)

        if product_id in self.cart:
            if new_quantity == 0:
                self.delete(product)
            else:
                self.cart[product_id]['quantity'] = new_quantity
                self.save()
        else:
            raise KeyError("Product not found in the cart.")

    def delete(self, product: Product) -> None:
        """Deletes a product from the cart if it is contained."""
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
        else:
            raise KeyError("Product not found in the cart.")


    def get_total_price(self) -> float:
        """Calculates the total price of all items in the cart."""
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())


class AnonymousCart(BaseCart):
    """Cart class for anonymous users."""

    def _get_cart(self) -> dict[str, Any]:
        """Retrieves the cart from the session."""
        if 'cart' not in self.session:
            self.session['cart'] = {}
        return self.session['cart']

    def reset(self) -> None:
        """Resets the cart in the current session."""
        del self.session['cart']

    def save(self) -> None:
        """Saves the cart to the session."""
        self.session['cart'] = self.cart
        self.session.modified = True


class AuthenticatedCart(BaseCart):
    """Cart class for authenticated users."""

    def __init__(self, request: HttpRequest) -> None:
        self.user = request.user
        super().__init__(request)

    def _get_cart(self) -> dict[str, Any]:
        """Retrieves the cart from the database."""
        shopping_user, _ = ShoppingUser.objects.get_or_create(user=self.user)
        return shopping_user.cart

    def reset(self) -> None:
        """Clear the cart."""
        self.cart.clear()
        self.save()

    def save(self) -> None:
        """Saves the cart to the database."""
        shopping_user, _ = ShoppingUser.objects.get_or_create(user=self.user)
        shopping_user.cart = self.cart
        shopping_user.save()

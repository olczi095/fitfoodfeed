from typing import Any, Dict

from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.html import format_html
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from comments.forms import CommentForm
from comments.views import CommentSubmissionMixin

from .models import Brand, Category, Product
from .utils import get_related_products, sort_products_to_display


def shop_redirect(request: HttpRequest) -> HttpResponseRedirect:
    return redirect('shop:product_list')

# Views related to products
def product_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    products_sorted = sort_products_to_display(products)
    return render(request, 'shop/product_list.html', {'products': products_sorted})

def product_on_sale_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.filter(is_on_sale=True).order_by('sale_price')
    if products:
        products_sorted = sort_products_to_display(products)
        return render(
            request,
            'shop/filtered_product_list.html',
            {'sale': True, 'products': products_sorted}
        )
    messages.error(
        request, "Unfortunately, there are no products on sale."
    )
    return redirect('shop:product_list')

def product_new_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    products_sorted = sort_products_to_display(products)
    new_products_sorted = [product for product in products_sorted if product.is_new()]
    if new_products_sorted:
        return render(
            request,
            'shop/filtered_product_list.html',
            {'new': True, 'products': new_products_sorted}
        )
    messages.error(
        request, "Unfortunately, there are no new products in store at this moment."
    )
    return redirect('shop:product_list')


class ProductDetailView(CommentSubmissionMixin, FormMixin, DetailView):
    form_class = CommentForm
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = 'shop/product_detail.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            product = self.get_object()
            if not product.available or product.quantity == 0:
                messages.error(
                        self.request,
                        format_html(
                            "Unfortunately, the product you were looking for"
                            " is <strong>currently unavailable in the store</strong>. "
                            "You can view it, but you can't buy it at this moment."
                        )
                )
            return super().get(request, *args, **kwargs)
        except Http404:
            messages.error(
                self.request,
                "Unfortunately, the product you were looking for was not found."
            )
            return redirect('shop:product_list')

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if self.object.publication:
            context['comments'] = self.object.publication.get_top_level_comments()

        context['form'] = CommentForm(initial={'publication': self.object.publication})
        context['user'] = self.request.user
        context['related_products'] = get_related_products(product=self.object, num_products=4)
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

# Views related to categories
def category_list(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

def category_product_list(request: HttpRequest, category_slug: str) -> HttpResponse:
    try:
        category = Category.objects.get(slug=category_slug)
        products = category.products.all()
        products_sorted = sort_products_to_display(products)
        return render(
            request, 'shop/filtered_product_list.html',
            {'category': category, 'products': products_sorted}
        )

    except Category.DoesNotExist:
        messages.error(
            request, "Unfortunately, the category you were looking for not found."
        )
        return redirect('shop:product_list')

# Views related to brands
def brand_list(request: HttpRequest) -> HttpResponse:
    brands = Brand.objects.all()
    return render(request, 'shop/brand_list.html', {'brands': brands})

def brand_product_list(request: HttpRequest, brand_slug: str) -> HttpResponse:
    try:
        brand = Brand.objects.get(slug=brand_slug)
        brand_products = brand.products.all()
        products_sorted = sort_products_to_display(brand_products)
        available_products = brand_products.filter(available=True)

        if not brand_products:
            messages.error(
                request,
                "At this moment, "
                "we do not have any products from this brand in our store. "
                "Come back soon!"
            )
            return redirect('shop:product_list')

        if not available_products:
            messages.error(
                request,
                "At this moment, "
                "we do not have any available products from this brand in our store. "
                "Come back soon!"
            )

        return render(
            request,
            'shop/filtered_product_list.html',
            {'brand': brand, 'products': products_sorted}
        )

    except Brand.DoesNotExist:
        messages.error(
            request, "Unfortunately, the brand you were looking for not found."
        )
        return redirect('shop:product_list')

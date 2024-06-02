from typing import Type

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class RegisterView(SuccessMessageMixin, CreateView):  # type: ignore
    template_name: str = 'registration/register.html'
    form_class: Type[CustomUserCreationForm] = CustomUserCreationForm
    success_url: str = reverse_lazy(settings.LOGIN_URL)
    success_message: str = "Registration Successful! Now you can log in."


class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        # Capture the next URL to redirect user after successfull login
        next_url = request.GET.get('next')
        if (next_url and
            url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()})):
            request.session['next'] = next_url
        return super().get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        next_url = self.request.session.get('next')
        if next_url:
            del self.request.session['next']
            return next_url
        return super().get_success_url()

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        username: str | None = form.cleaned_data.get('username')
        messages.success(self.request, f"Hello, <strong>{username}</strong>!")
        return super().form_valid(form)

    def form_invalid(self, form: BaseForm) -> HttpResponse:
        messages.error(self.request, 'Invalid username or password.')
        return self.render_to_response(self.get_context_data(form=form))


class BlogLogoutView(LogoutView):
    next_page = reverse_lazy('blog:home')


class ShopLogoutView(LogoutView):
    next_page = reverse_lazy('shop:product_list')

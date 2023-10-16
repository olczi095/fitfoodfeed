from typing import Type

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm

from .forms import CustomUserCreationForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name: str = 'registration/register.html'
    form_class: Type[CustomUserCreationForm] = CustomUserCreationForm
    success_url: str = reverse_lazy('app_accounts:login')
    success_message: str = f"Registration Successful! Now you can log in."


class CustomLoginView(LoginView):
    def get_success_url(self) -> str:
        return reverse('app_reviews:home')
    
    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        username: str | None = form.cleaned_data.get('username')
        messages.success(self.request, f"Hello, <strong>{username}</strong>!")
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseForm) -> HttpResponse:
        messages.error(self.request, 'Invalid username or password.')
        return self.render_to_response(self.get_context_data(form=form))
from typing import Type

from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm

from .forms import CustomUserCreationForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name: str = 'registration/register.html'
    form_class: Type[CustomUserCreationForm] = CustomUserCreationForm
    success_url: str = reverse_lazy('app_reviews:home')

    def form_valid(self, form: BaseForm) -> HttpResponse:
        response: HttpResponse = super().form_valid(form)
        username: str = form.cleaned_data['username']
        login(self.request, self.object)
        messages.success(self.request, f"Registration Successful! Welcome <strong>{username}</strong>, you are now logged in.")
        return response


class CustomLoginView(LoginView):
    def get_success_url(self) -> str:
        return reverse('app_reviews:home')
    
    def form_invalid(self, form: BaseForm) -> HttpResponse:
        messages.error(self.request, 'Invalid username or password.')
        return self.render_to_response(self.get_context_data(form=form))
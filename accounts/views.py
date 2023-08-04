from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse_lazy('app_reviews:home')
    

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('app_reviews:home')
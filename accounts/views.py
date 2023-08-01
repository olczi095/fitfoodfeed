from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    # success_url = reverse_lazy('app_reviews:home')

    def get_success_url(self):
        return reverse_lazy('app_reviews:home')
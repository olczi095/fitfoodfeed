from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
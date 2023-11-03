from typing import Type

from django import forms 
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm): # type: ignore
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model: Type[User] = User
        fields: tuple[str, ...] = (
            'username', 
            'password1', 
            'password2', 
            'first_name', 
            'last_name', 
            'email'
        )
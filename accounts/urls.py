from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from .views import RegisterView, CustomLoginView


app_name = 'app_accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password-reset/', PasswordResetView.as_view(
        template_name = 'password_reset/password_reset.html',
        email_template_name = 'password_reset/password_reset_email.html',
        success_url = reverse_lazy('app_accounts:password_reset_done')
    ), name='password_reset'),

    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name = 'password_reset/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name = 'password_reset/password_reset_confirm.html',
        success_url = reverse_lazy('app_accounts:password_reset_complete')
    ), name='password_reset_confirm'),

    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name = 'password_reset/password_reset_complete.html'
    ), name='password_reset_complete'),
]

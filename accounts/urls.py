from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import (LogoutView, PasswordChangeDoneView,
                                       PasswordChangeView, PasswordResetCompleteView,
                                       PasswordResetConfirmView, PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from .views import BlogLogoutView, CustomLoginView, RegisterView, ShopLogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/blog/', BlogLogoutView.as_view(), name='blog_logout'),
    path('logout/shop/', ShopLogoutView.as_view(), name='shop_logout'),

    path('password-change/', PasswordChangeView.as_view(
        template_name='password_change/password_change_form.html',
        success_url=reverse_lazy('accounts:password_change_done'),
        form_class=PasswordChangeForm
    ), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='password_change/password_change_done.html'
    ), name='password_change_done'),

    path('password-reset/', PasswordResetView.as_view(
        template_name='password_reset/password_reset.html',
        email_template_name='password_reset/password_reset_email.html',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='password_reset/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='password_reset/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='password_reset/password_reset_complete.html'
    ), name='password_reset_complete'),
]

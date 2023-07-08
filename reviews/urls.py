from django.urls import path
from . import views

app_name = 'app_reviews'

urlpatterns = [
    path('', views.test, name='test')
]


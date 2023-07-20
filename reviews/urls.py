from django.urls import path
from .views import PostListView

app_name = 'app_reviews'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
]


from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'app_reviews'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('<slug:slug>/', PostDetailView.as_view(), name='review'),
]
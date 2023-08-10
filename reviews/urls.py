from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView

app_name = 'app_reviews'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('add-review/', PostCreateView.as_view(), name='add_review'),
    path('<slug:slug>/', PostDetailView.as_view(), name='review'),
]
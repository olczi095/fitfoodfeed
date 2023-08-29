from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, TaggedPostsListView, TagsListView, CategoryListView

app_name = 'app_reviews'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('tags/', TagsListView.as_view(),name='tags'),
    path('create-review/', PostCreateView.as_view(), name='create_review'),
    path('category/<str:category_name>/', CategoryListView.as_view(), name='category'),
    path('tag/<str:tag_name>/', TaggedPostsListView.as_view(), name='tag'),
    path('<slug:slug>/', PostDetailView.as_view(), name='review'),
]
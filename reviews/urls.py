from django.urls import path

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    TaggedPostsListView,
    TagsListView,
    CategoryListView,
    PostLikeView,
)

app_name = 'app_reviews'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('tags/', TagsListView.as_view(),name='tags'),
    path('create-review/', PostCreateView.as_view(), name='create_review'),
    path('update-review/<int:pk>/', PostUpdateView.as_view(), name='update_review'),
    path('delete-review/<int:pk>/', PostDeleteView.as_view(), name='delete_review'),
    path('category/<str:category_name>/', CategoryListView.as_view(), name='category'),
    path('tag/<str:tag_name>/', TaggedPostsListView.as_view(), name='tag'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail_review'),
    path('like/<int:pk>/', PostLikeView.as_view(), name='like_post'),
]

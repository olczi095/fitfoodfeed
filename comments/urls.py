from django.urls import path

from .views import CommentDeleteView

app_name = 'comments'

urlpatterns = [
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(),
        name='delete_comment'),
]

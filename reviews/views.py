from typing import Any, Dict
from django.shortcuts import render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from reviews.models import Post

from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().order_by('-pub_date')
    

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    permission_required = 'app_reviews.add_post'
    permission_denied_message = "You don't have permission to access this page. Please log in using a valid account."
    template_name = 'reviews/post_add.html'
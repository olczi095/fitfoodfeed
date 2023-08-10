from typing import Any, Dict
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .forms import PostForm

from reviews.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().order_by('-pub_date')
    

class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'reviews/post_add.html'
from typing import Any, Dict
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView

from reviews.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'reviews/home.html'
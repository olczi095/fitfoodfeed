from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from taggit.models import Tag

from reviews.models import Post

from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(status='PUB').order_by('-pub_date')
    

class TaggedPostsListView(ListView):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3    

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, name=tag_name)
        return super().get_queryset().filter(status='PUB').filter(tags=tag)


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.filter(status="PUB")

  
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    permission_required = 'app_reviews.add_post'
    permission_denied_message = "You don't have permission to access this page. Please log in using a valid account"
    template_name = 'reviews/post_add.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.status == "PUB":
            return super().get_success_url() 
        return reverse('app_reviews:home')
        
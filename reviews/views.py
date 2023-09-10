from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from taggit.models import Tag

from reviews.models import Post, Category

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


class TagsListView(ListView):
    model = Tag
    template_name = 'reviews/tags.html'
    context_object_name = 'tags'


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.filter(status="PUB")
    template_name = 'reviews/review_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.filter(active=True)
        return context


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    permission_required = 'reviews.add_post'
    permission_denied_message = "You don't have permission to access this page. Please log in using a valid account"
    template_name = 'reviews/review_create.html'
    success_message = "Post <strong>%(title)s</strong> added successfully."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.status == "PUB":
            return super().get_success_url() 
        return reverse('app_reviews:home')
    

class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'pub_date', 'image', 'category', 'meta_description', 'body', 'status', 'tags']
    permission_denied_message = "You don't have permission to access this page. Please log in using a valid account"
    permission_required = 'reviews.update_post'
    template_name = 'reviews/review_update.html'
    success_message = "Post <strong>%(title)s</strong> successfully updated."

    def test_func(self):
        # Only superusers, staff and the proper post's author can access the update view
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user == self.get_object().author
    

class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    permission_denied_message = "You don't have permission to access this page. Please log in using a valid account"
    template_name = 'reviews/review_delete.html'
    success_url = reverse_lazy('app_reviews:home')

    def test_func(self):
        # Only superusers, staff and the proper post's author can access the delete view
        return self.request.user.is_superuser or self.request.user.is_staff or self.request.user == self.get_object().author

    def get_success_message(self, cleaned_data):
        return f"Post <strong>{self.object.title}</strong> deleted successfully."
    

class CategoryListView(ListView):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=category_name)
        return super().get_queryset().filter(status='PUB', category=category)
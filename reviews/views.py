from typing import Dict
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from reviews.models import Post, Category, Comment

from .forms import PostForm, CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(status='PUB').order_by('-pub_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts_with_comment_counters = {}
        recent_comments = [comment for comment in Comment.objects.filter(active=True).order_by('pub_datetime')[:3]]

        for post in Post.objects.filter(status='PUB'):
            posts_with_comment_counters[post] = post.comment_counter()

        popular_posts = sorted(posts_with_comment_counters.items(), key=lambda x: x[1], reverse=True)
        popular_posts = [popular_post[0] for popular_post in popular_posts] # Get just posts without comment counters
        context['popular_posts'] = popular_posts[:5]
        context['recent_comments'] = recent_comments
        return context
    

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


class PostDetailView(SuccessMessageMixin, FormMixin, DetailView):
    form_class = CommentForm
    model = Post
    queryset = Post.objects.filter(status="PUB")
    template_name = 'reviews/review_detail.html'

    def get_success_url(self) -> str:
        return reverse('app_reviews:detail_review', kwargs={'slug': self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.filter(active=True)
        context['form'] = CommentForm(initial={'post': self.object})
        context['user'] = self.request.user
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_comment = form.save(commit=False)

        if self.request.user.is_authenticated:
            new_comment.logged_user = self.request.user
            new_comment.unlogged_user = None
            
        if self.request.user.is_superuser:
            self.success_message = "Comment successfully added." 
        else:
            self.success_message = "Comment successfully submitted. It will be published after moderation and validation." 

        new_comment.post = self.object
        new_comment.save()

        form.save()
        
        return super(PostDetailView, self).form_valid(form)
    

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
from random import sample
from typing import Any

from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    UserPassesTestMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView,
    RedirectView
)
from django.views.generic.edit import FormMixin
from django.http import (
    HttpRequest, 
    HttpResponse
)
from django.db.models import Model, QuerySet
from django.forms import BaseForm, BaseModelForm, ModelForm
from taggit.models import Tag

from accounts.models import User
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


class PostListView(ListView[Model]):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.filter(status='PUB').order_by('-pub_date')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        posts_with_comment_counters = {}
        recent_comments_qs: QuerySet[Comment] = Comment.objects.filter(active=True) \
            .order_by('pub_datetime')[:3]
        recent_comments: list[Comment] = [comment for comment in recent_comments_qs]

        for post in Post.objects.filter(status='PUB'):
            posts_with_comment_counters[post] = post.comment_counter()
            
        popular_posts_with_comment_counters = sorted(
            posts_with_comment_counters.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        popular_posts = [popular_post[0] 
                        for popular_post in popular_posts_with_comment_counters] # Get just posts without comment counters
        context['popular_posts'] = popular_posts[:5]
        context['recent_comments'] = recent_comments
        return context
    

class TaggedPostsListView(ListView[Post]):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3    

    def get_queryset(self) -> QuerySet[Post]:
        tag_name = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, name=tag_name)
        queryset = Post.objects.filter(status='PUB').filter(tags=tag)
        return queryset


class TagsListView(ListView[Model]):
    model = Tag
    template_name = 'reviews/tags.html'
    context_object_name = 'tags'


class PostDetailView(SuccessMessageMixin, FormMixin[BaseForm], DetailView[Model]):
    form_class = CommentForm
    model = Post
    queryset = Post.objects.filter(status="PUB")
    template_name = 'reviews/review_detail.html'

    def get_success_url(self) -> str:
        if isinstance(self.object, Post):
            return self.object.get_absolute_url()
        return super().get_success_url()    
    
    def get_related_posts(self) -> list[Post]:
        """
        Gets random posts that have the same tag
        as post in order to propose them to the user.
        """
        post_tags = self.object.tags.all() if isinstance(self.object, Post) else None
        all_related_posts = list(Post.objects.filter(tags__in=post_tags).exclude(pk=self.object.pk).distinct())
        if len(all_related_posts) <= 3 :
            return all_related_posts
        else:
            three_random_related_posts = sample(all_related_posts, k=3)
            return three_random_related_posts
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(PostDetailView, self).get_context_data(**kwargs)

        if isinstance(self.object, Post):
            comments = self.object.comment_set.filter(active=True)
            context['comments'] = comments

            likes_count = self.object.likes_counter()
            context['post_likes'] = '1 Like' if likes_count == 1 else f'{likes_count} Likes'
            
        context['form'] = CommentForm(initial={'post': self.object})
        context['user'] = self.request.user
        context['related_posts'] = self.get_related_posts()
        return context
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any
             ) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: BaseForm) -> HttpResponse:
        if isinstance(form, CommentForm):
            new_comment = form.save(commit=False)

            if isinstance(self.request.user, User) and \
                    self.request.user.is_authenticated and \
                    isinstance(new_comment, Comment):
                new_comment.logged_user = self.request.user
                new_comment.unlogged_user = None
                
            if self.request.user.is_superuser:
                self.success_message = "Comment successfully added." 
            else:
                self.success_message = "Comment successfully submitted. \
                                        It will be published after moderation and validation." 

            if isinstance(new_comment, Comment) and isinstance(self.object, Post):
                new_comment.post = self.object
                new_comment.save()
        
        return super().form_valid(form)


class PostLikeView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        pk = kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        user = self.request.user
    
        if post.likes.filter(pk=str(user.pk)).exists() and isinstance(user, User):
            post.likes.remove(user)
        elif isinstance(user, User):
            post.likes.add(user)

        return post.get_absolute_url()


class PostCreateView(
    SuccessMessageMixin, 
    LoginRequiredMixin, 
    PermissionRequiredMixin, 
    CreateView[Model, BaseModelForm[Any]]
):
    model = Post
    form_class = PostForm
    permission_required = 'reviews.add_post'
    permission_denied_message = "You don't have permission to access this page. \
                                Please log in using a valid account"
    template_name = 'reviews/review_create.html'
    success_message = "Post <strong>%(title)s</strong> added successfully."

    def form_valid(self, form: BaseForm) -> HttpResponse:
        if isinstance(form, PostForm) and \
            isinstance(form.instance, Post) and \
            isinstance(self.request.user, User):
            form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        if isinstance(self.object, Post) and self.object.status == "PUB":
            return super().get_success_url() 
        return reverse('app_reviews:home')
    

class PostUpdateView(
    SuccessMessageMixin, 
    LoginRequiredMixin, 
    UserPassesTestMixin, 
    UpdateView[Post, ModelForm[Post]]
):
    model = Post
    fields = [
        'title', 
        'slug', 
        'pub_date', 
        'image', 
        'category', 
        'meta_description', 
        'body', 
        'status', 
        'tags'
    ]
    permission_denied_message = "You don't have permission to access this page. \
                                Please log in using a valid account"
    permission_required = 'reviews.update_post'
    template_name = 'reviews/review_update.html'
    success_message = "Post <strong>%(title)s</strong> successfully updated."

    def test_func(self) -> bool:
        # Only superusers, staff and the proper post's author can access the update view
        return (
            self.request.user.is_superuser 
            or self.request.user.is_staff 
            or self.request.user == self.get_object().author
        )
    

class PostDeleteView(
    SuccessMessageMixin, 
    LoginRequiredMixin, 
    UserPassesTestMixin, 
    DeleteView[Post, ModelForm[Post]]
): 
    model = Post
    permission_denied_message = "You don't have permission to access this page. \
                                Please log in using a valid account"
    template_name = 'reviews/review_delete.html'
    success_url = reverse_lazy('app_reviews:home')

    def test_func(self) -> bool:
        # Only superusers, staff and the proper post's author can access the delete view
        return (
            self.request.user.is_superuser 
            or self.request.user.is_staff 
            or self.request.user == self.get_object().author
        )

    def get_success_message(self, cleaned_data: dict[Any, Any]) -> str:
        return f"Post <strong>{self.object.title}</strong> deleted successfully."
    

class CategoryListView(ListView[Model]):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Post]:
        category_name = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=category_name)
        queryset = Post.objects.filter(status='PUB', category=category)
        return queryset
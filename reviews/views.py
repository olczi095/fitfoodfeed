from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Model, QuerySet
from django.forms import BaseForm, BaseModelForm, ModelForm
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from accounts.models import \
    User as AccountsUser  # Importing User directly for type hints

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

User = get_user_model()


class PostListView(ListView[Model]):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.filter(status='PUB').order_by('-pub_date')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.get_popular_posts(5)
        context['recent_comments'] = Comment.get_recent_comments(3)
        return context


class TaggedPostsListView(ListView[Post]):
    model = Post
    template_name = 'reviews/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.get_popular_posts(5)
        context['recent_comments'] = Comment.get_recent_comments(3)
        return context

    def get_queryset(self) -> QuerySet[Post]:
        tag_name = self.kwargs['tag_name']
        return Post.get_tagged_posts(tag_name)


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
        if not isinstance(self.object, Post):
            raise Http404("Post not found.")
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if isinstance(self.object, Post):
            context['comments'] = self.object.get_top_level_comments()
            context['post_likes'] = self.object.display_likes_stats()

        context['form'] = CommentForm(initial={'post': self.object})
        context['user'] = self.request.user
        context['related_posts'] = self.object.get_related_posts(3)
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any
             ) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()
        editing_comment_id: str | None = request.POST.get('editing_comment_id')

        if form.is_valid():
            return self.form_valid(form, editing_comment_id)
        return self.form_invalid(form)

    def form_valid(self, form: BaseForm, editing_comment_id: str) -> HttpResponse:
        comment_parent_id = self.request.POST.get('comment_parent_id')
        comment_parent = Comment.objects.filter(pk=comment_parent_id).first()

        if editing_comment_id:
            # Edit the existing comment if editing_comment_id field exists
            editing_comment = Comment.objects.get(pk=editing_comment_id)
            editing_comment.body = form.cleaned_data['body']
            editing_comment.save()

            self.success_message = "Comment successfully <strong>edited</strong>."
        else:
            # Add a new comment
            new_comment = form.save(commit=False)

            if comment_parent:
                new_comment.response_to = comment_parent

            if (
                isinstance(self.request.user, User)
                and self.request.user.is_authenticated
            ):
                new_comment.logged_user = self.request.user
                new_comment.unlogged_user = None

            self.success_message = (
                "Comment successfully <strong>added</strong>."
                if self.request.user.is_staff
                else "Comment successfully <strong>submitted</strong>."
                "It will be published after moderation and validation."
            )

            if isinstance(new_comment, Comment) and isinstance(self.object, Post):
                new_comment.post = self.object
                new_comment.save()

        return super().form_valid(form)


class PostLikeView(View):
    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        pk: int | None = kwargs.get('pk')
        post: Post = get_object_or_404(Post, pk=pk)
        user: AccountsUser | AnonymousUser = self.request.user
        liked: bool = post.toggle_like(user)

        data = {
            'url': post.get_absolute_url(),
            'liked': liked,
            'likes_stats_display': post.display_likes_stats()
        }
        return JsonResponse(data)


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
        if (
            isinstance(form, PostForm) and
            isinstance(form.instance, Post) and
            isinstance(self.request.user, User)
        ):
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.get_popular_posts(5)
        context['recent_comments'] = Comment.get_recent_comments(3)
        return context

    def get_queryset(self) -> QuerySet[Post]:
        category_name = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=category_name)
        return category.get_posts()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self) -> bool | None:
        return self.request.user.is_staff

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return HttpResponse(status=303)

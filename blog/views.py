from datetime import datetime
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.forms import BaseForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView, View)
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from accounts.models import \
    User as AccountsUser  # Importing User directly for type hints
from comments.forms import CommentForm
from comments.models import Publication
from comments.views import CommentSubmissionMixin
from fitfoodfeed.settings import EMAIL_HOST_USER

from .forms import PostForm, ProductSubmissionForm
from .models import Category, Post
from .utils import (generate_confirmation_data, generate_mail_data,
                    prepare_mail_message, send_email_with_product_for_review)

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.filter(status='PUB').order_by('-pub_date')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.get_popular_posts(5)
        context['recent_comments'] = Publication.get_recent_comments(3, 'post')
        return context


class TaggedPostsListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.get_popular_posts(5)
        context['recent_comments'] = Publication.get_recent_comments(3, 'post')
        return context

    def get_queryset(self) -> QuerySet[Post]:
        tag_slug = self.kwargs['tag_slug']
        return Post.get_tagged_posts(tag_slug)


class TagsListView(ListView):
    model = Tag
    template_name = 'blog/tags.html'
    context_object_name = 'tags'


class PostDetailView(CommentSubmissionMixin, FormMixin, DetailView):
    form_class = CommentForm
    model = Post
    slug_url_kwarg = 'post_slug'
    queryset = Post.objects.filter(status="PUB")
    template_name = 'blog/review_detail.html'

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['user'] = self.request.user
        context['related_posts'] = self.object.get_related_posts(3)
        context['post_likes'] = (
            self.object.display_likes_stats() if isinstance(self.object, Post) else None
        )
        context['comments'] = (
            self.object.publication.get_top_level_comments() if self.object.publication else None
        )
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()  # Get the post object
        form = self.get_form()  # Get the form instance with POST data

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class PostLikeView(View):
    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        pk: int | None = kwargs.get('pk')
        post: Post = get_object_or_404(Post, pk=pk)
        user: AccountsUser
        liked: bool

        if self.request.user.is_authenticated:
            user = self.request.user
            liked = post.toggle_like(user)

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
    CreateView
):
    model = Post
    form_class = PostForm
    permission_required = 'blog.add_post'
    permission_denied_message = "You don't have permission to access this page. \
                                Please log in using a valid account"
    template_name = 'blog/review_create.html'
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
        return reverse('blog:home')


class PostUpdateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
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
    permission_required = 'blog.update_post'
    template_name = 'blog/review_update.html'
    success_message = "Post <strong>%(title)s</strong> successfully updated."

    def test_func(self) -> bool:
        # Only superusers, staff and the proper post's author can access the update view
        return (
            self.request.user.is_superuser
            or self.request.user.is_staff
            or self.request.user == self.get_object().author
        )


class PostDeleteView(  # type: ignore
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Post
    permission_denied_message = "You don't have permission to access this page. \
                                Please log in using a valid account"
    template_name = 'blog/review_delete.html'
    success_url = reverse_lazy('blog:home')

    def test_func(self) -> bool:
        # Only superusers, staff and the proper post's author can access the delete view
        return (
            self.request.user.is_superuser
            or self.request.user.is_staff
            or self.request.user == self.get_object().author
        )

    def get_success_message(self, cleaned_data: dict[Any, Any]) -> str:
        return f"Post <strong>{self.object.title}</strong> deleted successfully."


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.get_popular_posts(5)
        context['recent_comments'] = Publication.get_recent_comments(3, 'post')
        return context

    def get_queryset(self) -> QuerySet[Post]:
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        return category.get_posts()


class ProductSubmissionFormView(FormView, SuccessMessageMixin):
    template_name = 'blog/product_submit.html'
    form_class = ProductSubmissionForm
    success_url = reverse_lazy('blog:home')
    success_message = "Your email has been sent successfully."

    def form_valid(self, form: ProductSubmissionForm) -> HttpResponse:
        if not self.request.user.is_authenticated:
            email = form.cleaned_data.get('user_email')
            if email:
                # Generate confirmation data
                confirmation_data = generate_confirmation_data()
                self.request.session['confirmation_data'] = confirmation_data
                self.request.session['completed_form'] = form.cleaned_data

                # Send confirmation mail
                subject = 'Please confirm your email address'
                context = {
                    'protocol': 'http',
                    'domain': self.request.get_host(),
                    'confirmation_code': confirmation_data['confirmation_code']
                }
                html_message = render_to_string('blog/mail_confirmation.html', context=context)
                plain_message = strip_tags(html_message)
                from_email = EMAIL_HOST_USER
                to_email = [email]

                send_mail(subject, plain_message, from_email, to_email)
                messages.success(
                    self.request,
                    'Email confirmation link has been sent. Please check your inbox.'
                )
                return super().form_valid(form)

        mail_message = prepare_mail_message(
            product_name=form.cleaned_data['name'],
            product_brand=form.cleaned_data['brand'],
            product_category=form.cleaned_data.get('category', ''),
            product_description=form.cleaned_data.get('description', ''),
            user_email=form.cleaned_data['user_email']
        )
        mail_data = generate_mail_data(
            product_name=form.cleaned_data['name'],
            message=mail_message,
            user_email=form.cleaned_data['user_email'],
            product_image=form.cleaned_data.get('image', None)
        )
        send_email_with_product_for_review(mail_data)
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class ConfirmEmailView(View, SuccessMessageMixin):
    success_message = "Your email has been sent successfully."

    def get(self, request: HttpRequest) -> HttpResponse:
        confirmation_data = request.session.get('confirmation_data')
        completed_form_data = request.session.get('completed_form')

        if not confirmation_data or not completed_form_data:
            return HttpResponse('Invalid confirmation request')

        confirmation_date = confirmation_data['confirmation_date']

        if confirmation_date:
            confirmation_date = datetime.fromisoformat(confirmation_date)
            current_date = timezone.now()

        if confirmation_date >= current_date:
            # Get cleaned data from the form
            product_name = completed_form_data.get('name')
            product_brand = completed_form_data.get('brand')
            product_category = completed_form_data.get('category', '')
            product_description = completed_form_data.get('description', '')
            user_email = completed_form_data.get('user_email')
            product_image = completed_form_data.get('image', None)

            mail_message = prepare_mail_message(product_name, product_brand,
                                                product_category, product_description,
                                                user_email)
            mail_data = generate_mail_data(product_name, mail_message, user_email,
                                           product_image)
            # Send an e-mail
            send_email_with_product_for_review(mail_data)
            messages.success(self.request, self.success_message)
        else:
            return HttpResponse('Confirmation code has expired')

        del request.session['confirmation_data']
        del request.session['completed_form']

        return HttpResponseRedirect(reverse('blog:home'))

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .forms import CommentForm
from .models import Comment

User = get_user_model()


class SuccessMessageCommentMixin(SuccessMessageMixin):
    """
    Mixin to add a success message on form submission for comments.
    """
    request: HttpRequest
    success_message = ""
    object: Any

    def form_valid(self, form: CommentForm) -> HttpResponse:
        self.success_message = ""

        editing_comment_id = self.request.POST.get('editing_comment_id')
        comment_parent_id = self.request.POST.get('comment_parent_id')
        comment_parent = None

        if comment_parent_id is not None and isinstance(comment_parent_id, str):
            comment_parent_id = str(comment_parent_id)
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

            if self.request.user.is_staff:
                self.success_message = (
                    "Comment successfully <strong>added</strong>."
                )
            else:
                self.success_message = (
                    "Comment successfully <strong>submitted</strong>. "
                    "It will be published after moderation and validation."
                )
            if isinstance(new_comment, Comment) and self.object.publication:
                new_comment.publication = self.object.publication
                new_comment.save()

        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self) -> bool | None:
        return self.request.user.is_staff

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return HttpResponse(status=303)

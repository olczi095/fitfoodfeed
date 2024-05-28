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


class CommentSubmissionMixin(SuccessMessageMixin):
    """
    Mixin to handle comment submission and editing comment logic
    with the proper success message.
    """
    request: HttpRequest
    success_message = ""
    object: Any

    def handle_comment_submission(self, form: CommentForm) -> str:
        """
        Handles submission of a new comment.

        This method is responsible for processing the submitted form data,
        saving the comment, and returning the appropriate success message.

        Args:
            form (CommentForm): The form instance containing comment data.

        Returns:
            str: The success message to be displayed.
        """
        editing_comment_id = self.request.POST.get('editing_comment_id')
        comment_parent_id = self.request.POST.get('comment_parent_id')
        comment_parent = None

        if comment_parent_id is not None and isinstance(comment_parent_id, str):
            comment_parent_id = str(comment_parent_id)
            comment_parent = Comment.objects.filter(pk=comment_parent_id).first()

        # If editing_comment_id is present, edit the existing comment
        if editing_comment_id:
            editing_comment = Comment.objects.get(pk=editing_comment_id)
            editing_comment.body = form.cleaned_data['body']
            editing_comment.save()
            return "Comment successfully <strong>edited</strong>."

        # Otherwise, add a new comment
        new_comment = form.save(commit=False)

        # Set the parent comment if it exists
        if comment_parent:
            new_comment.response_to = comment_parent

        # Set the user if authenticated
        if (
            isinstance(self.request.user, User)
            and self.request.user.is_authenticated
        ):
            new_comment.logged_user = self.request.user
            new_comment.unlogged_user = None

        # Associate the comment with the publication
        if isinstance(new_comment, Comment) and self.object.publication:
            new_comment.publication = self.object.publication
            new_comment.save()

        # Set the success message based on user role
        if self.request.user.is_staff:
            return "Comment successfully <strong>added</strong>."
        return (
                "Comment successfully <strong>submitted</strong>. "
                "It will be published after moderation and validation."
            )

    def form_valid(self, form: CommentForm) -> HttpResponse:
        """
        Overrides the form_valid method to handle comment submission
        and sets the proper success message for the commenting user.
        """
        self.success_message = self.handle_comment_submission(form)
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

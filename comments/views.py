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

    def form_valid(self, form: CommentForm) -> HttpResponse:
        """
        Overrides the form_valid method to handle comment submission
        and sets the proper success message for the commenting user.
        """
        self.success_message = self.handle_comment_submission(form)
        return super().form_valid(form)

    def handle_comment_submission(self, form: CommentForm) -> str:
        """
        Handles submission of a new comment.

        This method is responsible for processing the submitted form data,
        saving the comment, and returning the appropriate success message.

        Parameters:
            form (CommentForm): The form instance containing comment data

        Returns:
            str: The success message to be displayed
        """

        editing_comment = self.get_editing_comment()
        if editing_comment:
            return self.edit_existing_comment(editing_comment, form)
        return self.add_new_comment(form)

    def get_success_message(self, cleaned_data):
        return self.success_message

    def add_new_comment(self, form: CommentForm) -> str:
        """
        Adds a new comment and connect it with its parent.
        """
        comment_parent = self.get_comment_parent()
        new_comment = form.save(commit=False)

        if comment_parent:
            new_comment.response_to = comment_parent

        self.set_comment_user(new_comment)
        self.associate_comment_with_publication(new_comment)

        new_comment.save()

        return self.get_success_message_based_on_user_role()

    def get_comment_parent(self) -> Comment | None:
        """
        Retrieves comment parent if exists, otherwise returns None.
        """
        comment_parent_id = self.request.POST.get('comment_parent_id')
        if comment_parent_id is not None and isinstance(comment_parent_id, str):
            comment_parent_id = str(comment_parent_id)
            return Comment.objects.filter(pk=comment_parent_id).first()
        return None

    def get_editing_comment(self) -> Comment | None:
        """
        Retrieves the existing comment being edited from database if editing_comment_id is present.
        Otherwise returns None.
        """
        editing_comment_id = self.request.POST.get('editing_comment_id')
        if editing_comment_id:
            return Comment.objects.get(pk=editing_comment_id)
        return None

    def edit_existing_comment(self, editing_comment: Comment, form: CommentForm) -> str:
        """"
        Edit an existing comment if it is already in database.
        
        Parameters:
            editing_comment (Comment) : The comment being edited
            form (CommentForm) : The form instance containing comment data
            
        Returns: 
            str: The success message for editing a comment
        """
        editing_comment.body = form.cleaned_data['body']
        editing_comment.save()
        return "Comment successfully <strong>edited</strong>."

    def set_comment_user(self, new_comment: Comment) -> None:
        """
        Sets the user for the new comment if user is authenticated.
        """
        if (
            isinstance(self.request.user, User)
            and self.request.user.is_authenticated
        ):
            new_comment.logged_user = self.request.user
            new_comment.unlogged_user = None

    def associate_comment_with_publication(self, new_comment: Comment) -> None:
        """
        Associates the comment with the publication if it exists.
        """
        if isinstance(new_comment, Comment) and hasattr(self.object, 'publication'):
            new_comment.publication = self.object.publication

    def get_success_message_based_on_user_role(self) -> str:
        """
        Returns the success message based on the user role.
        """
        if self.request.user.is_staff:
            return "Comment successfully <strong>added</strong>."
        return (
                "Comment successfully <strong>submitted</strong>. "
                "It will be published after moderation and validation."
            )


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self) -> bool | None:
        return self.request.user.is_staff

    def delete(self, request: HttpRequest, pk: int) -> HttpResponse:
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return HttpResponse(status=303)

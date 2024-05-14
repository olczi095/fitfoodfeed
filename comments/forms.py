from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model: type[Comment] = Comment
        fields: list[str] = [
            'logged_user',
            'unlogged_user',
            'email',
            'body'
        ]
        labels: dict[str, str] = {
            'logged_user': 'User',
            'unlogged_user': 'Name',
            'body': '',
            'email': 'Email'
        }
        widgets: dict[str, forms.Widget] = {
            'logged_user': forms.TextInput(attrs={'readonly': True})
        }

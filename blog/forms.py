from django import forms
from django.db.models import Model

from blog.models import Comment, Post


class PostForm(forms.ModelForm[Model]):

    class Meta:
        model: type[Post] = Post
        fields: list[str] = [
            'title',
            'meta_description',
            'tags',
            'body',
            'image',
            'slug',
            'status'
        ]
        labels: dict[str, str] = {
            'title': 'Title',
            'meta_description': 'Meta Description',
            'tags': 'Tags',
            'body': 'Body',
            'image': 'Image',
            'slug': 'Slug',
            'status': 'Status'
        }
        widgets: dict[str, forms.Widget] = {
            'author': forms.HiddenInput()
        }
        help_texts: dict[str, str] = {
            'slug': 'You can leave this field empty. \
                The slug will be created based on the title automatically.',
        }


class CommentForm(forms.ModelForm[Model]):

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

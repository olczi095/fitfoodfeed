from django.forms import HiddenInput, ModelForm
from reviews.models import Post, Comment
from django import forms
    

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'meta_description', 'tags', 'body', 'image', 'slug', 'status']
        labels = {
            'title': 'Title',
            'meta_description': 'Meta Description',
            'tags': 'Tags',
            'body': 'Body',
            'image': 'Image',
            'slug': 'Slug',
            'status': 'Status'
        }
        widgets = {
            'author': HiddenInput()
        }
        help_texts = {
            'slug': 'You can leave this field empty. The slug will be created based on the title automatically.',
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['logged_user', 'unlogged_user', 'body']
        labels = {
            'logged_user': 'User',
            'unlogged_user': 'Name',
            'body': ''
        }
        widgets = {
            'logged_user': forms.TextInput(attrs={'readonly': True})
        }
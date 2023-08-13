from django.forms import HiddenInput, ModelForm
from reviews.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'meta_description', 'body', 'image', 'slug']
        labels = {
            'title': 'Title',
            'meta_description': 'Meta Description',
            'body': 'Body',
            'image': 'Image',
            'slug': 'Slug'
        }
        widgets = {
            'author': HiddenInput()
        }
        help_texts = {
            'slug': 'You can leave this field empty. The slug will be created based on the title automatically.',
        }
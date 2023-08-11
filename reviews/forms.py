from django.forms import ModelForm
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
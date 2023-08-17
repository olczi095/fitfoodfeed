from django.forms import HiddenInput, ModelForm
from reviews.models import Post
    

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
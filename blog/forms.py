from django import forms

from blog.models import Category, Post


class PostForm(forms.ModelForm):

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
            'author': forms.HiddenInput(),
            'title': 
                forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 0.7rem'}),
            'meta_description': 
                forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 0.7rem'}),
            'tags': 
                forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 0.7rem'}),
            'body': 
                forms.Textarea(attrs={'class': 'form-control', 'style': 'margin-bottom: 0.7rem'}),
            'image': 
                forms.FileInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 0.7rem'}),
            'slug': 
                forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 0.7rem'}),
            'status': 
                forms.Select(attrs={'class': 'form-control', 'style': 'margin-bottom: 0.7rem'}),
        }
        help_texts: dict[str, str] = {
            'slug': 'You can leave this field empty. \
                The slug will be created based on the title automatically.',
        }


class ProductSubmissionForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label="Product name",
        widget=forms.Textarea(
            attrs={
                'rows': 1, 
                'placeholder': 'e.g. Peanut Butter salted caramel', 
                'style': 'padding: 0.1rem 0.2rem;'
            }
        )
    )
    brand = forms.CharField(
        max_length=50,
        label="Brand",
        widget=forms.Textarea(
            attrs={
                'rows': 1, 
                'placeholder': 'e.g. Krukam',
                'style': 'padding: 0.1rem 0.2rem;'
            }
        )
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Category",
        help_text="optional"
    )
    image = forms.ImageField(
        required=False,
        label="Image",
        help_text="optional"
    )
    description = forms.CharField(
        required=False,
        label="Description",
        widget=forms.Textarea(
            attrs={
                'rows': 4, 
                'placeholder': 
                    'This is a new kind of peanut butter from Krukam, but it is already popular. '
                    'Totally recommend it!',
                'style': 'padding: 0.1rem 0.2rem;'
            }
        )
    )
    user_email = forms.EmailField(
        label="Your e-mail",
        widget=forms.Textarea(
            attrs={
                'rows': 1,
                'style': 'padding: 0.1rem 0.2rem;'
            }
        )
    )

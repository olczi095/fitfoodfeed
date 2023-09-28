from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'pk', 'author_model', 'category_model', 'status', 'pub_date', 'tag_list', 'slug']
    list_filter = ['category', 'status', 'author']
    search_fields = ['title', 'meta_description', 'body']
    prepopulated_fields = {'slug': ('title',)}

    def author_model(self, obj):
        author_change_url = reverse('admin:accounts_user_change', args=[obj.author.id])
        return format_html(f'<a href="{author_change_url}">{obj.author}</a>')
    
    def category_model(self, obj):
        category_change_url = reverse('admin:reviews_category_change', args=[obj.category.id])
        return format_html(f'<a href="{category_change_url}">{obj.category}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
    
    def tag_list(self, obj):
        tags = obj.tags.all()
        tag_links = []

        for tag in tags:
            tag_change_url = reverse('admin:taggit_tag_change', args=[tag.pk])
            tag_links.append(format_html(f'<a href="{tag_change_url}">{tag.name}</a>'))

        return format_html(', '.join(tag_links))
    
    def save_model(self, request, obj, *args, **kwargs):
        if not obj.author:
            obj.author = request.user
        return super().save_model(request, obj, *args, **kwargs)
    
    author_model.short_description = 'AUTHOR'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    list_filter = ['name']
    search_fields = ['name']

    def post_count(self, obj):
        return obj.post_set.count()
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'comment', 'active', 'post_title', 'email', 'datetime']
    list_display_links = ['comment']
    ordering = ['active', 'pub_datetime']

    def author(self, obj):
        if obj.logged_user:
            logged_user_change_url = reverse('admin:accounts_user_change', args=[obj.logged_user.id])
            return format_html(f'<a href="{logged_user_change_url}">{obj.logged_user}</a>')
        else:
            return obj.unlogged_user
        
    def comment(self, obj):
        return obj.body[:75]
    
    def post_title(self, obj):
        post_change_url = reverse('admin:reviews_post_change', args=[obj.post.id])
        return format_html(f'<a href="{post_change_url}">{obj.post.title}</a>')
        
    def email(self, obj):
        if obj.logged_user:
            print(obj.logged_user)
            return obj.email
        return obj.email
        
    def datetime(self, obj):
        return obj.pub_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    def save_model(self, request, obj, form, change):
        if obj.logged_user:
            obj.unlogged_user = None
        return super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj, **kwargs):
        if obj and obj.logged_user is not None:
            self.readonly_fields = ('unlogged_user',)
        else:
            self.readonly_fields = ()
        return super().get_form(request, obj, **kwargs)
    
    def get_changeform_initial_data(self, request):
        return {'unlogged_user': ''}
    
    datetime.short_description = "DATE / TIME"
    post_title.short_description = "POSTED IN"
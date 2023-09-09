from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'pk', 'author', 'category', 'status', 'pub_date', 'tag_list', 'slug']
    list_filter = ['category', 'status', 'author']
    search_fields = ['title', 'meta_description', 'body']
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
    
    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    
    def save_model(self, request, obj, *args, **kwargs):
        if not obj.author:
            obj.author = request.user
        return super().save_model(request, obj, *args, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    list_filter = ['name']
    search_fields = ['name']

    def post_count(self, obj):
        return obj.post_set.count()
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'pub_datetime', 'active']

    def author(self, obj):
        if obj.logged_user:
            return obj.logged_user.username
        else:
            return obj.unlogged_user
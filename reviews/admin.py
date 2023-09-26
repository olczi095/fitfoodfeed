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
    list_display = ['comment', 'post', 'author', 'email', 'datetime', 'active']
    ordering = ['active', 'pub_datetime']

    def comment(self, obj):
        return obj.body[:75]

    def author(self, obj):
        if obj.logged_user:
            return obj.logged_user.username
        else:
            return obj.unlogged_user
        
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
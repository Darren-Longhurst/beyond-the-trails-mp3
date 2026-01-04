from django.contrib import admin
from blogging.models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin
from django.utils.text import slugify

"""Post model in admin panel"""

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'author', 'status', 'created_at')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_at')
    summernote_fields = ('content',)

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return ('likes', 'image', 'slug')
        else:
            return ('author', 'slug', 'likes', 'image', 'status')

    def save_model(self, request, obj, form, change):
        # Automatically sets the author to the person logged in
        if not obj.pk: 
            obj.author = request.user

            if not request.user.is_superuser:
                obj.status = 0
        
        # Automatically creates the slug if it doesn't exist
        if not obj.slug:
            base_slug = slugify(obj.title)
            slug=base_slug
            count = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            obj.slug = slug
            
        super().save_model(request, obj, form, change)

"""Comment model in admin panel"""

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ('author', 'post')
    list_display = ('author', 'post', 'created_at', 'approved')
    search_fields = ['author__username', 'body']
    list_filter = ('approved', 'created_at')
    actions = ['approve_comments']

    """Approve selected comments"""

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

 


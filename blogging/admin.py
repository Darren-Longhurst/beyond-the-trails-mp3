from django.contrib import admin
from blogging.models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

"""Post model in admin panel"""

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_at')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    fields = ('title', 'slug', 'author', 'location', 'weather', 'excerpt', 'bike_choice', 'likes', 'content', 'status',)

"""Comment model in admin panel"""

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'approved')
    search_fields = ['name', 'email', 'body']
    list_filter = ('approved', 'created_at')
    actions = ['approve_comments']

    """Approve selected comments"""

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


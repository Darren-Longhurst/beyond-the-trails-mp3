from django.contrib import admin
from blogging.models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    pass  # Customize admin options here if needed

admin.site.register(Post, PostAdmin)
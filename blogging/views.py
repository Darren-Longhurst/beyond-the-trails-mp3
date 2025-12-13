from django.shortcuts import render
from django.http import HttpResponse
from blogging.models import Post

# Create your views here.
def index(request):
    template = 'blogging/index.html'
    context = {
        'page_title': 'Blog Home',
    }

    return render(request, template, context)

def post_list(request):
    posts = Post.objects.all()
    template = 'blogging/post_list.html'
    context = {
        'page_title': 'All Blog Posts',
        'posts': posts,
    }
    
    return render(request, template, context)

def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)

    template = 'blogging/post_detail.html'
    context = {
        'page_title': post.title,
        'post': post,
    }
    
    return render(request, template, context)

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import messages
from .models import Post
from .forms import CommentForm

# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_at')
    template_name = 'blogging/index.html'
    paginate_by = 6
    

def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

     # Location image mapping
    LOCATION_IMAGES = {
        "KAW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450332/KAW_azhb8h.jpg",
        "GNT": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/GNT_hgmttq.jpg",
        "MCW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/MCW_vccqz4.jpg",
        "TE": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/TE_dxmhjq.jpg",
        "NDW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/NDW_trpocy.jpg",
        "RW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/RW_j5smla.jpg",
        "WKW": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450331/WKW_gnmghj.jpg",
        "OTHER": "https://res.cloudinary.com/dxbvkulz4/image/upload/v1766450332/OTHER_pics80.jpg",
    }

    # Determine fallback image based on location
    image_url = LOCATION_IMAGES.get(post.location, LOCATION_IMAGES["OTHER"])

    # Always define comments and counts first
    comments = post.comments.filter(approved=True).order_by('created_at')
    comment_count = comments.count()

    # Handle POST for new comments
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(
                request,
                "Your comment has been submitted and is awaiting approval."
            )
    else:
        comment_form = CommentForm()

    # Now pass everything to context
    context = {
        'post': post,
        'comments': comments,
        'comment_count': comment_count,
        'comment_form': comment_form,
        'image_url': image_url,
    }

    return render(request, "blogging/post_detail.html", context)
"""
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
"""
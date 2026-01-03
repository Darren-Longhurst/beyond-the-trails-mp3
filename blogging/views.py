from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import CommentForm


# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('created_at')
    template_name = 'blogging/blog.html'
    paginate_by = 6

def home_page(request):
    # Filter for published posts and ensure slug is not empty/null
    latest_posts = Post.objects.filter(status=1).exclude(slug="").order_by('created_at')[:3]
    hero_image = Post.LOCATION_IMAGES["OTHER"]
    
    context = {
        'latest_posts': latest_posts,
        'hero_image': hero_image,
    }
    return render(request, 'blogging/index.html', context)
    

def post_detail(request, slug):
    post = get_object_or_404(Post.objects.filter(status=1), slug=slug)

    # Comments: approved or authored by the logged-in user
    if request.user.is_authenticated:
        comments = (post.comments.filter(approved=True) | post.comments.filter(author=request.user)).distinct().order_by('created_at')
    else:
        comments = post.comments.filter(approved=True).order_by('created_at')

    comment_count = post.comments.filter(approved=True).count()

    # Handle new comment submission
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, "Your comment has been submitted and is awaiting approval.")
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_count': comment_count,
        'comment_form': comment_form,
    }

    return render(request, "blogging/post_detail.html", context)

@login_required
def comment_edit(request, slug, comment_id):
    """
    view to edit comments
    """
    post = get_object_or_404(Post, slug=slug, status=1)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)
    
    """ Ensure the logged-in user is the author of the comment """
    if comment.author != request.user:
        messages.error(request, "You are not allowed to edit this comment.")
        return HttpResponseRedirect(reverse("post_detail", args=[slug]))

    if request.method == "POST":
        comment_form = CommentForm(request.POST, instance=comment)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.approved = False
            comment.save()
            messages.success(request, "Comment updated and awaiting approval.")
        else:
            messages.error(request, "Error updating comment.")

    return HttpResponseRedirect(reverse("post_detail", args=[slug]))

@login_required
def comment_delete(request, slug, comment_id):
    """
    view to delete comments
    """
    post = get_object_or_404(Post, slug=slug, status=1)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    """ Ensure the logged-in user is the author of the comment """
    if comment.author != request.user:
        messages.error(request, "You are not allowed to delete this comment.")
        return HttpResponseRedirect(reverse("post_detail", args=[slug]))

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully.")

    return HttpResponseRedirect(reverse("post_detail", args=[slug]))

@login_required
def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(post.get_absolute_url())
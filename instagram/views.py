from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
# from .forms import PostForm, CommentForm
from .forms import PostForm
from .models import Tag, Post

# Create your views here.

@login_required
def index(request):
    return render(request, "instagram/index.html", {    })


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit =False)
            post.author = request.user 
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request, "Record Post")
            return redirect(post)
    else: 
        form = PostForm()

    return render(request, "instagram/post_form.html", {
        "form": form,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "instagram/post_detail.html", {
        "post":post,
    })


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()  
    
    # if request.user.is_authenticated:
    #     is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    # else:
    #     is_follow = False

    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
        "post_list_count": post_list_count,
        # "is_follow": is_follow,
    })
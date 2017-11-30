from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewsPostForm
from .models import NewsPost

@login_required(login_url="/login/")
def home_page(request):
    """ Form logic for registering a new post """
    if request.method == "POST":
        form = NewsPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    
    form = NewsPostForm()
    post_list = NewsPost.objects.all()
    return render(request, 'blog/home.html', {'form': form, 'post_list':post_list})
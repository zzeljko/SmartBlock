from django.shortcuts import render, redirect
from .forms import NewsPostForm
from .models import NewsPost
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import KeyForm

@login_required(login_url="/login/")
def home_page(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	form_class = NewsPostForm
    # if request is not post, initialize an empty form
	form = form_class(request.POST or None)
	
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

@login_required(login_url="/login/")
def my_profile(request):
	# if not request.user.is_authenticated():
	# 	return HttpResponseRedirect('/')
	print ('aici')
	if request.method == 'POST':
		form = KeyForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
	else:
		form = KeyForm()
	return render(request, 'blog/profile.html', {"form_my_profile": form})

from django.shortcuts import render, redirect
from .forms import NewsPostForm
from .models import NewsPost, Key
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from .forms import KeyForm

@login_required(login_url="/login/")
def home_page(request):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	form_class = NewsPostForm
    # if request is not post, initialize an empty form
	form = form_class(request.POST or None)
	
	""" Form logic for registering a new post """
	if request.method == "POST":
		if 'keyset' in request.POST :
			for keyset in request.POST.getlist('keyset'):
				query = keyset.split('-')
				# db_key = Key.objects.filter(name=query[0])
				if query[1] == "not_at_me":
					Key.objects.filter(name=query[0]).update(is_used = False)
				elif query[1] == "at_me_not_using_it":
					Key.objects.filter(name=query[0]).update(is_used = False)
					Key.objects.filter(name=query[0]).update(owner = request.user)
				else:
					Key.objects.filter(name=query[0]).update(is_used = True)
					Key.objects.filter(name=query[0]).update(owner = request.user)

		form = NewsPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
    
	form = NewsPostForm()
	keys_list = Key.objects.all()
	post_list = NewsPost.objects.all()
	#form_my_profile = my_profile(request)
	return render(request, 'blog/home.html', {'form' : form,
		'post_list' : post_list, 'keys_list' : keys_list})

# def my_profile(request):

# 	if request.method == 'POST':
# 		form_my_profile = KeyForm(request.POST)
# 		if form_my_profile.is_valid():
# 			instance = form_my_profile.save(commit=False)
# 			instance.save()
# 	else:
# 		form_my_profile = KeyForm()
# 	return form_my_profile